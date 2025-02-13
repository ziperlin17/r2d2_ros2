import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_share = get_package_share_directory('r2d2_sim')
    world_path = os.path.join(pkg_share, 'models', 'r2d2models', 'model.sdf')
    xacro_path = os.path.join(pkg_share, 'models', 'r2d2models', 'r2d2.xacro.urdf')
    control_config = os.path.join(pkg_share, 'config', 'diff_drive_controller.yaml')
    config_dir = os.path.join(pkg_share, 'config')
    
    doc = xacro.process_file(
        xacro_path,
        mappings={'config_dir': config_dir} 
    )
    robot_description = doc.toxml()

    return LaunchDescription([
    
        SetEnvironmentVariable(
            name='GZ_SIM_SYSTEM_PLUGIN_PATH',
            value=os.environ.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '') + ':/opt/ros/jazzy/lib'
        ),

        ExecuteProcess(
            cmd=[
                'gz', 'sim',
                '-r',                      
                '--render-engine', 'ogre', 
                world_path
            ],
            output='screen'
        ),

        TimerAction(
            period=0.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'run', 'ros_gz_sim', 'create',
                        '-string', robot_description, 
                        '-name', 'r2d2',
                        '-z', '0.5'
                    ],
                    output='screen'
                )
            ]
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
            ],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        TimerAction(
            period=8.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'run', 'controller_manager', 'spawner',
                        'joint_state_broadcaster',
                        '--controller-manager', '/controller_manager',
                        '--param-file', control_config
                    ],
                    output='screen'
                )
            ]
        ),

        TimerAction(
            period=10.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'run', 'controller_manager', 'spawner',
                        'diff_drive_controller',
                        '--controller-manager', '/controller_manager',
                        '--param-file', control_config
                    ],
                    output='screen'
                )
            ]
        ),
    ])
