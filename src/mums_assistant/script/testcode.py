#! /usr/bin/env python3

import copy
import math
import sys

import actionlib
import geometry_msgs.msg
import moveit_commander
import moveit_msgs.msg
import rospy
from rospy.exceptions import ROSInitException

from testcode2 import MumsAssistantGripper

class MumsAssistantArm:

    # Constructor
    def __init__(self):

        rospy.init_node('node_planning', anonymous=True)

        self._planning_group = "arm_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        self._display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

        self._exectute_trajectory_client = actionlib.SimpleActionClient(
            'execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()


        rospy.loginfo('\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo('\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo('\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo('\033[94m' + " >>> Mum's Assistant Arm init done." + '\033[0m')


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

    lst_joint_angles_a = [math.radians(0),
                        math.radians(0),
                        math.radians(0),
                        math.radians(0),
                        math.radians(40)]

    lst_joint_angles_g = [math.radians(-40),
                          math.radians(-40)]

    while not rospy.is_shutdown():
        rospy.sleep(5)
        maa.set_joint_angles(lst_joint_angles_a)

        rospy.sleep(2)
        mag.set_joint_angles(lst_joint_angles_g)

    del maa


if __name__ == '__main__':
    try:
        main()
    except ROSInitException as e:
        print(e)