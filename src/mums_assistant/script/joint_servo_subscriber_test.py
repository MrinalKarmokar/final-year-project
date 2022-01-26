#!/usr/bin/env python3
""" This is to test if message is being published """
import rospy
from std_msgs.msg import Float32MultiArray

def callback(data):
    rospy.loginfo('\033[94m' + f"Published Data -> Arduino: {data.data}" + '\033[0m')

def joint_servo_listener():

    rospy.init_node('joint_servo_listener', anonymous=True)

    rospy.Subscriber("/joint_servo_topic", Float32MultiArray, callback)

    rospy.spin()

if __name__ == '__main__':
    joint_servo_listener()
