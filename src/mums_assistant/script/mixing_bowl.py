#! /usr/bin/env python3

import sys
import math
import rospy

from testcode import MumsAssistantArm
from testcode2 import MumsAssistantGripper


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

    spoon_pick = [math.radians(23),
                  math.radians(-70),
                  math.radians(-25),
                  math.radians(0),
                  math.radians(-47)]

    mix01 = [math.radians(-40),
             math.radians(-45),
             math.radians(0),
             math.radians(0),
             math.radians(-50)]

    mix02 = [math.radians(-40),
             math.radians(-64),
             math.radians(29),
             math.radians(0),
             math.radians(-60)]

    mix03 = [math.radians(-55),
             math.radians(-62),
             math.radians(-29),
             math.radians(0),
             math.radians(-59)]

    mix04 = [math.radians(-55),
             math.radians(-42),
             math.radians(0),
             math.radians(0),
             math.radians(-48)]

    maa.set_joint_angles(rest)
    mag.set_joint_angles(gripper_open)
    rospy.sleep(1)
    maa.set_joint_angles(spoon_pick)
    rospy.sleep(1)
    mag.set_joint_angles(gripper_close)
    rospy.sleep(5)
    maa.set_joint_angles(rest)
    rospy.sleep(5)

    if len(sys.argv) > 1:
        rospy.loginfo(f"Mixing {sys.argv[1]}")
        for i in range(1, int(sys.argv[1])):
            maa.set_joint_angles(mix01)
            rospy.sleep(1)
            maa.set_joint_angles(mix02)
            rospy.sleep(1)
            maa.set_joint_angles(mix03)
            rospy.sleep(1)
            maa.set_joint_angles(mix04)
            rospy.sleep(1)

    else:
        rospy.loginfo("Mixing Once")
        maa.set_joint_angles(mix01)
        rospy.sleep(1)
        maa.set_joint_angles(mix02)
        rospy.sleep(1)
        maa.set_joint_angles(mix03)
        rospy.sleep(1)
        maa.set_joint_angles(mix04)
        rospy.sleep(1)
        maa.set_joint_angles(mix01)
        rospy.sleep(1)

    maa.set_joint_angles(rest)
    rospy.sleep(1)
    maa.set_joint_angles(spoon_pick)
    rospy.sleep(5)
    mag.set_joint_angles(gripper_open)
    rospy.sleep(5)
    maa.set_joint_angles(rest)
    rospy.sleep(1)
    mag.set_joint_angles(gripper_close)

    rospy.spin()

    del maa
    del mag


if __name__ == '__main__':
    try:
        main()
    except Exception:
        pass
