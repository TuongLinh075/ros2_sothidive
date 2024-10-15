# ros2_sothidive
# create packages
ros2 pkg create --build-type ament_python --license Apache-2.0 <package_name>
# build
colcon build --packages-select my_package
source install/local_setup.bash
