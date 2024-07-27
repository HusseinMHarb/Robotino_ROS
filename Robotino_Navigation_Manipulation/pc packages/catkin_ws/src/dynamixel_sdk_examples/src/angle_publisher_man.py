#!/usr/bin/env python3

from turtle import setposition
import dynamixel_sdk_examples
import rospy
import time
from dynamixel_sdk import *
from dynamixel_sdk_examples.srv import *
from dynamixel_sdk_examples.msg import *

def map_angle_to_encoder(angle,upper_angle,lower_angle,upper_limit,lower_limit):
    return int((angle -lower_angle) * (upper_limit - lower_limit) / (upper_angle -lower_angle) + lower_limit)

def initial_pos():
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)

    pub.publish(SetPosition(1,map_angle_to_encoder(9,94,9,600,320)))
    pub.publish(SetPosition(2,map_angle_to_encoder(0,91,-90,130,750)))
    pub.publish(SetPosition(3,map_angle_to_encoder(0,84,-87,720,150)))
    
def test(angle1,angle2,angle3):
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)

    if(angle1<95 and angle1>8):
        pub.publish(SetPosition(1,map_angle_to_encoder(angle1,94,9,600,320)))

    if(angle2<92 and angle2>-91):
        pub.publish(SetPosition(2,map_angle_to_encoder(angle2,91,-90,130,750)))

    if(angle3<85 and angle3>-88):
        pub.publish(SetPosition(3,map_angle_to_encoder(angle3,84,-87,720,150)))

def limits():
    a1=0
    pos1=320
    pos2=750
    pos3=150
    a2=1
    a3=0
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher', anonymous=True)
    rate = rospy.Rate(1/5) # 10hz
    while not rospy.is_shutdown():
        #SetPosition.id=1
        #SetPosition.position=320
        #second try
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

        # first try

        # pub.publish(SetPosition(3,150)) #570
        # pub.publish(SetPosition(1,320)) #280
        # pub.publish(SetPosition(2,750)) #620
        # time.sleep(5)
        # pub.publish(SetPosition(1,600))
        # pub.publish(SetPosition(2,130))
        # pub.publish(SetPosition(3,720))
        # time.sleep(5)

if __name__ == '__main__':
    try:
        time.sleep(10)
        initial_pos()
        while not rospy.is_shutdown():
            
            angle1=input("set angle for motor 1 (94-9) ")
            angle2=input("set angle for motor 2 (91,-90) ")
            angle3=input("set angle for motor 3 (84,-87) ")

            test(int(angle1),int(angle2),int(angle3))

        # angle_publisher()
    except rospy.ROSInterruptException:
        pass
