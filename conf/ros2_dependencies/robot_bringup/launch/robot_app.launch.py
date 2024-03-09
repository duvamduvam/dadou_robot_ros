from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # name= rename node
    # remap topic remappings=
    # parameters=

    #remap_number_topic = ("number", "my_number")

    animations_server_node = Node(
        package="robot",
        executable="animations_node",
        name="animations_node"
    )

    audio_server_node = Node(
        package="robot",
        executable="audio_node",
        name="audio_node"
    )

    face_server_node = Node(
        package="robot",
        executable="face_node",
        name="face_node"
    )

    lights_server_node = Node(
        package="robot",
        executable="lights_node",
        name="lights_node"
    )

    relays_server_node = Node(
        package="robot",
        executable="relays_node",
        name="relays_node"
    )

    system_server_node = Node(
        package="robot",
        executable="system_node",
        name="system_node"
    )

    wheels_server_node = Node(
        package="robot",
        executable="wheels_node",
        name="wheels_node"

        #remappings=[
        #    remap_number_topic
        #],
        #parameters=[
        #    {"number_to_publish": 4},
        #    {"publish_frequency": 5.0}
        #]
    )

    #number_counter_node = Node(
    #    package="robot",
    #    executable="number_counter",
    #    name="my_number_counter",
    #    remappings=[
    #        remap_number_topic,
    #        ("count", "my_count"),
    #    ],
    #    parameters = [
    #        {"number_to_publish": 4},
    #        {"publish_frequency": 5.0}
    #    ]
    #)

    ld.add_action(animations_server_node)
    ld.add_action(audio_server_node)
    ld.add_action(face_server_node)
    ld.add_action(lights_server_node)
    ld.add_action(relays_server_node)
    ld.add_action(system_server_node)
    ld.add_action(wheels_server_node)
    #ld.add_action(number_counter_node)
    return ld