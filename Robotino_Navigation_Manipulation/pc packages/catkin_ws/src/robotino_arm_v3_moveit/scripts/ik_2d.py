#! /usr/bin/env python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list
from numpy import * 
import numpy as np
from math import *

# Length of links in cm
# a1= 0.13863 #meters
# a2 = 0.07720
# a3 = 0.0461 # to the center of rotation

a1= 13.863 #meters
a2 = 7.720
a3 = 4.61 # to the center of rotation


# offset_z=64.7
# offset_y=-0.32


# y0=16 # y is swapping
# z0=80 # we have two levels of z
# angle_wrt_y=np.deg2rad(60)

# pz=z0-offset_z
# py=y0-offset_y

# phi=angle_wrt_y

x=8
y=11

# 1- we want to go to x4 y4 
# 2-solve x3 y3 and add angle 
# 3- it will go to an approximate pose with certian oreintation 

phi=np.arccos(((x**2)+(y**2)+(a1**2)-(a2**2))/(2*a1*np.sqrt((x**2)+(y**2))))
beta=np.arctan(x/y)
theta_1=beta+phi

theta=np.arccos(((x**2)+(y**2)-(a1**2)-(a2**2))/(2*a1*a2))

theta_2=180-np.rad2deg(theta)


print(np.rad2deg(theta_1))
print(np.rad2deg(theta_2))

# # end of ik code

# moveit_commander.roscpp_initialize(sys.argv)
# rospy.init_node('move_group_python_interface_tutorial',anonymous=True)

# robot=moveit_commander.RobotCommander()

# scene=moveit_commander.PlanningSceneInterface()
# group=moveit_commander.MoveGroupCommander("arm")

# display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory, queue_size=100)
# # print(group.get_current_pose())
# print(group.get_current_rpy())
# print(group.get_current_state())

# joint_goal = group.get_current_joint_values()
# joint_goal[0] = theta_1
# joint_goal[1] = theta_2
# joint_goal[2] = theta_3

# group.go(joint_goal, wait=True)

# moveit_commander.roscpp_shutdown()