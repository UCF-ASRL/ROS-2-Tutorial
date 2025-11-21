# Imports
# For os path commands
import os

# Importing Model and world and launch files
from ament_index_python.packages import get_package_share_directory  # type: ignore

# Import Ros Launch
import launch_ros  # type: ignore
from launch_ros.actions import Node  # type: ignore
from launch_ros.substitutions import FindPackageShare  # type: ignore

# Core structure
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler  # type: ignore
from launch.event_handlers import OnProcessExit  # type: ignore
from launch.launch_description_sources import PythonLaunchDescriptionSource  # type: ignore
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution  # type: ignore

# Xacro
import xacro  # type: ignore

#----------------------------------------------------------------------------
# Launch
def generate_launch_description():

    # Names
    # Base Files
    package_name = 'asrl_tutorial'
    robot_name = 'rome_urdf'
    urdf_name = 'main.xacro'
    urdf_folder_name = 'model'
    rviz_param_file = 'rviz_config.rviz'

    # Paths
    path_to_urdf = os.path.join(get_package_share_directory(package_name),urdf_folder_name,urdf_name)
    path_to_rviz_params = os.path.join(get_package_share_directory(package_name),'config',rviz_param_file)

    # Robot Description
    robot_description = xacro.process_file(path_to_urdf).toxml()

    # Publishers
    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    # Joint State Publisher GUI
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )

    # RVIZ
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', path_to_rviz_params],
    )

    # Launch Description
    ld = LaunchDescription()

    # Add Launch Nodes
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_gui_node)
    ld.add_action(rviz_node)

    return ld
