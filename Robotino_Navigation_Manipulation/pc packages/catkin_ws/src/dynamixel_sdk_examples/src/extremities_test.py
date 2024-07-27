#!/usr/bin/env python3

from turtle import setposition
import dynamixel_sdk_examples
import rospy
import time
from dynamixel_sdk import *
from dynamixel_sdk_examples.msg import *

def angle_publisher():
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)

    while not rospy.is_shutdown():

        pub.publish(SetPosition(3,150)) #570
        pub.publish(SetPosition(1,320)) #280
        pub.publish(SetPosition(2,750)) #620
        time.sleep(5)
        pub.publish(SetPosition(1,600))
        pub.publish(SetPosition(2,130))
        pub.publish(SetPosition(3,720))
        time.sleep(5)

if __name__ == '__main__':
    try:
        angle_publisher()
    except rospy.ROSInterruptException:
        pass