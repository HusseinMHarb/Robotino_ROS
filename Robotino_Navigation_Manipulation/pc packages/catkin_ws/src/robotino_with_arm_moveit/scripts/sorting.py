#! /usr/bin/env python3

import rospy
import sys
from cmvision.msg import Blobs
from geometry_msgs.msg import Twist
import moveit_commander
import moveit_msgs.msg

from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from numpy import * 

i=0

def grip():
    global i
    i=1
    # print("Hi")
    # rospy.sleep(3)
    # rospy.Subscriber("blobs", Blobs, callback,queue_size=None,buff_size=1)
    # rospy.spin()
    # color_sorter()
    moveit_commander.roscpp_initialize(sys.argv)

    robot=moveit_commander.RobotCommander()

    scene=moveit_commander.PlanningSceneInterface()
    group=moveit_commander.MoveGroupCommander("arm")
    gripper=moveit_commander.MoveGroupCommander("gripper")

    display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory, queue_size=100)

    gripper.set_named_target ("closed")
    gripper.go(wait=True)

    gripper.set_named_target ("open")
    gripper.go(wait=True)


    group.set_named_target ("pregrip")
    group.go(wait=True)

    gripper.set_named_target ("closed")
    gripper.go(wait=True)

    group.set_named_target ("final")
    group.go(wait=True)

    #gripper.set_named_target ("open")
    #gripper.go(wait=True)

    group.set_named_target ("home")
    group.go(wait=True)

    gripper.set_named_target ("closed")
    gripper.go(wait=True)


def callback(data):
    try:
        # rospy.sleep(2)
        # print("Try")
        # name=None
        # posx=0
        # posy=0
        # area=0
        ms=data.blobs[0]
    except IndexError:
        # name=None
        # posx=0
        # posy=0
        # area=0
        i=0
        print ("no blue color exist! :(")
    else:
        global msg
        msg=Twist()
        pub = rospy.Publisher('cmd_vel',Twist ,queue_size=100)
        global i
        # print("else")
        ms=data.blobs[0]
        name=ms.name
        posx=ms.x
        posy=ms.y
        #print(posy)
        area=ms.area
        if(name == "Blue"):
            print("Cube is Blue :)")
            if(20<area<10000):
                print("cube has the right size :)")
                if(posx>390): #400
                    msg.angular.z=0.05
                    pub.publish(msg)

                if(posx<350): #300
                    msg.angular.z=-0.05
                    pub.publish(msg)

                if(360<posx<390):
                    print("at x position !!")
                    msg.angular.z= 0.0
                    pub.publish(msg)
                    if(posy>240): #240
                        msg.linear.x=0.02
                        pub.publish(msg)

                    if(posy<200): #200
                        msg.linear.x=-0.1
                        pub.publish(msg)

                    if(200<posy<240):
                        msg.linear.x=0.0
                        pub.publish(msg)
                        grip()
                        if(i==0):
                            print("at y position!!")
                            print("")
                            print("------------------------------------")
                            print("Let us grip it ;)")
                            print("")
                            print("------------------------------------")

def color_sorter():

    rospy.init_node('color_sorter', anonymous=True)

    sub=rospy.Subscriber("blobs", Blobs, callback,queue_size=None,buff_size=1)

    rospy.spin()

if __name__ == '__main__':
    color_sorter()
