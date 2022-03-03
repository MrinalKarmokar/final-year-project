#!/usr/bin/env python3
import math

import rospy
from mums_assistant.msg import Dofs
from sensor_msgs.msg import JointState


def cb(msg):

    dofs = Dofs()
    dofs.joint1 = int(math.degrees(msg.position[0])+90)
    dofs.joint2 = int(math.degrees(msg.position[1])+90)
    dofs.joint3 = int(math.degrees(msg.position[2])+90)
    dofs.joint4 = int(math.degrees(msg.position[3])+90)
    dofs.joint5 = int(math.degrees(msg.position[4])+90)
    dofs.joint6 = int(math.degrees(msg.position[5])+90)
    print("Publishing")
    pub.publish(dofs)

if __name__ == '__main__':
    try:
        rospy.init_node('jointstate_to_plain')

        pub = rospy.Publisher("arm_dofs", Dofs, queue_size=1)
        rospy.Subscriber("joint_states", JointState, cb)
        rospy.spin()

    except:
        pass
