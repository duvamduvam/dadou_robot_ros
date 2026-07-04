import os
import sys

# La racine du dépôt donne accès au package robot/ et, via le symlink
# dadou_utils_ros -> ../dadou_utils_ros, à la lib partagée.
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# robot_drive n'est pas un package installé (pas de colcon build sur l'hôte
# de dev) : on l'ajoute au path pour que les tests fassent
# `from robot_drive... import ...` comme si le package était sourcé.
sys.path.insert(0, os.path.join(ROOT, "conf", "ros2_dependencies", "robot_drive"))
