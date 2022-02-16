#! /usr/bin/env python3

import math
import sys

import actionlib
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Float32MultiArray
import rospy

from testcode2 import MumsAssistantGripper

class MumsAssistantArm:

    # Constructor
    def __init__(self):

        rospy.init_node('node_planning_arm', anonymous=True)

        self._planning_group = "arm_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        self._display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)
        self.pub = rospy.Publisher("/joint_servo_topic", Float32MultiArray, queue_size=10)

        self._exectute_trajectory_client = actionlib.SimpleActionClient(
            'execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()
        self._box_name = ''

        rospy.loginfo('\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo('\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo('\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo('\033[94m' + " >>> Mum's Assistant Arm init done." + '\033[0m')

    def joint_servo_talker(self, list_joint_values):

        data_to_send = Float32MultiArray(data=list_joint_values)  # the data to be sent, initialise the array
        rospy.loginfo('\033[94m' + f">>> Joint Servo Talker: {data_to_send.data}" + '\033[0m')
        self.pub.publish(data_to_send)

    def set_joint_angles(self, arg_list_joint_angles):

        list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo('\033[94m' + ">>> Current Joint Values:" + '\033[0m')
        rospy.loginfo(list_joint_values)

        self._group.set_joint_value_target(arg_list_joint_angles)
        self._group.plan()
        flag_plan = self._group.go(wait=True)

        list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo('\033[94m' + ">>> Final Joint Values:" + '\033[0m')
        rospy.loginfo(list_joint_values)

        pose_values = self._group.get_current_pose().pose
        rospy.loginfo('\033[94m' + ">>> Final Pose:" + '\033[0m')
        rospy.loginfo(pose_values)

        if (flag_plan == True):
            rospy.loginfo(
                '\033[94m' + ">>> set_joint_angles() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> set_joint_angles() Failed." + '\033[0m')

        return flag_plan

    # Destructor

    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Mum's Assistant Arm Deleted." + '\033[0m')


def main():

    maa = MumsAssistantArm()
    mag = MumsAssistantGripper()

    lst_servo_zeros = [0,0,0,0,0]

    lst_joint_angles_a = [math.radians(0),
                        math.radians(0),
                        math.radians(0),
                        math.radians(0),
                        math.radians(0)]

    # this is list published to Arduino to control servo
    lst_joint_angles_servo = [150,0,0,0,0]


    lst_joint_angles_g = [math.radians(-40),
                          math.radians(-40)]

    lst_joint_angles_gc = [math.radians(-1),
                          math.radians(-1)]

    maa.joint_servo_talker(lst_servo_zeros)
    rospy.sleep(5)
    rospy.loginfo('\033[94m' + ">>> Arm Moving" + '\033[0m')
    maa.set_joint_angles(lst_joint_angles_a)            #function for showing movement in Rviz and Gazebo
    maa.joint_servo_talker(lst_joint_angles_servo)      #function to publish data to arduino

    # rospy.sleep(2)
    # rospy.loginfo('\033[94m' + ">>> Gripper Opening" + '\033[0m')
    # mag.go_to_predefined_pose("gripper_open")
    # mag.set_joint_angles(lst_joint_angles_g)

    # rospy.sleep(2)
    # rospy.loginfo('\033[94m' + ">>> Gripper Closing" + '\033[0m')
    # mag.go_to_predefined_pose("gripper_close")

    # rospy.loginfo('\033[94m' + ">>> ADD BOX" + '\033[0m')
    # mag.add_box()

    # rospy.loginfo('\033[94m' + ">>> ATTACH BOX" + '\033[0m')
    # mag.attach_box()
    # mag.set_joint_angles(lst_joint_angles_gc)

    rospy.spin()

    del maa
    del mag


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)