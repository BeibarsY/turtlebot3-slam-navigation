"""
labyrinth_world.launch.py

Open Gazebo Classic with the custom labyrinth world and spawn a
TurtleBot3 Burger at a configurable initial pose.

Tested on ROS 2 Humble + Ubuntu 22.04 with the standard apt packages
ros-humble-turtlebot3-gazebo and ros-humble-gazebo-ros-pkgs installed.

Usage:
    export TURTLEBOT3_MODEL=burger
    export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:<path-to-repo>/gazebo/models
    ros2 launch labyrinth_world.launch.py

Optional spawn arguments:
    x_pose:=-2.0  y_pose:=-0.5  yaw_pose:=0.0

The spawn pose must be inside the free space of the labyrinth or
gmapping cannot bootstrap.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # ------------------------------------------------------------
    # Resolve the path to this repository's worlds directory.
    # We assume this launch file is run from inside the repo, so we
    # walk up two levels (launch/ -> repo root) and then into gazebo/worlds.
    # ------------------------------------------------------------
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    world_path = os.path.join(pkg_dir, 'gazebo', 'worlds', 'labyrinth.world')

    # ------------------------------------------------------------
    # Spawn-pose launch arguments. Defaults were chosen so the robot
    # lands in an open corridor of our maze; override them on the
    # command line if you use a different STL mesh.
    # ------------------------------------------------------------
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='-0.5')
    yaw_pose = LaunchConfiguration('yaw_pose', default='0.0')

    declare_x = DeclareLaunchArgument('x_pose', default_value='-2.0',
                                     description='Initial robot x in world frame')
    declare_y = DeclareLaunchArgument('y_pose', default_value='-0.5',
                                     description='Initial robot y in world frame')
    declare_yaw = DeclareLaunchArgument('yaw_pose', default_value='0.0',
                                       description='Initial yaw (radians)')

    # ------------------------------------------------------------
    # Launch Gazebo Classic server + client with our world.
    # ------------------------------------------------------------
    gazebo_ros = get_package_share_directory('gazebo_ros')
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_path}.items(),
    )
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
    )

    # ------------------------------------------------------------
    # robot_state_publisher: provides TF tree from the TurtleBot3 URDF
    # so that SLAM and RViz see the chassis, wheels, and LiDAR frame.
    # ------------------------------------------------------------
    tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    robot_state_pub = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items(),
    )

    # ------------------------------------------------------------
    # Spawn TurtleBot3 model into the running Gazebo world.
    # We reuse the spawn helper shipped with turtlebot3_gazebo.
    # ------------------------------------------------------------
    spawn_tb3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo, 'launch', 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
        }.items(),
    )

    return LaunchDescription([
        declare_x,
        declare_y,
        declare_yaw,
        gzserver,
        gzclient,
        robot_state_pub,
        spawn_tb3,
    ])
