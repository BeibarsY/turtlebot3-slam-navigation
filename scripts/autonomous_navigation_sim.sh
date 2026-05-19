#!/usr/bin/env bash
#
# autonomous_navigation_sim.sh
#
# Convenience launcher for running autonomous Nav2 navigation on the
# previously-built map of the labyrinth.
#
# Prerequisites:
#   - maps/labyrinth_sim.yaml exists (run slam_mapping_sim.sh first).
#   - turtlebot3_navigation2 and nav2_bringup are installed.
#
# Workflow once everything is up:
#   1. In RViz, click "2D Pose Estimate" and click+drag at the robot's
#      true starting pose. The AMCL particle cloud should collapse
#      around the robot.
#   2. Optionally drive a few seconds with teleop so AMCL converges.
#   3. Click "Nav2 Goal" in RViz and click anywhere on the map; the
#      robot will plan and drive autonomously.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

export GAZEBO_MODEL_PATH="${GAZEBO_MODEL_PATH:-}:${REPO_ROOT}/gazebo/models"
export TURTLEBOT3_MODEL=burger

# Tab 1: Gazebo + world + robot
gnome-terminal --tab --title="Gazebo+World" -- bash -c \
    "source /opt/ros/humble/setup.bash && \
     ros2 launch ${REPO_ROOT}/launch/labyrinth_world.launch.py; exec bash"

sleep 5

# Tab 2: Nav2 stack with our tuned params and the saved map
gnome-terminal --tab --title="Nav2" -- bash -c \
    "source /opt/ros/humble/setup.bash && \
     ros2 launch ${REPO_ROOT}/launch/navigation.launch.py \
         map:=${REPO_ROOT}/maps/labyrinth_sim.yaml \
         use_sim_time:=true; exec bash"

cat <<EOF

Two terminals launched. In RViz:
  - Use "2D Pose Estimate" to set the initial pose.
  - Use "Nav2 Goal" to send the robot to any point.

EOF
