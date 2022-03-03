# Requirements:
- Ubuntu 20.04 LTS
- ROS noetic (Desktop Full)
  - follow installion steps here : https://wiki.ros.org/noetic/Installation/Ubuntu
- SolidWorks
  - Install SolidWorks to URDF exporter : https://wiki.ros.org/sw_urdf_exporter/Tutorials/Export%20an%20Assembly
- VSCode/Pycharm as code editor

![Gazebo and Rviz Simultaneously](media/images/gazebo_rviz_model_grasp.png?raw=true "Robot Model")

### Robot Model designed by _HowToMechatronics_
Model Download link: https://thangs.com/m/38899

# Create ROS Workspace
    $ mkdir -p ~/ros_ws/catkin_ws/src
    $ cd ~/ros_ws/catkin_ws/
    $ catkin build
(if error encountered while catkin build, refer : https://answers.ros.org/question/353113/catkin-build-in-ubuntu-2004-noetic)

**ROS Tutorials : https://wiki.ros.org/ROS/Tutorials**

### Create package
    # catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
    
    $ cd ~/ros_ws/catkin_ws/src
    $ catkin_create_pkg mums_assistant std_msgs rospy roscpp

### URDF
Link

    <link name="link_1">
        <inertial>
            <origin xyz="0.001372 0.0064346 0.017289" rpy="0 0 0" />
            <mass value="0.068038" />
            <inertia ixx="4.5018E-05" ixy="-6.4176E-07" ixz="-6.2428E-06" iyy="5.8133E-05" iyz="-5.1777E-06" izz="5.4676E-05" />
        </inertial>
    
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <mesh filename="package://mums_assistant/meshes/link_1.STL" />
            </geometry>
            <material name="">
                <color rgba="0.79216 0.81961 0.93333 1" />
            </material>
        </visual>
        <collision>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <mesh filename="package://mums_assistant/meshes/link_1.STL" />
            </geometry>
        </collision>
    </link>

Joint

    <joint name="joint_1" type="revolute">
        <origin xyz="0 0 0.056" rpy="0 0 0" />
        <parent link="base_link" />
        <child link="link_1" />
        <axis xyz="0 0 1" />
        <limit lower="-1.57" upper="1.57" effort="0.92" velocity="6.16" />
        <dynamics damping="0" friction="0" />
    </joint>

### Package created using 'Moveit Setup Assistant'

- Launch Moveit Setup Assistant
  - `$ roslaunch moveit_setup_assistant setup_assistant.launch`
- Create New Moveit Configuration Package
  - Load URDF
- Self-Collisions
  - Click **Generate Collision Matrix**
- Planning Groups
  - < ADD IMAGE HERE >
- Robot Poses
  - rest pose : all arm joint angle = [0 0 0 0 0]
  - gripper_close : gripper joint = [0 0]
  - gripper_open : gripper joint = [-1 -1]
- End Effector
  - < ADD IMAGE HERE >
- Controllers
  - Auto Add FollowJointTrajectory Controllers for each Planning Group
  - **Add Controller** : position_controllers/JointTrajectoryController to each Planning Group

# Code for terminal
- $ source devel/setup.bash
- $ roscore
- $ rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200
- $ roslaunch mums_assistant test.launch
- $ rosrun mums_assistant testcode.py
- $ rosrun mums_assistant joint_servo_publisher_test.py
- $ rosrun mums_assistant joint_servo_subscriber_test.py
