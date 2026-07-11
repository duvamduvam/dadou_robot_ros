#!/usr/bin/env python3
"""Node rclpy + serveur aiohttp (HTTP + WebSocket) du pont web W0 : supervision,
contenus (animation/face/audio/robot_lights), panneau technique (servos/relais/
gaze/system). AUCUN accès roues ni verrou e_stop -- la whitelist qui le garantit
vit dans web_protocol.py (import unique de vérité, testé en isolation).

PIÈGE DEUX BOUCLES D'ÉVÉNEMENTS : rclpy.spin() est une boucle bloquante propre
à rclpy ; aiohttp a besoin de SA PROPRE boucle asyncio pour servir les
WebSockets. On ne les mélange PAS dans le même thread (rclpy.spin() ne rend
jamais la main à un event loop asyncio, et inversement) :
 - rclpy.spin(node) tourne dans un thread dédié (daemon, démarré dans main()) ;
 - aiohttp (web.run_app, boucle asyncio) tourne dans le thread principal.
Les deux communiquent par deux canaux, chacun protégé pour son usage :
 - `publisher.publish()` est thread-safe côté rclpy (documenté) : les
   handlers WebSocket (thread asyncio) appellent directement
   WebBridgeNode.publish_cmd(), aucune synchronisation nécessaire ;
 - `self.last_topics` (dernier payload par topic, pour la supervision) est
   ÉCRIT par les callbacks d'abonnement (thread spin) et LU par le timer
   asyncio qui construit le message "state" (thread aiohttp) : protégé par
   `self.lock` (threading.Lock, PAS asyncio.Lock -- les deux accès ne sont
   pas dans la même boucle d'événements).
`SessionManager`, lui, n'est touché QUE depuis le thread asyncio (tous les
handlers WS + le timer de diffusion y tournent) : pas besoin de le protéger.
"""

import asyncio
import json
import logging
import os
import pathlib
import threading
import time
import uuid

import rclpy
from aiohttp import web, WSMsgType
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node

from robot_interfaces.msg import StringTime
from robot_web.web_catalog import build_catalog
from robot_web.web_protocol import (
    WHITELIST, WRITE_TIMEOUT_S, ProtocolError, SessionManager,
    build_ack, build_err, build_hb_ack, build_hello, build_state,
    parse_client_message, stop_all_commands,
)

STATE_PERIOD_S = 2.0  # cadence de diffusion du message "state" à tous les clients
NODES_REFRESH_PERIOD_S = 5.0  # get_node_names_and_namespaces() : évite de le refaire à 2 Hz


class WebBridgeNode(Node):

    def __init__(self):
        super().__init__("web_bridge_node")

        # 8765 et pas 8088 : 8088 est le port par défaut de Superset, collision
        # RÉELLE constatée sur le PC de dev (réseau host, bind refusé au premier
        # lancement). Surchargable via le paramètre (WEB_PORT côté compose sim).
        self.declare_parameter("web_port", 8765)
        self.declare_parameter("token", "")
        self.declare_parameter("json_dir", "/home/ros2_ws/json")

        self.web_port = self.get_parameter("web_port").value
        self.json_dir = self.get_parameter("json_dir").value
        token = self.get_parameter("token").value or None

        # ROS_DOMAIN_ID n'est pas exposé comme paramètre de node par rclpy :
        # c'est une variable d'environnement du PROCESSUS, lue une fois au
        # démarrage (elle ne change jamais en cours de vie du node).
        try:
            self.domain_id = int(os.environ.get("ROS_DOMAIN_ID", "-1"))
        except ValueError:
            self.domain_id = -1

        self.sessions = SessionManager(token)

        # last_topics : topic -> {"msg": <valeur brute décodée>, "at_s": horloge monotone}.
        self.lock = threading.Lock()
        self.last_topics = {}
        self.node_names_cache = []

        # Un publisher/subscriber par topic whitelisté : IMPOSSIBLE de publier
        # ailleurs (pas de create_publisher générique côté handlers WS).
        self.publishers_by_topic = {
            topic: self.create_publisher(StringTime, topic, 10) for topic in sorted(WHITELIST)
        }
        for topic in sorted(WHITELIST):
            self.create_subscription(StringTime, topic, self._make_listener(topic), 10)

        self.get_logger().info(
            "web_bridge_node prêt : port={} domain_id={} token_required={} json_dir={}".format(
                self.web_port, self.domain_id, self.sessions.token_required, self.json_dir))

    def _make_listener(self, topic):
        """Une closure par topic : le callback doit savoir sous quelle clé
        ranger la valeur reçue dans last_topics."""
        def _on_message(msg):
            try:
                value = json.loads(msg.msg)
            except (TypeError, json.JSONDecodeError):
                # Payload non-JSON (ne devrait pas arriver, cf. décodage StringTime
                # commun côté nodes robot) : republié tel quel, la supervision ne
                # doit jamais planter sur un topic externe au bridge.
                value = msg.msg
            with self.lock:
                self.last_topics[topic] = {"msg": value, "at_s": time.monotonic()}
        return _on_message

    def publish_cmd(self, topic: str, value, time_ms: int = 0) -> None:
        """Publie une commande web. Sérialisation EXACTEMENT comme la
        télécommande (main_no_gui) : msg.msg = json.dumps(valeur nue) --
        "joie" -> '"joie"', False -> 'false' -- pas de ré-emballage {topic: valeur}
        sur le fil (voir docs/interfaces.md)."""
        ros_msg = StringTime()
        ros_msg.msg = json.dumps(value)
        ros_msg.time = time_ms
        ros_msg.anim = False
        self.publishers_by_topic[topic].publish(ros_msg)

    def snapshot_topics(self) -> dict:
        """Copie protégée de last_topics, âge recalculé à l'instant présent."""
        now = time.monotonic()
        with self.lock:
            items = dict(self.last_topics)
        return {
            topic: {"msg": info["msg"], "age_s": round(now - info["at_s"], 1)}
            for topic, info in items.items()
        }

    def refresh_node_names(self) -> None:
        self.node_names_cache = sorted(
            name for name, _namespace in self.get_node_names_and_namespaces())

    def hello_message(self, client_id: str) -> dict:
        return build_hello(self.domain_id, writer=self.sessions.is_writer(client_id),
                            token_required=self.sessions.token_required)


# --- Serveur HTTP / WebSocket (thread asyncio) ------------------------------

async def _send_json_safe(ws: web.WebSocketResponse, payload: dict) -> None:
    """Best-effort : un client qui a fermé sa socket entre-temps ne doit pas
    faire planter le diffuseur d'état ni un handler de commande."""
    if ws.closed:
        return
    try:
        await ws.send_json(payload)
    except ConnectionResetError:
        pass


async def catalog_handler(request: web.Request) -> web.Response:
    node = request.app["node"]
    return web.json_response(build_catalog(node.json_dir))


async def handle_client_message(node: WebBridgeNode, app: web.Application,
                                 client_id: str, ws: web.WebSocketResponse, raw: str) -> None:
    """Décode puis applique un message client. Chaque commande acceptée est
    logguée en INFO (topic + payload + id client, journal exigé par le plan) ;
    chaque refus (parsing, écriture non détenue, auth) en WARNING -- motif du
    décodage StringTime commun : refus loggué, jamais une perte silencieuse."""
    try:
        msg = parse_client_message(raw)
    except ProtocolError as e:
        node.get_logger().warning("message web rejeté id={} : {}".format(client_id, e.raison))
        await _send_json_safe(ws, build_err(e.raison))
        return

    msg_type = msg["type"]

    if msg_type == "auth":
        now_s = time.monotonic()
        if not node.sessions.authenticate(client_id, msg["token"], now_s):
            node.get_logger().warning("auth web refusée id={} (mauvais token)".format(client_id))
            await _send_json_safe(ws, build_err("token invalide"))
            return
        node.get_logger().info("auth web acceptée id={} writer={}".format(
            client_id, node.sessions.is_writer(client_id)))
        await _send_json_safe(ws, node.hello_message(client_id))
        return

    if msg_type == "hb":
        node.sessions.heartbeat(client_id, time.monotonic())
        await _send_json_safe(ws, build_hb_ack(msg["t"]))
        return

    if msg_type == "take_control":
        previous_writer = node.sessions.writer_id
        if not node.sessions.take_control(client_id, time.monotonic()):
            await _send_json_safe(ws, build_err("non authentifié"))
            return
        node.get_logger().info("prise de main écriture id={}".format(client_id))
        await _send_json_safe(ws, node.hello_message(client_id))
        # L'ancien writer (autre onglet/opérateur) doit voir son bandeau
        # repasser en lecture seule sans attendre le prochain "state".
        if previous_writer and previous_writer != client_id and previous_writer in app["clients"]:
            await _send_json_safe(app["clients"][previous_writer],
                                   build_hello(node.domain_id, writer=False,
                                               token_required=node.sessions.token_required))
        return

    if msg_type == "stop_all":
        if not node.sessions.is_writer(client_id):
            node.get_logger().warning("stop_all refusé (lecture seule) id={}".format(client_id))
            await _send_json_safe(ws, build_err("écriture non détenue"))
            return
        for topic, value in stop_all_commands():
            node.publish_cmd(topic, value)
        node.get_logger().info("STOP CONTENUS déclenché id={}".format(client_id))
        await _send_json_safe(ws, build_ack("stop_all"))
        return

    if msg_type == "cmd":
        if not node.sessions.is_writer(client_id):
            node.get_logger().warning("cmd web refusée (lecture seule) id={} topic={}".format(
                client_id, msg["topic"]))
            await _send_json_safe(ws, build_err("écriture non détenue"))
            return
        node.publish_cmd(msg["topic"], msg["value"], msg["time"])
        node.get_logger().info("cmd web id={} topic={} payload={!r}".format(
            client_id, msg["topic"], msg["value"]))
        await _send_json_safe(ws, build_ack(msg["topic"]))


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    node = request.app["node"]
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client_id = str(uuid.uuid4())
    request.app["clients"][client_id] = ws
    node.get_logger().info("client web connecté id={}".format(client_id))

    # hello immédiat, AVANT toute auth : le bandeau (mode SIMULATION/ROBOT RÉEL/
    # INCONNU) doit s'afficher même pendant que l'opérateur choisit son token.
    await _send_json_safe(ws, node.hello_message(client_id))

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                await handle_client_message(node, request.app, client_id, ws, msg.data)
            elif msg.type == WSMsgType.ERROR:
                node.get_logger().warning("erreur WebSocket id={} : {}".format(
                    client_id, ws.exception()))
    finally:
        released = node.sessions.remove_client(client_id)
        request.app["clients"].pop(client_id, None)
        node.get_logger().info("client web déconnecté id={} (écriture libérée: {})".format(
            client_id, released))

    return ws


async def _broadcast(app: web.Application, payload: dict) -> None:
    # list() volontaire (pas une scorie) : chaque send est un point d'await où
    # un client peut se (dé)connecter et muter app["clients"] -- itérer le
    # dict vivant lèverait RuntimeError, on fige donc un instantané.
    for ws in list(app["clients"].values()):
        await _send_json_safe(ws, payload)


async def _state_loop(app: web.Application) -> None:
    """Boucle de fond (une par process, démarrée par cleanup_ctx) : toutes les
    STATE_PERIOD_S, vérifie le timeout heartbeat puis diffuse l'état à tous
    les clients connectés."""
    node = app["node"]
    last_nodes_refresh = 0.0
    while True:
        await asyncio.sleep(STATE_PERIOD_S)

        now_s = time.monotonic()
        released_id = node.sessions.check_timeouts(now_s)
        if released_id is not None:
            node.get_logger().warning(
                "écriture libérée par timeout heartbeat (> {:.1f}s) id={}".format(
                    WRITE_TIMEOUT_S, released_id))
            if released_id in app["clients"]:
                await _send_json_safe(app["clients"][released_id], build_hello(
                    node.domain_id, writer=False, token_required=node.sessions.token_required))

        if now_s - last_nodes_refresh > NODES_REFRESH_PERIOD_S:
            node.refresh_node_names()
            last_nodes_refresh = now_s

        await _broadcast(app, build_state(
            topics=node.snapshot_topics(),
            nodes=node.node_names_cache,
            clients=len(app["clients"]),
            writer_present=node.sessions.writer_present(),
        ))


async def _state_loop_ctx(app: web.Application):
    """cleanup_ctx aiohttp : démarre la boucle de fond au premier `up`, la
    coupe proprement au `cleanup` (sinon la task fuit au redémarrage/reload)."""
    task = asyncio.ensure_future(_state_loop(app))
    yield
    task.cancel()


def build_app(node: WebBridgeNode) -> web.Application:
    app = web.Application()
    app["node"] = node
    app["clients"] = {}  # client_id -> WebSocketResponse, pour le broadcast d'état

    static_dir = pathlib.Path(get_package_share_directory("robot_web")) / "static"

    async def index_handler(_request):
        return web.FileResponse(static_dir / "index.html")

    app.router.add_get("/", index_handler)
    app.router.add_get("/api/catalog", catalog_handler)
    app.router.add_get("/ws", websocket_handler)
    app.router.add_static("/static/", static_dir)

    app.cleanup_ctx.append(_state_loop_ctx)
    return app


def main(args=None):
    rclpy.init(args=args)
    node = WebBridgeNode()
    try:
        # rclpy.spin dans un thread daemon : voir le pourquoi en tête de fichier.
        # daemon=True -> pas besoin de join() explicite, le thread meurt avec
        # le process (web.run_app est la boucle principale, bloquante).
        spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
        spin_thread.start()
        web.run_app(build_app(node), host="0.0.0.0", port=node.web_port)
    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
