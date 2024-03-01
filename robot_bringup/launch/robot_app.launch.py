from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # name= rename node
    # remap topic remappings=
    # parameters=

    remap_number_topic = ("number", "my_number")

    wheels_server_node = Node(
        package="dadou_robot/dadourobot/nodes",
        executable="wheels_node",
        name="my_number_publisher",
        remappings=[
            remap_number_topic
        ],
        parameters=[
            {"number_to_publish": 4},
            {"publish_frequency": 5.0}
        ]
    )

    number_counter_node = Node(
        package="tutorial",
        executable="number_counter",
        name="my_number_counter",
        remappings=[
            remap_number_topic,
            ("count", "my_count"),
        ],
        parameters = [
            {"number_to_publish": 4},
            {"publish_frequency": 5.0}
        ]
    )

    ld.add_action(wheels_server_node)
    #ld.add_action(number_counter_node)
    return ld