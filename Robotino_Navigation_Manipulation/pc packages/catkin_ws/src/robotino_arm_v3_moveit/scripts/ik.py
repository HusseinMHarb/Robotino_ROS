#! /usr/bin/env python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from numpy import * 
import numpy as np

# Length of links in cm
a1= 14
a2 = 7.7
a3 = 4.61
# offset between local and global origin
offset_z=64.7
offset_y=-0.32 #8.3

# define end cordinates with respect to global origin
y0=15
z0=79
# define the orientation of the end effector with respect to y axis
angle_wrt_y=np.deg2rad(0)

# define translation between local and global origins
pz=z0-offset_z
py=y0-offset_y


# Equations for kinematics
phi=angle_wrt_y
wx = py - a3*np.cos(phi)
wy = pz - a3*np.sin(phi)

delta = wx**2 + wy**2
c2 = ( delta -a1**2 -a2**2)/(2*a1*a2)
s2 = np.sqrt(1-c2**2)  # elbow down
theta_2 = np.arctan2(s2, c2)

s1 = ((a1+a2*c2)*wy - a2*s2*wx)/delta
c1 = ((a1+a2*c2)*wx + a2*s2*wy)/delta
theta_1 = np.arctan2(s1,c1)
theta_3 = phi-theta_1-theta_2

#print the results
print('theta_1: ', np.rad2deg(theta_1))
print('theta_2: ', np.rad2deg(theta_2))
print('theta_3: ', np.rad2deg(theta_3))

# end of ik code


# initialize a new node and moveit commander
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface',anonymous=True)

# initialize robotcommander for tf, planingSceneInterface,and MoveGroupCommander to decide on the targeted group.
robot=moveit_commander.RobotCommander()
scene=moveit_commander.PlanningSceneInterface()
group=moveit_commander.MoveGroupCommander("arm")

display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory, queue_size=100)
# define joint goals
joint_goal = group.get_current_joint_values()
joint_goal[0] = theta_1
joint_goal[1] = theta_2
joint_goal[2] = theta_3

# actuate the order and shutdown moveit commander
group.go(joint_goal, wait=True)

moveit_commander.roscpp_shutdown()