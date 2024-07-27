#!/usr/bin/env python

import rospy
import time


def map_angle_to_encoder(angle,upper_angle,lower_angle,upper_limit,lower_limit):
    return int((angle -lower_angle) * (upper_limit - lower_limit) / (upper_angle -lower_angle) + lower_limit)


def test(c_angle1,c_angle2,c_angle3,angle1,angle2,angle3):

    if(angle1<95 and angle1>8):
        if (c_angle1<angle1):
            c_angle1+=1
        elif(c_angle1>angle1):
            c_angle1-=1


    if(angle2<92 and angle2>-91):
        if (c_angle2<angle2):
            c_angle2+=1
        elif(c_angle2>angle2):
            c_angle2-=1

    if(angle3<85 and angle3>-88):
        if (c_angle3<angle3):
            c_angle3+=1
        elif(c_angle3>angle3):
            c_angle3-=1
    return c_angle1 , c_angle2 , c_angle3

if __name__ == '__main__':
    try:
        c_angle1=9
        c_angle2=0
        c_angle3=0


        while not rospy.is_shutdown():
            c_angle1,c_angle2,c_angle3=test(c_angle1,c_angle2,c_angle3,9,-90,-50)
            time.sleep(1)

    except rospy.ROSInterruptException:
        pass
