# Code for terminal
- source devel/setup.bash
- roscore
- rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200
- roslaunch mums_assistant test.launch
- rosrun mums_assistant testcode.py
- rosrun mums_assistant joint_servo_publisher_test.py
- rosrun mums_assistant joint_servo_subscriber_test.py
