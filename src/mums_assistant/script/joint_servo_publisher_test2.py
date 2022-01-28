#! /usr/bin/env python3

import rospy
import sys
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Float32MultiArray
from tf.transformations import euler_from_quaternion

class MumsAssistantGripper:

    # Constructor
    def __init__(self):

        self._planning_group = "gripper_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        self._display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)
        self.pub = rospy.Publisher("/joint_servo_gripper_rviz_topic", Float32MultiArray, queue_size=1)

        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()

        rospy.loginfo(
            '\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo('\033[94m' + " >>> Ur5Moveit init done." + '\033[0m')

        self.prev = False
        self.prev_lst_val = []
        self.new_lst_val = []
        self.new_list_joint_values = []
        self.list_joint_values = []

    def publish_joint_angles(self):

        self.new_list_joint_values = []
        self.list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo_once("Getting Joint Values")
        # new_list_joint_values = self._group.get_joints()
        for num in self.list_joint_values:
            formatted_float = "{:.3f}".format(num)
            self.new_list_joint_values.append(float(formatted_float))

        if self.prev is False:
            self.prev_lst_val = self.new_list_joint_values
            self.prev = True
        else:
            self.new_lst_val = self.new_list_joint_values
            self.prev = False

        if self.prev_lst_val == self.new_lst_val:
            print(f">>>> Publishing Data to servo")
            self.prev = False
            data_to_send = Float32MultiArray(data=self.new_list_joint_values)  # the data to be sent, initialise the array
            self.pub.publish(data_to_send)
        else:
            rospy.loginfo("Gripper moving")

    # Destructor

    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class MumsAssistant Deleted." + '\033[0m')