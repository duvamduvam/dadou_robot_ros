"""Pont web du robot (W0) : supervision + contenus + panneau technique.

    ros2 launch robot_web web.launch.py
    ros2 launch robot_web web.launch.py web_port:=8765 token:=secret

Pas de use_sim_time ici : les timeouts de session (heartbeat WRITE_TIMEOUT_S)
sont mesurés en horloge MURALE (time.monotonic(), voir web_protocol.py), pas
en horloge simulée -- un opérateur humain de l'autre côté du WebSocket vit en
temps réel, que le Gazebo tourne à 1x, en pause ou accéléré n'y change rien.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("web_port", default_value="8765",
                              description="Port HTTP/WebSocket du pont web (8088 évité : défaut"
                                           " Superset, collision vue sur le PC de dev)"),
        DeclareLaunchArgument("token", default_value="",
                              description="Token d'auth ; vide = accès libre (dev/sim)"),
        DeclareLaunchArgument("json_dir", default_value="/home/ros2_ws/json",
                              description="Dossier json/ (catalogue faces/audios/animations/relais/lights)"),

        Node(
            package="robot_web",
            executable="web_bridge",
            name="web_bridge_node",
            parameters=[{
                "web_port": LaunchConfiguration("web_port"),
                "token": LaunchConfiguration("token"),
                "json_dir": LaunchConfiguration("json_dir"),
            }],
        ),
    ])
