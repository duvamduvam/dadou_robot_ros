"""Validation structurelle de l'URDF (généré depuis le xacro).

Garantit que le modèle reste chargeable (RViz/Gazebo) et que les joints
portent les noms attendus par le code robot (neck, left_arm, ...).
"""

import os
import xml.etree.ElementTree as ET

import pytest
import xacro

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
XACRO_PATH = os.path.join(REPO_ROOT, "conf", "ros2_dependencies", "robot_description",
                          "urdf", "dadou_robot.urdf.xacro")

SERVO_JOINTS = {"neck", "left_arm", "right_arm", "left_eye", "right_eye"}
WHEEL_JOINTS = {"wheel_left_joint", "wheel_right_joint"}


@pytest.fixture(scope="module")
def urdf():
    return ET.fromstring(xacro.process_file(XACRO_PATH).toxml())


def test_xacro_generates_valid_urdf(urdf):
    assert urdf.tag == "robot"
    assert urdf.get("name") == "dadou_robot"


def test_joints_reference_existing_links(urdf):
    links = {l.get("name") for l in urdf.findall("link")}
    for joint in urdf.findall("joint"):
        parent = joint.find("parent").get("link")
        child = joint.find("child").get("link")
        assert parent in links, "joint {} : parent {} inconnu".format(joint.get("name"), parent)
        assert child in links, "joint {} : child {} inconnu".format(joint.get("name"), child)


def test_tree_has_single_root(urdf):
    links = {l.get("name") for l in urdf.findall("link")}
    children = {j.find("child").get("link") for j in urdf.findall("joint")}
    roots = links - children
    assert roots == {"base_link"}, "racines de l'arbre : {}".format(roots)


def test_servo_joints_exist_with_limits(urdf):
    joints = {j.get("name"): j for j in urdf.findall("joint")}
    assert SERVO_JOINTS <= set(joints), "joints servo manquants : {}".format(SERVO_JOINTS - set(joints))
    for name in SERVO_JOINTS:
        joint = joints[name]
        assert joint.get("type") == "revolute"
        limit = joint.find("limit")
        assert limit is not None and float(limit.get("lower")) < float(limit.get("upper"))


def test_wheel_joints_are_continuous(urdf):
    joints = {j.get("name"): j for j in urdf.findall("joint")}
    for name in WHEEL_JOINTS:
        assert joints[name].get("type") == "continuous"


def test_links_have_positive_mass(urdf):
    for link in urdf.findall("link"):
        inertial = link.find("inertial")
        if inertial is not None:
            assert float(inertial.find("mass").get("value")) > 0, link.get("name")
