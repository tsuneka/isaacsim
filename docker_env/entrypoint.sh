#!/bin/bash
set -e

source /opt/ros/$ROS_DISTRO/setup.bash --extend
source /home/$USERNAME/ws/IsaacSim-ros_workspaces/humble_ws/install/setup.bash --extend

exec "$@"