from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # name= rename node
    # remap topic remappings=
    # parameters=

    remap_number_topic = ("number", "my_number")

    turtlesime_display_node = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )

    turtlesime_spwner_node = Node(
        package="tutorial",
        executable="turtlesim_spawner"
    )

    turtlesime_controller_node = Node(
        package="tutorial",
        executable="turtlesim_controller"
    )

    ld.add_action(turtlesime_display_node)
    ld.add_action(turtlesime_spwner_node)
    ld.add_action(turtlesime_controller_node)
    return ld