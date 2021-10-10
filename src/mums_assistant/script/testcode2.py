#! /usr/bin/env python

import sys

import actionlib
import moveit_commander
import moveit_msgs.msg
import rospy
from rospy.exceptions import ROSException

class MumsAssistantGripper:

    # Constructor
    def __init__(self):

        rospy.init_node('node_mums_assistant_gripper', anonymous=True)

        self._gripper_planning_group = "gripper_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self.__gripper_group = moveit_commander.MoveGroupCommander(self._gripper_planning_group)
        self._display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

        self._exectute_trajectory_client = actionlib.SimpleActionClient('execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        self._planning_frame = self.__gripper_group.get_planning_frame()
        self._eef_link = self.__gripper_group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()


        rospy.loginfo('\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo('\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo('\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo('\033[94m' + " >>> Mum's Assistant Gripper init done." + '\033[0m')

    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self.__gripper_group.set_named_target(arg_pose_name)
        plan = self.__gripper_group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')


    # Destructor
    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Mum's Assistant Gripper Deleted." + '\033[0m')


def main():

    mag = MumsAssistantGripper()

    while not rospy.is_shutdown():
        rospy.sleep(15)
        mag.go_to_predefined_pose("gripper_open")
        rospy.sleep(2)
        mag.go_to_predefined_pose("gripper_close")
        rospy.sleep(2)

    del mag


if __name__ == '__main__':
    try:
        main()
    except ROSException as e:
        print(e)
