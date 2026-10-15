import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    pkg_dir = get_package_share_directory('med_robot_simulation')
    
    params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # 1. Launch Nav2 navigation servers (Planner, Controller, BT Navigator) without map_server/amcl
    nav2_navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': 'true'
        }.items()
    )

    # 2. Launch slam_toolbox to map dynamically and manage map -> odom transform
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': params_file
        }.items()
    )

    return LaunchDescription([
        nav2_navigation_launch,
        slam_toolbox_launch
    ])
