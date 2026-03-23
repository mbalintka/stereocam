import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch_ros.actions import Node

os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time}: [{name}] [{severity}]\t{message}'

def generate_launch_description():

    config_dir = os.path.join(get_package_share_directory('camera_node'), 'config')
    left_yaml_path = os.path.join(config_dir, 'szocske_left.yaml')
    right_yaml_path = os.path.join(config_dir, 'szocske_right.yaml')

    # BAL KAMERA DRIVER
    camera_left = Node(
        name='camera_driver',
        namespace='left/camera_E7589C',
        package='camera_aravis2',
        executable='camera_driver_uv',
        output='screen',
        emulate_tty=True,
        parameters=[
                {
                    'guid': 'Point Grey Research-1E1000E7589C-00E7589C', 
                    'frame_id': 'camera_left_optical_frame',
                    'camera_info_urls': [left_yaml_path],
                    'verbose': True,
                    # fps cap
                    'AcquisitionControl': {
                        'AcquisitionFrameRateEnable': True,
                        'AcquisitionFrameRate': 15.0
                    },
                    'ImageFormatControl': {
                        'PixelFormat': ['Mono8'],
                        'BinningHorizontal': 2,
                        'BinningVertical': 2,
                        'Width': 960,
                        'Height': 600
                    }
                }
            ]
    )

    # BAL KAMERA RECTIFY NODE (Abszolút útvonalakkal)
    rectify_left = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node_left',
        output='screen',
        remappings=[
            ('image', '/left/camera_E7589C/camera_driver/image_raw'),
            ('camera_info', '/left/camera_E7589C/camera_driver/camera_info'),
            ('image_rect', '/left/camera_E7589C/camera_driver/image_rect')
        ]
    )

    # JOBB KAMERA DRIVER
    camera_right = Node(
        name='camera_driver',
        namespace='right/camera_E7588B',
        package='camera_aravis2',
        executable='camera_driver_uv',
        output='screen',
        emulate_tty=True,
        parameters=[
                {
                    'guid': 'Point Grey Research-1E1000E7588B-00E7588B',
                    'frame_id': 'camera_right_optical_frame',
                    'camera_info_urls': [right_yaml_path],
                    'verbose': True,
                    # fps cap
                    'AcquisitionControl': {
                        'AcquisitionFrameRateEnable': True,
                        'AcquisitionFrameRate': 15.0
                    },
                   'ImageFormatControl': {
                        'PixelFormat': ['Mono8'],
                        'BinningHorizontal': 2,
                        'BinningVertical': 2,
                        'Width': 960,
                        'Height': 600
                    }
                }
            ]
    )

    # JOBB KAMERA RECTIFY NODE (Abszolút útvonalakkal)
    rectify_right = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node_right',
        output='screen',
        remappings=[
            ('image', '/right/camera_E7588B/camera_driver/image_raw'),
            ('camera_info', '/right/camera_E7588B/camera_driver/camera_info'),
            ('image_rect', '/right/camera_E7588B/camera_driver/image_rect')
        ]
    )

    # STEREO DISZPARITÁS FELDOLGOZÓ (Abszolút útvonalakkal)
    stereo_disparity = Node(
        package='stereo_image_proc',
        executable='disparity_node',
        output='screen',
        parameters=[{
            'approximate_sync': True,
            'queue_size': 5,
            # EZEKET A BEÁLLÍTÁSOKAT ADJUK HOZZÁ A GYORSÍTÁSHOZ:
            'stereo_algorithm': 0,          # 0 = Block Matching (A leggyorsabb algoritmus)
            'disparity_range': 32,          # Csak 32 pixelnyit keres, nem 128-at! (Nagy CPU tehermentesítés)
            'correlation_window_size': 11,  # Kisebb ablakméret a gyorsabb egyeztetésért
            'texture_threshold': 10         # A homogén (pl. sima fehér fal) részeket hamarabb átugorja
        }],
        remappings=[
            ('left/image_rect', '/left/camera_E7589C/camera_driver/image_rect'),
            ('left/camera_info', '/left/camera_E7589C/camera_driver/camera_info'),
            ('right/image_rect', '/right/camera_E7588B/camera_driver/image_rect'),
            ('right/camera_info', '/right/camera_E7588B/camera_driver/camera_info')
        ]
    )

    furulya = launch.actions.ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', 'test', '--all', '--compression-mode', 'file', '--compression-format', 'zstd', '--storage', 'mcap'],
        output='screen'
    )
    
    return launch.LaunchDescription([
        camera_left, 
        rectify_left, 
        camera_right, 
        rectify_right, 
        stereo_disparity, 
        furulya
    ])