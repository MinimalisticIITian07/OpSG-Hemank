from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_first_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hemank',
    maintainer_email='hemank@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drone_publisher = my_first_package.drone_publisher:main',
            'target_subscriber = my_first_package.target_subscriber:main',
            'drone_service = my_first_package.drone_service:main',
            'drone_client = my_first_package.drone_client:main',
            'takeoff_and_land = my_first_package.takeoff_and_land:main',
            'square_flight = my_first_package.square_flight:main',
            'figure8_flight = my_first_package.figure8_flight:main',
            'camera_viewer = my_first_package.camera_viewer:main',
            'triangle_flight = my_first_package.triangle_flight:main'
        ],
    },
)
