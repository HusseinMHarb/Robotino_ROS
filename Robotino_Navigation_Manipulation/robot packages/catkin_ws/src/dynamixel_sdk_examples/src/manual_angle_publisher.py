#!/usr/bin/env python2
from turtle import setposition
import dynamixel_sdk_examples
import rospy
import time
from dynamixel_sdk import *
from dynamixel_sdk_examples.msg import *

def map_angle_to_encoder(angle,upper_angle,lower_angle,upper_limit,lower_limit):
    return int((angle -lower_angle) * (upper_limit - lower_limit) / (upper_angle -lower_angle) + lower_limit)

def initial_pos():
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    pub.publish(SetPosition(1,map_angle_to_encoder(9,94,9,600,320)))
    pub.publish(SetPosition(2,map_angle_to_encoder(0,91,-90,130,750)))
    pub.publish(SetPosition(3,map_angle_to_encoder(0,84,-87,720,150)))
    
def man_pub(angle1,angle2,angle3):
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)

    if(angle1<95 and angle1>8):
        pub.publish(SetPosition(1,map_angle_to_encoder(angle1,94,9,600,320)))

    if(angle2<92 and angle2>-91):
        pub.publish(SetPosition(2,map_angle_to_encoder(angle2,91,-90,130,750)))

    if(angle3<85 and angle3>-88):
        pub.publish(SetPosition(3,map_angle_to_encoder(angle3,84,-87,720,150)))

if __name__ == '__main__':
    try:
        time.sleep(10)
        initial_pos()
        time.sleep(5)
        while not rospy.is_shutdown():       
            angle1=input("set angle for motor 1 (94-9) ")
            angle2=input("set angle for motor 2 (91,-90) ")
            angle3=input("set angle for motor 3 (84,-87) ")
            man_pub(int(angle1),int(angle2),int(angle3))
    except rospy.ROSInterruptException:
        pass
