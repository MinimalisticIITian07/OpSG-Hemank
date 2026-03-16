from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Start the publisher node
        Node(
            package='my_first_package',
            executable='drone_publisher',
            name='drone_publisher'
        ),
        # Start the subscriber node
        Node(
            package='my_first_package',
            executable='target_subscriber',
            name='target_subscriber'
        )
    ])
