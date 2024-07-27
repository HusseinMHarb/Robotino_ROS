#! /usr/bin/env python3

import rospy
from cmvision.msg import Blobs

import message_filters
import sys
import rospy
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


    group.set_named_target ("grip")
    group.go(wait=True)

    gripper.set_named_target ("closed")
    gripper.go(wait=True)

    group.set_named_target ("final")
    group.go(wait=True)

    gripper.set_named_target ("open")
    gripper.go(wait=True)

    group.set_named_target ("home")
    group.go(wait=True)

    gripper.set_named_target ("closed")
    gripper.go(wait=True)
    # print("end")
    # time.sleep(3)

    # moveit_commander.roscpp_shutdown()

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
        print ("no green color exist! :(")
    else:
        global i
        # print("else")
        ms=data.blobs[0]
        name=ms.name
        posx=ms.x
        # print(posx)
        posy=ms.y
        area=ms.area
        if(name == "green"):
            print("Cube is Green :)")
            if(1500<area<2300):
                print("cube has the right size :)")
                if(79<posx<99):
                    print("at x position !!")
                    if(69<posy<81):
                        if(i==0):
                            print("at y position!!")
                            print("")
                            print("------------------------------------")
                            print("Let us grip it ;)")
                            print("")
                            print("------------------------------------")
                            grip()

def color_sorter():

    rospy.init_node('color_sorter', anonymous=True)

    sub=rospy.Subscriber("blobs", Blobs, callback,queue_size=None,buff_size=1)

    rospy.spin()

if __name__ == '__main__':
    color_sorter()