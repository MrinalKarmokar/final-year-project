#!/usr/bin/env python3
""" This is to test if message is being published """
import rospy
from std_msgs.msg import Float32MultiArray
from mums_assistant.msg import Dofs

# ------------------------------------------------------------------------------------

def callback_arm(data):
    rospy.loginfo('\033[94m' + f"Published ARM Data >>> Arduino: {data.data}" + '\033[0m')

def joint_servo_arm_listener():
    rospy.Subscriber("/joint_servo_arm_topic", Float32MultiArray, callback_arm)

# ------------------------------------------------------------------------------------

def callback_gripper(data):
    rospy.loginfo('\033[94m' + f"Published GRIPPER Data >>> Arduino: {data.data}" + '\033[0m')

def joint_servo_gripper_listener():
    rospy.Subscriber("/joint_servo_gripper_topic", Float32MultiArray, callback_gripper)

# ------------------------------------------------------------------------------------

def callback_rviz_arm(data):
    rospy.loginfo('\033[94m' + f"Publisher from RVIZ >>> Arm: {data.data}" + '\033[0m')

def joint_servo_rviz_arm_listener():
    rospy.Subscriber("/joint_servo_arm_rviz_topic", Float32MultiArray, callback_rviz_arm)

# ------------------------------------------------------------------------------------

def callback_rviz_gripper(data):
    rospy.loginfo('\033[94m' + f"Publisher from RVIZ >>> Gripper: \n{data.data}" + '\033[0m')

def joint_servo_rviz_gripper_listener():
    rospy.Subscriber("/joint_servo_gripper_rviz_topic", Float32MultiArray, callback_rviz_gripper)

# ------------------------------------------------------------------------------------

def cb(data):
    rospy.loginfo('\033[94m' + f"Publisher from DOFS >>> Arm: {data}" + '\033[0m')

def joint_state_pub_listener():
    rospy.Subscriber("/arm_dofs", Dofs, cb)

# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    rospy.init_node('joint_servo_listener', anonymous=True)
    # joint_servo_arm_listener()
    # joint_servo_gripper_listener()
    # joint_servo_rviz_arm_listener()
    # joint_servo_rviz_gripper_listener()
    joint_state_pub_listener()
    rospy.spin()