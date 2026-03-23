import os

from ament_index_python import get_package_share_directory

import launch
from launch_ros.actions import Node

os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'
# Verbose log:
# os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message} '
# '({function_name}() at {file_name}:{line_number})'


# Start as node:
def generate_launch_description():


    config_dir = os.path.join(get_package_share_directory('camera_node'), 'config')
    yaml_file_path = os.path.join(config_dir, 'szocske.yaml')

    '''camera_E75894 = Node(
        name='camera_E75894',
        package='camera_aravis2',
        executable='camera_driver_uv',
        output='screen',
        emulate_tty=True,
        # arguments=['--ros-args', '--log-level', 'debug'],
        parameters=[
                {
                    # Driver-specific parameters
                    'guid': 'Point Grey Research-1E1000E75894-00E75894',
                    'frame_id': 'camera_uv',
                    'camera_info_urls': [yaml_file_path],
                    'verbose': True,

                    # GenICam-specific parameters
                    'ImageFormatControl': {
                        'PixelFormat': ['BayerRG8'],
                        'Width': 1920,
                        'Height': 1200
                    }
                }
            ]
    )'''

    camera_left = Node(
        name='camera_driver',
        namespace='left/camera_E7589C',
        package='camera_aravis2',
        executable='camera_driver_uv',
        output='screen',
        emulate_tty=True,
        # arguments=['--ros-args', '--log-level', 'debug'],
        parameters=[
                {
                    # Driver-specific parameters
                    'guid': 'Point Grey Research-1E1000E7589C-00E7589C',
                    'frame_id': 'camera_uv',
                    'camera_info_urls': [yaml_file_path],
                    'verbose': True,

                    # GenICam-specific parameters
                    'ImageFormatControl': {
                        'PixelFormat': ['BayerRG8'],
                        'Width': 1920,
                        'Height': 1200
                    }
                }
            ]
    )

    # BAL KAMERA RECTIFY NODE (Kiegyenesítés)
    rectify_left = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node_left',
        namespace='left/camera_E7589C',
        output='screen',
        # Az 'image' bemenetet rákötjük a nyers képre, a kimenet automatikusan 'image_rect' lesz
        remappings=[
            ('image', 'image_raw')
        ]
    )

    # JOBB KAMERA RECTIFY NODE (Kiegyenesítés)
    rectify_right = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node_right',
        namespace='right/camera_E7588B',
        output='screen',
        remappings=[
            ('image', 'image_raw')
        ]
    )

    camera_right = Node(
        name='camera_driver',
        namespace='right/camera_E7588B',
        package='camera_aravis2',
        executable='camera_driver_uv',
        output='screen',
        emulate_tty=True,
        # arguments=['--ros-args', '--log-level', 'debug'],
        parameters=[
                {
                    # Driver-specific parameters
                    'guid': 'Point Grey Research-1E1000E7588B-00E7588B',
                    'frame_id': 'camera_uv',
                    'camera_info_urls': [yaml_file_path],
                    'verbose': True,

                    # GenICam-specific parameters
                    'ImageFormatControl': {
                        'PixelFormat': ['BayerRG8'],
                        'Width': 1920,
                        'Height': 1200
                    }
                }
            ]
    )

    # A stereo_image_proc most már az új névterekről olvassa az adatokat
    stereo_disparity = Node(
        package='stereo_image_proc',
        executable='disparity_node',
        output='screen',
        parameters=[{'approximate_sync': True}],
        # Újra kell mappolnunk, hogy a node megtalálja az egyedi nevű kamerákat
        remappings=[
            ('left/image_rect', '/left/camera_E7589C/image_rect'),
            ('left/camera_info', '/left/camera_E7589C/camera_info'),
            ('right/image_rect', '/right/camera_E7588B/image_rect'),
            ('right/camera_info', '/right/camera_E7588B/camera_info')
        ]
    )

    # recorder ( ez veszi fel a topicokat csak a recorder az angolul furulya es az vicces )
    furulya = launch.actions.ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', 'test', '--all', '--compression-mode', 'file', '--compression-format', 'zstd', '--storage', 'mcap'],
        output='screen'
    )
    
    return launch.LaunchDescription([ camera_left, camera_right])