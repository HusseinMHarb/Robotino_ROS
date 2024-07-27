#!/usr/bin/env python2
from turtle import setposition
from unicodedata import name
import dynamixel_sdk_examples
import rospy
import time
from dynamixel_sdk import *
from dynamixel_sdk_examples.srv import *
from dynamixel_sdk_examples.msg import *

from sensor_msgs.msg import JointState

a1=0
a2=0
a3=0
a1f=0
a2f=0
a3f=0
ag=0
agf=0
pub = rospy.Publisher('set_position', SetPosition, queue_size=100)

def callback(data):
    global a1
    global a2
    global a3
    global a1f
    global a2f
    global a3f
    global ag
    global agf
    
    a1=rad_to_degree(data.position[3]) 
    a2=rad_to_degree(data.position[4]) 
    a3=rad_to_degree(data.position[5]) 
    ag=rad_to_degree(data.position[6])
    
    # print(2)
    if(abs(a1-a1f)>0.0001):
        # print("ok")
        pub.publish(SetPosition(1,map_angle_to_encoder(a1,94,9,600,320)))
        a1f=a1
        # time.sleep(0.01)
    if(abs(a2-a2f)>0.0001):
        pub.publish(SetPosition(2,map_angle_to_encoder(a2,91,-90,130,750)))
        a2f=a2
        # time.sleep(0.01)
    if(abs(a3-a3f)>0.0001):
        pub.publish(SetPosition(3,map_angle_to_encoder(a3,84,-87,720,150)))
        a3f=a3
        # time.sleep(0.01)
    if (abs(ag - agf)> 1):
        if (ag>35):
            pub.publish(SetPosition(4,560)) #open
            agf=ag
        if (ag<35):
            pub.publish(SetPosition(4,620))
            agf=ag
        
    
    # else:
        
    
def joint_reader():
    rospy.Subscriber("joint_states", JointState, callback)
    # print(1)

def map_m2_to_zero(angle):
    return angle-1

def rad_to_degree(angle1):
    return(angle1*(180/3.14))
def map_angle_to_encoder(angle,upper_angle,lower_angle,upper_limit,lower_limit):
    return int((angle -lower_angle) * (upper_limit - lower_limit) / (upper_angle -lower_angle) + lower_limit)

def initial_pos():
    
    pub = rospy.Publisher('set_position', SetPosition, queue_size=10)
    rospy.init_node('angle_publisher_in', anonymous=True)
    pub.publish(SetPosition(1,map_angle_to_encoder(90,94,9,600,320)))
    pub.publish(SetPosition(2,map_angle_to_encoder(0,91,-90,130,750)))
    pub.publish(SetPosition(3,map_angle_to_encoder(0,84,-87,720,150)))
    
    return(0)

if __name__ == '__main__':
    try:
        i=0
        rospy.init_node('joint_reader', anonymous=True)
        joint_reader()
        # print(an)
        
        # initial_pos()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
