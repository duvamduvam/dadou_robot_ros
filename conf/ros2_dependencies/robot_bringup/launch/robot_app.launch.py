from launch import LaunchDescription
from launch_ros.actions import Node

from dadou_utils_ros.utils_static import NAME, NECK, HEAD_PWM_NB, DEFAULT_POS, MAX_POS, LEFT_ARM, LEFT_ARM_NB, \
    RIGHT_ARM, RIGHT_ARM_NB, LEFT_EYE, LEFT_EYE_NB, RIGHT_EYE, RIGHT_EYE_NB
from robot.robot_config import config


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
    )

    neck_server_node = Node(
        package="robot",
        executable="servo_node",
        name="{}_node".format(NECK),
        parameters=[
            {NAME: NECK},
            {HEAD_PWM_NB: config[HEAD_PWM_NB]},
            {DEFAULT_POS: 70},
            {MAX_POS: 180}
        ]
    )

    left_arm_server_node = Node(
        package="robot",
        executable="servo_node",
        name="{}_node".format(LEFT_ARM),
        parameters=[
            {NAME: LEFT_ARM},
            {HEAD_PWM_NB: config[LEFT_ARM_NB]},
            {DEFAULT_POS: 70},
            {MAX_POS: 180}
        ]
    )

    right_arm_server_node = Node(
        package="robot",
        executable="servo_node",
        name="{}_node".format(RIGHT_ARM),
        parameters=[
            {NAME: RIGHT_ARM},
            {HEAD_PWM_NB: config[RIGHT_ARM_NB]},
            {DEFAULT_POS: 160},
            {MAX_POS: 180}
        ]
    )

    left_eye_server_node = Node(
        package="robot",
        executable="servo_node",
        name="{}_node".format(NECK),
        parameters=[
            {NAME: LEFT_EYE},
            {HEAD_PWM_NB: config[LEFT_EYE_NB]},
            {DEFAULT_POS: 70},
            {MAX_POS: 180}
        ]
    )

    right_eye_server_node = Node(
        package="robot",
        executable="servo_node",
        name="{}_node".format(RIGHT_EYE),
        parameters=[
            {NAME: RIGHT_EYE},
            {HEAD_PWM_NB: config[RIGHT_EYE_NB]},
            {DEFAULT_POS: 45},
            {MAX_POS: 180}
        ]
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
    #ld.add_action(face_server_node)
    ld.add_action(lights_server_node)
    ld.add_action(relays_server_node)
    ld.add_action(system_server_node)
    ld.add_action(wheels_server_node)
    ld.add_action(neck_server_node)
    ld.add_action(left_arm_server_node)
    ld.add_action(right_arm_server_node)
    ld.add_action(left_eye_server_node)
    ld.add_action(right_eye_server_node)
    return ld