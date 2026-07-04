"""Simulation Gazebo (Harmonic) du robot Dadou.

Lance : serveur gz (+ GUI si headless:=false), spawn du robot depuis
robot_description, robot_state_publisher et le bridge ros_gz.

    ros2 launch robot_sim sim.launch.py            # avec GUI
    ros2 launch robot_sim sim.launch.py headless:=true

Tout tourne en use_sim_time (horloge /clock bridgée depuis gz).
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
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
    ])
