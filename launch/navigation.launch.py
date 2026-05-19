"""
navigation.launch.py

Bring up the ROS 2 Nav2 stack on a pre-built map of the labyrinth,
using the tuned nav2_params.yaml from this repository.

This launches everything from the official TurtleBot3 Nav2 bringup
launch file, but overrides the params file and map file with our
tuned versions.

Tested on ROS 2 Humble. Assumes ros-humble-nav2-bringup and
ros-humble-turtlebot3-navigation2 are installed.

Usage:
    export TURTLEBOT3_MODEL=burger
    ros2 launch navigation.launch.py
    ros2 launch navigation.launch.py map:=maps/labyrinth_real.yaml

Optional arguments:
    map:=<path>        path to a *.yaml map file (default: maps/labyrinth_sim.yaml)
    use_sim_time:=true if running against Gazebo, false on real robot
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    default_map = os.path.join(pkg_dir, 'maps', 'labyrinth_sim.yaml')
    params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    map_arg = DeclareLaunchArgument(
        'map',
        default_value=default_map,
        description='Path to map YAML for the labyrinth (sim or real).',
    )
    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock from Gazebo (true) or real time (false).',
    )

    # Reuse the official TurtleBot3 navigation2 launch and override
    # params + map. This keeps RViz config, AMCL, and recovery
    # behaviors exactly as the official tutorial expects, while still
    # picking up our tuned numbers from config/nav2_params.yaml.
    tb3_nav2 = get_package_share_directory('turtlebot3_navigation2')
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_nav2, 'launch', 'navigation2.launch.py')
        ),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'map': LaunchConfiguration('map'),
            'params_file': params_file,
        }.items(),
    )

    return LaunchDescription([
        map_arg,
        sim_time_arg,
        nav2_launch,
    ])
