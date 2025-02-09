from setuptools import find_packages, setup

package_name = 'r2d2_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/r2d2.launch.py']),
        ('share/' + package_name + '/models/r2d2models', ['models/r2d2models/model.sdf']),
        ('share/' + package_name + '/models/r2d2models', ['models/r2d2models/r2d2.sdf']),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='',
    maintainer_email='',
    description='r2d2',
    license='',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 
        ],
    },
)
