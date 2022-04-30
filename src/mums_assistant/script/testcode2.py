#! /usr/bin/env python3

import sys

import actionlib
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Float32MultiArray
import rospy


class MumsAssistantGripper:

    # Constructor
    def __init__(self):

        # rospy.init_node('node_planning_gripper', anonymous=True)

        self._planning_group = "gripper_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        self._display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)
        self.pub = rospy.Publisher(
            "/joint_servo_gripper_topic", Float32MultiArray, queue_size=10)

        self._exectute_trajectory_client = actionlib.SimpleActionClient(
            'execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()

        rospy.loginfo(
            '\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo(
            '\033[94m' + " >>> Mum's Assistant Gripper init done." + '\033[0m')

    def joint_servo_gripper_talker(self, list_joint_values):

        # the data to be sent, initialise the array
        data_to_send = Float32MultiArray(data=list_joint_values)
        rospy.loginfo(
            '\033[94m' + f">>> Joint Servo Gripper Talker: {data_to_send.data}" + '\033[0m')
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

        if (flag_plan == True):
            rospy.loginfo(
                '\033[94m' + ">>> set_joint_angles() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> set_joint_angles() Failed." + '\033[0m')

        return flag_plan

    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo(
            '\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo(
            '\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')

    def add_box(self):
        '''Adding Box in RVIZ planning'''

        box_name = self._box_name
        scene = self._scene
        robot = self._robot
        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = robot.get_planning_frame()
        box_pose.pose.orientation.w = 1.0
        box_pose.pose.position.x = 0.0
        box_pose.pose.position.y = 0.45
        box_pose.pose.position.z = 1.91
        box_name = "box"
        scene.add_box(box_name, box_pose, size=(0.15, 0.15, 0.15))
        self._box_name = box_name

    def attach_box(self):
        '''Attach Box to Ur5 Robot in RVIZ planning'''

        box_name = self._box_name
        robot = self._robot
        scene = self._scene
        eef_link = self._eef_link
        grasping_group = 'ur5_1_planning_group'
        touch_links = robot.get_link_names(group=grasping_group)
        scene.attach_box(eef_link, box_name, touch_links=touch_links)

    def remove_box(self):
        '''Remove Box from RVIZ planning'''

        box_name = self._box_name
        scene = self._scene
        eef_link = self._eef_link
        scene.remove_attached_object(eef_link, name=box_name)
        scene.remove_world_object(box_name)

    # Destructor

    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Mum's Assistant Gripper Deleted." + '\033[0m')
