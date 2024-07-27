#!/usr/bin/env python3

from turtle import setposition
import dynamixel_sdk_examples
import rospy
import time
from dynamixel_sdk import *
from dynamixel_sdk_examples.srv import *
from dynamixel_sdk_examples.msg import *

def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def map_encoder_to_angle(encoder,upper_limit,lower_limit,upper_angle,lower_angle):
    return int((encoder -lower_limit) * (upper_angle - lower_angle) / (upper_limit -lower_limit) + lower_angle)

def map_angle_to_encoder(angle,upper_angle,lower_angle,upper_limit,lower_limit):
    return int((angle -lower_angle) * (upper_limit - lower_limit) / (upper_angle -lower_angle) + lower_limit)


    # upper_limit
    # pos1 600 = 94 degree
    # pos2 130 = 91 degree
    # pos3 720 = 84 degree
    # lower_limit
    # pos1 320= 9 degree
    # pos2 750=-90 degree
    # pos3 150 =-87 degree

def limits():
    a1=0
    pos1=320
    pos2=750
    pos3=150
    a2=0
    a3=0
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)
    rate = rospy.Rate(1/5) # 10hz
    while not rospy.is_shutdown():
        #SetPosition.id=1
        #SetPosition.position=320
        #second try

        if(a2==0):
            if(pos1<=600):
                pos1=pos1+4
                pub.publish(1,pos1)
                time.sleep(0.01)
            else:
                a1=1
            if(pos3<=720):
                pos3=pos3+4
                pub.publish(3,pos3)
                time.sleep(0.01)
            else:
                a3=1

            if(pos2>=130):
                pos2=pos2-4
                pub.publish(2,pos2)
                time.sleep(0.01)
            else:
                a2=1

def angle_publisher():
    a1=0
    pos1=320
    pos2=750
    pos3=150
    a2=0
    a3=0
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)
    rate = rospy.Rate(1/5) # 10hz
    while not rospy.is_shutdown():
        #SetPosition.id=1
        #SetPosition.position=320
        #second try

        if(a2==0):
            if(pos1<=600):
                pos1=pos1+4
                pub.publish(1,pos1)
                time.sleep(0.01)
            else:
                a1=1
            if(pos3<=720):
                pos3=pos3+4
                pub.publish(3,pos3)
                time.sleep(0.01)
            else:
                a3=1

            if(pos2>=130):
                pos2=pos2-4
                pub.publish(2,pos2)
                time.sleep(0.01)
            else:
                a2=1
        if(a2==1):
            if(pos3>=150):
                pos3=pos3-4
                pub.publish(3,pos3)
                time.sleep(0.01)
            else:
                a3=0
            if(pos1>=320):
                pos1=pos1-4
                pub.publish(1,pos1)
                time.sleep(0.01)
            else:
                a1=0
            if(pos2<=750):
                pos2=pos2+4
                pub.publish(2,pos2)
                time.sleep(0.01)
            else:
                a2=0


if __name__ == '__main__':
    try:
        angle_publisher()
    except rospy.ROSInterruptException:
        pass