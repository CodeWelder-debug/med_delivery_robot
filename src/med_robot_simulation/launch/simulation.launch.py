import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('med_robot_simulation')
    
    # File Paths
    world_path = os.path.join(pkg_share, 'worlds', 'hospital_world.sdf')
    urdf_path = os.path.join(pkg_share, 'urdf', 'med_delivery_robot.urdf')
    bridge_config_path = os.path.join(pkg_share, 'config', 'ros_gz_bridge.yaml')
    
    # Read URDF Content
    with open(urdf_path, 'r') as f:
        robot_desc = f.read()

    # 1. Set Gazebo Resource Path
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[pkg_share, ':', os.path.join(pkg_share, 'meshes')]
    )

    # 2. Launch Gazebo Sim with World
    start_gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # 3. Publish Robot State / Transforms (TF)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }]
    )

    # 4. Spawn Robot into Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-string', robot_desc,
            '-name', 'med_delivery_robot',
            '-x', '-11.5',
            '-y', '1.5',
            '-z', '0.1'
        ],
        output='screen'
    )

    # 5. Launch Topic Bridge (Translates ROS 2 <-> Gazebo messages)
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_path,
            'use_sim_time': True
        }],
        output='screen'
    )

    return LaunchDescription([
        set_gz_resource_path,
        start_gazebo,
        robot_state_publisher,
        spawn_robot,
        ros_gz_bridge
    ])
