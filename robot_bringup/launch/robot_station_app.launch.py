from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # name= rename node
    # remap topic remappings=
    # parameters=

    remap_number_topic = ("number", "my_number")

    robot_station_node1 = Node(
        package="tutorial",
        executable="robot_news_station",
        name="robot_station_1"
    )

    robot_station_node2 = Node(
        package="tutorial",
        executable="robot_news_station",
        name="robot_station_2"
    )

    robot_station_node3 = Node(
        package="tutorial",
        executable="robot_news_station",
        name="robot_station_3"
    )

    robot_station_node4 = Node(
        package="tutorial",
        executable="robot_news_station",
        name="robot_station_4"
    )

    robot_station_node5 = Node(
        package="tutorial",
        executable="robot_news_station",
        name="robot_station_5"
    )

    smartphone_node = Node(
        package="tutorial",
        executable="smartphone"
    )

    ld.add_action(robot_station_node1)
    ld.add_action(robot_station_node2)
    ld.add_action(robot_station_node3)
    ld.add_action(robot_station_node4)
    ld.add_action(robot_station_node5)
    ld.add_action(smartphone_node)
    return ld