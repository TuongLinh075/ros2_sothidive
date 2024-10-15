import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    package_name = 'car_3_wheel'
    pkg_share = FindPackageShare(package=package_name).find(package_name)

    robot_name_in_model = 'ver6'
    urdf_file_name = 'ver6.urdf'
    urdf_path = os.path.join(pkg_share, 'urdf', urdf_file_name)

    # world_file_name = 'world.world'
    # world_path = os.path.join(pkg_share, 'worlds', world_file_name)

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    robot_description = {"robot_description": robot_desc}

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
    )
    # declare_world_cmd = DeclareLaunchArgument(
    #     name='world',
    #     default_value=world_path,
    # )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description", 
                   "-entity", robot_name_in_model,
                   "-x", '0.0',
                   "-y", '0.0',
                   "-z", '0.05',
                   "-Y", '0.0'],
    )

    # Node trang thái
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
    )

    # Node trang thai khop
    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        name='joint_state_publisher',
    )

    # rviz2 = Node(
    #     package='rviz2',    
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     parameters=[{'use_sim_time': use_sim_time}]
    # )
    
    # ,LaunchConfiguration('world')
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 
        'libgazebo_ros_init.so',],
        output='screen',
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        # declare_world_cmd,
        spawn_robot,
        start_joint_state_publisher_cmd,
        robot_state_publisher_node,
        gazebo,
        # rviz2,
    ])
