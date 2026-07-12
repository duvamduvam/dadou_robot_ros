#!/usr/bin/env python3
"""Node `gaze_follower` : le robot suit une personne DU REGARD (cou seulement).

SÉCURITÉ (cf. CLAUDE.md) :
 - Ce node ne publie QUE sur le cou (`neck` en mode robot, `/neck/position` en
   mode sim). Il ne touche JAMAIS wheels/cmd_vel*/e_stop — aucun de ces topics
   n'apparaît ici. Le regard ne déplace pas les 50 kg du robot.
 - Il démarre DÉSACTIVÉ (enabled=False) : télécommande > autonome, toujours.
   Activation en direct via le topic `gaze` ("on"/"off") — un bouton télécommande
   pourra s'y brancher plus tard.

NON AJOUTÉ au launch de prod (robot_bringup) POUR L'INSTANT : tant que le sens du
cou (direction_sign) n'a pas été validé au protocole caméra, ce node se lance À LA
MAIN. Voir le rapport de validation sim et « reste à valider sur le vrai robot ».

Node volontairement FIN (I/O seulement) : toute la logique est dans la classe pure
robot.move.gaze_control.GazeControl (testée hors ROS). On n'importe PAS robot_config
ni robot.actions.* : le node reste autonome et tourne tel quel dans le conteneur de
simulation (qui n'embarque pas les dépendances matérielles du Pi).
"""

import json
import time

import rclpy
from geometry_msgs.msg import PointStamped
from rclpy.node import Node
from std_msgs.msg import Float64
from robot_interfaces.msg import StringTime

from robot.move.gaze_control import GazeControl, consigne_to_radians

# Contrats de topics (ne pas dévier — interfaces existantes).
VISION_TOPIC = "/vision/person"     # PointStamped : x=azimut, y=élévation, z=confiance
GAZE_CMD_TOPIC = "gaze"             # StringTime "on"/"off" : activation en direct
NECK_TOPIC_ROBOT = "neck"          # StringTime : consigne 0-99 (vrai robot)
NECK_TOPIC_SIM = "/neck/position"  # Float64 en radians (JointPositionController gz)
LEFT_EYE_TOPIC = "left_eye"        # StringTime : consigne 0-99 (servo œil gauche)
RIGHT_EYE_TOPIC = "right_eye"      # StringTime : consigne 0-99 (servo œil droit)


def _now_ms():
    """Horloge MONOTONE en millisecondes. On n'utilise PAS le temps ROS/sim : le
    suivi du regard n'est pas lié au temps de simulation (contrairement au chemin
    roues), et une horloge monotone évite tout saut d'horloge sur les timeouts."""
    return int(time.monotonic() * 1000)


class GazeFollowerNode(Node):
    def __init__(self):
        super().__init__("gaze_follower")

        # --- Paramètres ROS déclarés (réglables au lancement) ---
        self.declare_parameter("enabled", False)          # DÉSACTIVÉ par défaut
        self.declare_parameter("output_mode", "robot")    # 'robot' | 'sim'
        self.declare_parameter("gain", 20.0)
        # direction_sign=+1 VALIDÉ au protocole caméra réel du 2026-07-12 :
        # boucle fermée stable (la caméra est montée sur la tête — l'azimut
        # converge vers 0 quand le cou tourne vers la personne).
        self.declare_parameter("direction_sign", 1)
        self.declare_parameter("center", 50)
        self.declare_parameter("confidence_min", 0.4)
        # ema_alpha=0.15 / slew_max=1.5 : amortissement VALIDÉ au protocole du
        # 2026-07-12 — avec les valeurs initiales (0.4 / 3.0) la boucle
        # oscillait (cou 53<->61 en va-et-vient : trop de retard de phase
        # cumulé EMA perception + EMA locale + slew + rampe physique du servo
        # pour ce gain). Suivi doux et stable avec ces valeurs.
        self.declare_parameter("ema_alpha", 0.15)
        self.declare_parameter("slew_max", 1.5)
        self.declare_parameter("slew_return", 1.0)
        self.declare_parameter("timeout_ms", 1500)
        self.declare_parameter("tick_hz", 10.0)
        # --- Yeux (2026-07-12) : les servos left_eye/right_eye suivent AUSSI
        # l'azimut. MÊME logique pure (deuxième instance de GazeControl) avec
        # leur propre réglage : gain plus fort et slew plus vif — les yeux
        # dardent, le cou suit, c'est le comportement naturel d'un regard.
        # Consigne IDENTIQUE aux deux yeux (les séquences artistiques leur
        # donnent la même plage 15-90 ; si le montage réel s'avère miroir,
        # ajouter un eye_right_sign — à trancher au protocole visuel).
        # eye_gain=49 (plein débattement 1-99, les séquences artistiques
        # utilisent déjà 0-99 : mécanique éprouvée) et eye_direction_sign=-1 :
        # VALIDÉS visuellement au protocole du 2026-07-12 (le montage des
        # yeux est bien MIROIR du cou — avec +1 le regard fuyait la personne,
        # amplitude jugée trop faible à gain 25 puis 35).
        self.declare_parameter("eyes_enabled", True)
        self.declare_parameter("eye_gain", 49.0)
        self.declare_parameter("eye_center", 50)
        self.declare_parameter("eye_direction_sign", -1)
        self.declare_parameter("eye_slew_max", 8.0)
        self.declare_parameter("eye_slew_return", 3.0)

        enabled = self.get_parameter("enabled").value
        self.output_mode = self.get_parameter("output_mode").value
        tick_hz = self.get_parameter("tick_hz").value

        # Logique pure : instanciée avec les paramètres, puis activée/désactivée.
        self.gaze = GazeControl(
            center=self.get_parameter("center").value,
            gain=self.get_parameter("gain").value,
            direction_sign=self.get_parameter("direction_sign").value,
            confidence_min=self.get_parameter("confidence_min").value,
            ema_alpha=self.get_parameter("ema_alpha").value,
            slew_max=self.get_parameter("slew_max").value,
            slew_return=self.get_parameter("slew_return").value,
            timeout_ms=self.get_parameter("timeout_ms").value,
            enabled=bool(enabled),
        )

        # --- Yeux : deuxième GazeControl, mêmes filtres d'entrée (confiance,
        # timeout), réglages propres. ZÉRO logique nouvelle : la classe pure
        # déjà testée fait tout (EMA, slew, LOST->retour centre, anti-spam).
        self.eyes_enabled = bool(self.get_parameter("eyes_enabled").value)
        self.eyes = GazeControl(
            center=self.get_parameter("eye_center").value,
            gain=self.get_parameter("eye_gain").value,
            direction_sign=self.get_parameter("eye_direction_sign").value,
            confidence_min=self.get_parameter("confidence_min").value,
            ema_alpha=self.get_parameter("ema_alpha").value,
            slew_max=self.get_parameter("eye_slew_max").value,
            slew_return=self.get_parameter("eye_slew_return").value,
            timeout_ms=self.get_parameter("timeout_ms").value,
            enabled=bool(enabled) and self.eyes_enabled,
        )

        # --- Sortie : publishers selon le mode (pas de topic inutile) ---
        if self.output_mode == "sim":
            self.pub = self.create_publisher(Float64, NECK_TOPIC_SIM, 10)
            # Yeux non câblés en sim pour l'instant (pas de joint gz dédié
            # exposé) : le suivi des yeux est validé visuellement en réel.
            self.eye_pubs = []
        else:
            self.pub = self.create_publisher(StringTime, NECK_TOPIC_ROBOT, 10)
            self.eye_pubs = [
                self.create_publisher(StringTime, LEFT_EYE_TOPIC, 10),
                self.create_publisher(StringTime, RIGHT_EYE_TOPIC, 10),
            ] if self.eyes_enabled else []

        # --- Entrées ---
        self.create_subscription(PointStamped, VISION_TOPIC, self._on_person, 10)
        self.create_subscription(StringTime, GAZE_CMD_TOPIC, self._on_gaze_cmd, 10)

        # Timer de tick à cadence fixe.
        self.create_timer(1.0 / tick_hz, self._on_tick)

        self.get_logger().info(
            "gaze_follower démarré : output_mode={} enabled={} (télécommande > autonome)".format(
                self.output_mode, bool(enabled)))

    def _on_person(self, msg):
        # x=azimut [-1..1], y=élévation [-1..1] (ignorée), z=confiance [0..1].
        now = _now_ms()
        self.gaze.update(msg.point.x, msg.point.y, msg.point.z, now)
        self.eyes.update(msg.point.x, msg.point.y, msg.point.z, now)

    def _on_gaze_cmd(self, ros_msg):
        # Le fil StringTime porte "on"/"off" (json ou brut, on tolère les deux).
        raw = ros_msg.msg
        try:
            value = json.loads(raw)
        except (ValueError, TypeError):
            value = raw
        if value in ("on", True, 1, "1"):
            self.gaze.set_enabled(True)
            self.eyes.set_enabled(self.eyes_enabled)
            self.get_logger().info("gaze ON : suivi du regard activé (cou{})".format(
                " + yeux" if self.eyes_enabled else ""))
        elif value in ("off", False, 0, "0"):
            self.gaze.set_enabled(False)  # reset complet de l'état
            self.eyes.set_enabled(False)
            self.get_logger().info("gaze OFF : suivi désactivé, état réinitialisé")
        else:
            self.get_logger().warn("commande gaze inconnue : {!r}".format(raw))

    def _on_tick(self):
        now = _now_ms()
        consigne = self.gaze.tick(now)
        if consigne is not None:
            if self.output_mode == "sim":
                self.pub.publish(Float64(data=consigne_to_radians(consigne)))
            else:
                # Contrat vrai robot : msg = json.dumps(valeur 0-99), time = 0.
                self.pub.publish(StringTime(msg=json.dumps(consigne), time=0))

        # Yeux : même consigne aux deux servos (cf. déclaration des paramètres),
        # anti-spam porté par l'instance GazeControl dédiée.
        eye_consigne = self.eyes.tick(now)
        if eye_consigne is not None:
            for pub in self.eye_pubs:
                pub.publish(StringTime(msg=json.dumps(eye_consigne), time=0))


def main(args=None):
    rclpy.init(args=args)
    node = GazeFollowerNode()
    try:
        rclpy.spin(node)
    except Exception as e:
        node.get_logger().error(str(e))
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
