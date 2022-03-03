# Requirements:
- Ubuntu 20.04 LTS
- ROS noetic (Desktop Full)
  - follow installation steps here : https://wiki.ros.org/noetic/Installation/Ubuntu
- SolidWorks
  - Install SolidWorks to URDF exporter : https://wiki.ros.org/sw_urdf_exporter/Tutorials/Export%20an%20Assembly
- VSCode/Pycharm and Arduino IDE

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
  - **Generate Collision Matrix**
- Planning Groups
  - <img src="media/images/planning_group.png" width="60%">
- Robot Poses
  - rest pose : all arm joint angle = [0 0 0 0 0]
  - gripper_close : gripper joint = [0 0]
  - gripper_open : gripper joint = [-1 -1]
- End Effector
  - <img src="media/images/end_effector.png" width="60%">
- Controllers
  - <img src="media/images/setup_controllers.png" width="60%">
- Save package as : `mums_assistant_config`

# World
- Kitchen model in world file

      <model name='kitchen'>
        <static>1</static>
          <link name='kitchen'>
            <visual name='visual'>
               <geometry>
                  <mesh>
                    <uri>model://Kitchen/meshes/model.dae</uri>
                    <scale>0.5 0.5 0.5</scale>
                  </mesh>
               </geometry>
            </visual>
            <self_collide>0</self_collide>
            <enable_wind>0</enable_wind>
            <kinematic>0</kinematic>
          </link>
        <pose>-0.804049 0.532603 0 0 -0 0</pose>
      </model>

# Simulation
https://user-images.githubusercontent.com/42796209/156630172-7028c14f-a111-45b8-9cae-e2dcd7bb42e3.mp4

---

# 3D Printing Parts

| 1                                                           | 2                                                           | 3                                                           |
|-------------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------|
| ![3D Printed Parts](media/images/3d_printed_2.jpg?raw=true) | ![3D Printed Parts](media/images/3d_printed_3.jpg?raw=true) | ![3D Printed Parts](media/images/3d_printed_4.jpg?raw=true) |

---
# Code for terminal
- $ source devel/setup.bash
- $ roscore
- $ rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0 _baud:=115200
- $ roslaunch mums_assistant test.launch
- $ rosrun mums_assistant testcode.py
- $ rosrun mums_assistant joint_servo_publisher_test.py
- $ rosrun mums_assistant joint_servo_subscriber_test.py
