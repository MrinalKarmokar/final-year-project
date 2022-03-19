#! /usr/bin/env python3

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

    pick_stuff = [math.radians(33),
                  math.radians(-89),
                  math.radians(13),
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
    rospy.sleep(2)
    mag.set_joint_angles(gripper_close)
    rospy.sleep(2)
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
