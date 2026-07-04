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
        self.declare_parameter("direction_sign", 1)       # +1/-1 (à valider caméra)
        self.declare_parameter("center", 50)
        self.declare_parameter("confidence_min", 0.4)
        self.declare_parameter("ema_alpha", 0.4)
        self.declare_parameter("slew_max", 3.0)
        self.declare_parameter("slew_return", 1.0)
        self.declare_parameter("timeout_ms", 1500)
        self.declare_parameter("tick_hz", 10.0)

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

        # --- Sortie : un seul publisher, selon le mode (pas de topic inutile) ---
        if self.output_mode == "sim":
            self.pub = self.create_publisher(Float64, NECK_TOPIC_SIM, 10)
        else:
            self.pub = self.create_publisher(StringTime, NECK_TOPIC_ROBOT, 10)

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
        self.gaze.update(msg.point.x, msg.point.y, msg.point.z, _now_ms())

    def _on_gaze_cmd(self, ros_msg):
        # Le fil StringTime porte "on"/"off" (json ou brut, on tolère les deux).
        raw = ros_msg.msg
        try:
            value = json.loads(raw)
        except (ValueError, TypeError):
            value = raw
        if value in ("on", True, 1, "1"):
            self.gaze.set_enabled(True)
            self.get_logger().info("gaze ON : suivi du regard activé")
        elif value in ("off", False, 0, "0"):
            self.gaze.set_enabled(False)  # reset complet de l'état
            self.get_logger().info("gaze OFF : suivi désactivé, état réinitialisé")
        else:
            self.get_logger().warn("commande gaze inconnue : {!r}".format(raw))

    def _on_tick(self):
        consigne = self.gaze.tick(_now_ms())
        if consigne is None:
            return  # rien à publier (IDLE ou consigne inchangée) -> pas de spam
        if self.output_mode == "sim":
            self.pub.publish(Float64(data=consigne_to_radians(consigne)))
        else:
            # Contrat vrai robot : msg = json.dumps(valeur 0-99), time = 0.
            self.pub.publish(StringTime(msg=json.dumps(consigne), time=0))


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
