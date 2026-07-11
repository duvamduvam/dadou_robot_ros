"""Protocole du pont web (W0), logique 100% PURE : aucun import rclpy/aiohttp/
robot/dadou_utils_ros -- testable sans ROS ni réseau (garde-fou AST dans
test_web_protocol.py, même motif que wheels_payload.py).

Trois responsabilités :
 - la WHITELIST des topics publiables (contrat de sécurité W0 : wheels/
   cmd_vel_* et e_stop ne DOIVENT jamais y figurer -- voir CLAUDE.md/
   docs/etude-interface-web.md, W0 = supervision + contenus, pas les roues) ;
 - le parsing/validation des messages client -> serveur (parse_client_message) ;
 - la session d'écriture exclusive + heartbeat (WebSession/SessionManager).

Horloge injectée partout (paramètre `now_s`) plutôt que time.time() interne :
c'est ce qui permet de tester le timeout heartbeat en avançant une horloge
factice à la main, sans time.sleep() ni monkeypatch (même philosophie que
TwistDeadman.is_expired(now_ms) dans robot_drive.deadman).
"""

import json

# --- Whitelist des topics publiables --------------------------------------
# Chaînes littérales dupliquées volontairement (pas d'import dadou_utils_ros.
# utils_static) : robot_web est un package AUTONOME façon robot_drive, le
# conteneur de simulation ne l'embarque pas. wheels/cmd_vel_*/e_stop sont
# ABSENTS ici par construction -- c'est la garantie W0 (pas d'accès roues ni
# verrou e_stop tant que W1/W3 ne sont pas faits, voir etude-interface-web.md).
WHITELIST_SPECTACLE = {"animation", "face", "audio", "robot_lights"}
WHITELIST_TECHNIQUE = {"relay", "neck", "left_eye", "right_eye", "left_arm", "right_arm", "gaze", "system"}
WHITELIST = WHITELIST_SPECTACLE | WHITELIST_TECHNIQUE

# Session d'écriture : silence du writer au-delà de ce délai -> écriture
# libérée (personne ne la récupère automatiquement, cf. §2 du protocole).
WRITE_TIMEOUT_S = 3.0
# Cadence attendue du heartbeat client (exportée pour que l'UI s'y cale).
HEARTBEAT_PERIOD_S = 1.0


class ProtocolError(Exception):
    """Message client invalide (JSON cassé, type inconnu, topic hors
    whitelist, champ manquant). Le node l'attrape SANS fermer la connexion
    et répond {"type": "err", ...} -- motif du décodage StringTime commun
    (payload invalide = refus loggué, jamais une perte silencieuse)."""

    def __init__(self, raison):
        super().__init__(raison)
        self.raison = raison


# --- Parsing des messages client -> serveur --------------------------------

def _is_plain_int(value) -> bool:
    # bool est une sous-classe d'int en Python : un horodatage/une durée ne
    # peut pas être True/False, on l'exclut explicitement partout où on
    # attend un entier (hb.t, cmd.time).
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_auth(msg: dict) -> dict:
    token = msg.get("token")
    if token is not None and not isinstance(token, str):
        raise ProtocolError("auth.token doit être une chaîne ou null")
    return {"type": "auth", "token": token}


def _parse_hb(msg: dict) -> dict:
    t = msg.get("t")
    if not _is_plain_int(t):
        raise ProtocolError("hb.t manquant ou non entier")
    return {"type": "hb", "t": t}


def _parse_cmd(msg: dict) -> dict:
    topic = msg.get("topic")
    if topic not in WHITELIST:
        raise ProtocolError("topic hors whitelist : {!r}".format(topic))
    if "value" not in msg:
        raise ProtocolError("cmd.value manquant")
    time_ms = msg.get("time", 0)
    if not _is_plain_int(time_ms):
        raise ProtocolError("cmd.time doit être un entier (ms)")
    # Borné ici et pas dans le node : StringTime.time est un int64, une valeur
    # hors bornes ferait lever rclpy à l'affectation et tuerait la connexion
    # du client au lieu d'un refus propre. Négatif refusé aussi : time est une
    # durée/un temps restant en ms, jamais négatif dans le contrat existant.
    if not 0 <= time_ms < 2 ** 63:
        raise ProtocolError("cmd.time hors bornes (0 <= ms < 2^63)")
    return {"type": "cmd", "topic": topic, "value": msg["value"], "time": time_ms}


# Dispatch par type : chaque entrée valide/normalise son propre message
# (dict -> dict), les types sans champ additionnel se contentent de le
# renvoyer tel quel. Table plutôt qu'une cascade de if/elif : c'est ce qui
# tenait parse_client_message() sous le seuil de complexité cyclomatique du
# linter (S3776) tout en gardant chaque règle isolée et testable.
_PARSERS = {
    "auth": _parse_auth,
    "hb": _parse_hb,
    "cmd": _parse_cmd,
    "take_control": lambda msg: {"type": "take_control"},
    "stop_all": lambda msg: {"type": "stop_all"},
}


def parse_client_message(raw: str) -> dict:
    """JSON brut reçu sur le WebSocket -> dict validé et normalisé (defaults
    appliqués, ex. cmd.time). Lève ProtocolError sur toute entrée invalide."""
    try:
        msg = json.loads(raw)
    except (TypeError, ValueError) as e:
        raise ProtocolError("JSON illisible : {}".format(e))

    if not isinstance(msg, dict):
        raise ProtocolError("message non-objet : {!r}".format(msg))

    msg_type = msg.get("type")
    if msg_type is None:
        raise ProtocolError("champ 'type' manquant")

    parser = _PARSERS.get(msg_type)
    if parser is None:
        raise ProtocolError("type de message inconnu : {!r}".format(msg_type))
    return parser(msg)


# --- Bouton STOP CONTENUS ---------------------------------------------------

def stop_all_commands() -> list:
    """Liste EXACTE (topic, valeur_python) publiée par le bouton STOP CONTENUS,
    dans cet ordre. Pas de roues en W0 ; le verrou e_stop viendra en W1."""
    return [
        ("animation", False),
        ("audio", "stop"),
        ("face", "stop"),
        ("neck", "stop"),
        ("left_eye", "stop"),
        ("right_eye", "stop"),
        ("left_arm", "stop"),
        ("right_arm", "stop"),
    ]


# --- Mode robot / sim (sécurité : toujours savoir à qui on parle) ----------

def mode_from_domain_id(domain_id: int) -> str:
    """domain 43 -> SIMULATION, 42 -> ROBOT RÉEL, autre -> INCONNU (affiché
    tel quel, jamais masqué : voir §2 de la spec, "on doit TOUJOURS savoir à
    qui on parle")."""
    if domain_id == 43:
        return "SIMULATION"
    if domain_id == 42:
        return "ROBOT RÉEL"
    return "INCONNU"


# --- Messages serveur -> client (constructeurs purs) ------------------------

def build_hello(domain_id: int, writer: bool, token_required: bool) -> dict:
    return {
        "type": "hello",
        "domain_id": domain_id,
        "mode": mode_from_domain_id(domain_id),
        "writer": writer,
        "token_required": token_required,
    }


def build_hb_ack(t) -> dict:
    return {"type": "hb_ack", "t": t}


def build_ack(topic: str) -> dict:
    return {"type": "ack", "topic": topic}


def build_err(reason: str) -> dict:
    return {"type": "err", "reason": reason}


def build_state(topics: dict, nodes: list, clients: int, writer_present: bool) -> dict:
    return {"type": "state", "topics": topics, "nodes": nodes, "clients": clients,
            "writer_present": writer_present}


# --- Session d'écriture exclusive + heartbeat -------------------------------

class WebSession:
    """État d'un client connecté. authenticated conditionne tout le reste
    (take_control/heartbeat sont no-op pour un client non authentifié)."""

    def __init__(self):
        self.authenticated = False
        self.last_hb_s = None  # dernier battement reçu (horloge injectée), None si jamais


class SessionManager:
    """Gestion pure de l'auth + de l'écriture exclusive. Horloge TOUJOURS
    passée en paramètre (now_s) par l'appelant (le node), jamais lue en
    interne -- c'est ce qui rend check_timeouts()/heartbeat() testables sans
    horloge réelle."""

    def __init__(self, token: str | None):
        # Token serveur vide/None = accès libre (mode dev/sim, cf. §2).
        self.token = token or None
        self._sessions: dict[str, WebSession] = {}
        self.writer_id: str | None = None

    @property
    def token_required(self) -> bool:
        return self.token is not None

    def authenticate(self, client_id: str, token, now_s: float) -> bool:
        """Le premier client authentifié prend l'écriture automatiquement.
        Renvoie False (rejet) si un token serveur est configuré et que celui
        du client ne correspond pas -- la session reste non authentifiée."""
        if self.token_required and token != self.token:
            return False

        session = self._sessions.setdefault(client_id, WebSession())
        session.authenticated = True
        if self.writer_id is None:
            self._grant_write(client_id, now_s)
        return True

    def take_control(self, client_id: str, now_s: float) -> bool:
        """Reprise d'écriture EXPLICITE (opérateur unique, confirmée côté
        client). Toujours autorisée pour un client authentifié, même si un
        autre écrit déjà -- il n'y a qu'un seul opérateur en pratique."""
        session = self._sessions.get(client_id)
        if session is None or not session.authenticated:
            return False
        self._grant_write(client_id, now_s)
        return True

    def _grant_write(self, client_id: str, now_s: float) -> None:
        self.writer_id = client_id
        self._sessions[client_id].last_hb_s = now_s

    def heartbeat(self, client_id: str, now_s: float) -> bool:
        """Réarme l'horloge d'écriture. Un battement d'un non-writer est
        ignoré (il n'a rien à réarmer)."""
        if client_id != self.writer_id:
            return False
        self._sessions[client_id].last_hb_s = now_s
        return True

    def check_timeouts(self, now_s: float) -> str | None:
        """À appeler périodiquement par le node. Libère l'écriture si le
        writer est silencieux depuis plus de WRITE_TIMEOUT_S ; renvoie
        l'identifiant du client libéré (pour que le node le loggue et le
        notifie individuellement), ou None si rien n'a changé."""
        if self.writer_id is None:
            return None

        session = self._sessions.get(self.writer_id)
        if session is None or session.last_hb_s is None \
                or (now_s - session.last_hb_s) > WRITE_TIMEOUT_S:
            released_id = self.writer_id
            self.writer_id = None
            return released_id
        return None

    def remove_client(self, client_id: str) -> bool:
        """Déconnexion : la session est oubliée. Si c'était le writer,
        l'écriture est libérée -- personne ne la récupère automatiquement
        (cf. §2). Renvoie True si le writer a été libéré (pour le log)."""
        was_writer = (client_id == self.writer_id)
        self._sessions.pop(client_id, None)
        if was_writer:
            self.writer_id = None
        return was_writer

    def is_writer(self, client_id: str) -> bool:
        return client_id == self.writer_id

    def writer_present(self) -> bool:
        return self.writer_id is not None

    def client_count(self) -> int:
        return len(self._sessions)
