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
        self.pub = rospy.Publisher("/joint_servo_arm_topic", Float32MultiArray, queue_size=10)

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

    def joint_servo_arm_talker(self, list_joint_values):

        data_to_send = Float32MultiArray(data=list_joint_values)  # the data to be sent, initialise the array
        rospy.loginfo('\033[94m' + f">>> Joint Servo Arm Talker: {data_to_send.data}" + '\033[0m')
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

    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')

    # Destructor

    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Mum's Assistant Arm Deleted." + '\033[0m')


def main():

    maa = MumsAssistantArm()
    mag = MumsAssistantGripper()

    rest = [math.radians(0),
            math.radians(0),
            math.radians(0),
            math.radians(0),
            math.radians(0)]

    gripper_open = [math.radians(-45),
                    math.radians(-45)]

    gripper_close = [math.radians(0),
                     math.radians(0)]

    pick_stuff = [math.radians(38),
                  math.radians(-86),
                  math.radians(10),
                  math.radians(0),
                  math.radians(0)]

    place_stuff = [math.radians(-40),
                  math.radians(-45),
                  math.radians(0),
                  math.radians(0),
                  math.radians(-50)]

    maa.set_joint_angles(rest)
    mag.set_joint_angles(gripper_open)
    maa.set_joint_angles(pick_stuff)
    rospy.sleep(1.5)
    mag.set_joint_angles(gripper_close)
    rospy.sleep(1.5)
    # maa.set_joint_angles(rest)
    maa.set_joint_angles(place_stuff)
    mag.set_joint_angles(gripper_open)
    rospy.sleep(1)
    mag.set_joint_angles(gripper_close)
    maa.set_joint_angles(rest)

    rospy.spin()

    del maa
    del mag


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass