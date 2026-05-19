#!/usr/bin/env bash
#
# slam_mapping_sim.sh
#
# Convenience launcher for SLAM-based map building in the custom
# labyrinth Gazebo world. Opens three terminals (using gnome-terminal;
# substitute for your terminal of choice as needed):
#
#   1. Gazebo + labyrinth world + TurtleBot3
#   2. slam_toolbox (online async SLAM)
#   3. teleop_keyboard
#
# When the map is fully built, save it from a fourth shell with:
#   ros2 run nav2_map_server map_saver_cli -f maps/labyrinth_sim
#
# Tested on Ubuntu 22.04 + ROS 2 Humble.

set -euo pipefail

# Resolve repo root from the script location.
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Make our custom labyrinth model visible to Gazebo.
export GAZEBO_MODEL_PATH="${GAZEBO_MODEL_PATH:-}:${REPO_ROOT}/gazebo/models"
export TURTLEBOT3_MODEL=burger

# Open the three required processes in separate terminals so each can
# be inspected / stopped independently.
gnome-terminal --tab --title="Gazebo+World" -- bash -c \
    "source /opt/ros/humble/setup.bash && \
     ros2 launch ${REPO_ROOT}/launch/labyrinth_world.launch.py; exec bash"

sleep 5  # give Gazebo time to come up before SLAM subscribes to /scan

gnome-terminal --tab --title="SLAM" -- bash -c \
    "source /opt/ros/humble/setup.bash && \
     ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true; exec bash"

sleep 2

gnome-terminal --tab --title="Teleop" -- bash -c \
    "source /opt/ros/humble/setup.bash && \
     export TURTLEBOT3_MODEL=burger && \
     ros2 run turtlebot3_teleop teleop_keyboard; exec bash"

cat <<EOF

Three terminals launched.

When the map is complete, save it with:

  cd ${REPO_ROOT}
  ros2 run nav2_map_server map_saver_cli -f maps/labyrinth_sim

This writes maps/labyrinth_sim.pgm and maps/labyrinth_sim.yaml.

EOF
