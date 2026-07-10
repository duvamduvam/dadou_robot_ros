"""Simulation Gazebo (Harmonic) du robot Dadou.

Lance : serveur gz (+ GUI si headless:=false), spawn du robot depuis
robot_description, robot_state_publisher et le bridge ros_gz.

    ros2 launch robot_sim sim.launch.py            # avec GUI
    ros2 launch robot_sim sim.launch.py headless:=true

    # Rejeu des séquences JSON (animations_node, package "robot" -- OFF par
    # défaut, comme gaze_follower : lancement explicite requis) :
    ros2 launch robot_sim sim.launch.py animations:=true
    # puis, dans un autre terminal (même domaine ROS que la sim, 43) :
    #   ros2 topic pub -1 animation robot_interfaces/msg/StringTime '{msg: "\\"parle\\""}'

Tout tourne en use_sim_time (horloge /clock bridgée depuis gz).
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

# base_link est au centre de la caisse : rayon roue (0.13) + demi-hauteur
# de caisse (0.10), plus 1 cm de marge pour poser le robot sans le coincer.
SPAWN_Z = "0.24"


def generate_launch_description():
    headless = LaunchConfiguration("headless")
    animations = LaunchConfiguration("animations")

    robot_description = ParameterValue(
        Command([
            "xacro ",
            PathJoinSubstitution([
                FindPackageShare("robot_description"), "urdf", "dadou_robot_gz.urdf.xacro",
            ]),
        ]),
        value_type=str,
    )

    world = PathJoinSubstitution([FindPackageShare("robot_sim"), "worlds", "stage.sdf"])

    # -r : la simulation démarre en lecture (pas en pause) ; -s : serveur seul.
    gz_args = [
        world, " -r",
        PythonExpression(["' -s' if '", headless, "' == 'true' else ''"]),
    ]

    return LaunchDescription([
        DeclareLaunchArgument("headless", default_value="false",
                              description="true = serveur gz seul, sans GUI"),
        DeclareLaunchArgument("animations", default_value="false",
                              description="true = lance animations_node (paquet robot, rejeu des"
                                           " séquences JSON) -- OFF par défaut, même prudence que"
                                           " gaze_follower : activation explicite requise"),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"])
            ),
            launch_arguments={"gz_args": gz_args}.items(),
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description, "use_sim_time": True}],
        ),

        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=["-topic", "robot_description", "-name", "dadou_robot", "-z", SPAWN_Z],
            output="screen",
        ),

        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            parameters=[{
                "config_file": PathJoinSubstitution([
                    FindPackageShare("robot_sim"), "config", "gz_bridge.yaml",
                ]),
                "use_sim_time": True,
            }],
            output="screen",
        ),

        # Visualisation LED (matériaux émissifs gz, cf. robot_sim_lib/leds_logic.py) :
        # écoute robot_lights/face côté ROS, publie /material_color (bridgé vers
        # /world/stage/material_color, système gz UserCommands du monde `stage`).
        Node(
            package="robot_sim",
            executable="leds_sim_node",
            parameters=[{"use_sim_time": True}],
            output="screen",
        ),

        # Rejeu des servos (neck/left_arm/right_arm/left_eye/right_eye, cf.
        # robot_sim_lib/servos_logic.py) : écoute les 5 topics StringTime,
        # publie /<servo>/position (radians) sur les JointPositionController gz.
        Node(
            package="robot_sim",
            executable="servos_sim_node",
            parameters=[{"use_sim_time": True}],
            output="screen",
        ),

        # Rejeu des séquences JSON (paquet "robot", le VRAI code du robot --
        # PAS un paquet robot_sim, cf. Dockerfile-sim/docker-compose-sim.yml
        # pour comment il est construit dans le conteneur sim). OFF par défaut
        # (animations:=false) : même prudence que gaze_follower, activation
        # explicite. LIMITE ASSUMÉE : AnimationManager/Animation utilisent
        # TimeUtils.current_milli_time() (horloge MURALE partout, jamais
        # get_clock()) -- comme sur le vrai robot, donc pas une régression,
        # mais le rejeu ne suit PAS l'horloge simulée (use_sim_time n'aurait
        # aucun effet ici ; on ne le passe donc pas, contrairement aux autres
        # nodes de ce fichier).
        Node(
            package="robot",
            executable="animations_node",
            output="screen",
            condition=IfCondition(animations),
        ),
    ])
