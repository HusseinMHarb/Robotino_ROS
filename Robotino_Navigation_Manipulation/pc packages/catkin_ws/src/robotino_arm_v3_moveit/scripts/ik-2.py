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
offset_phi=-1.4747
offset_z=64.7
offset_y=-0.32 #8.3
# z0-offset_z=pz
# y0-offset_y=py
y0=15
z0=79
# y0=18.2
# z0=70
angle_wrt_y=np.deg2rad(0)

# y0=10.5-8.3
# z0=-14.9+64.7

pz=z0-offset_z
py=y0-offset_y
# py0=11
# pz0=76
# # Desired Position of End effector
# px = py0-offset_y #y
# py = pz0-offset_z #z
# pz=12 #z
# py=20 #y

phi=angle_wrt_y
# phi = 0 #angle wrt y
# phi = np.deg2rad(phi)

# Equations for Inverse kinematics
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

print('theta_1: ', np.rad2deg(theta_1))
print('theta_2: ', np.rad2deg(theta_2))
print('theta_3: ', np.rad2deg(theta_3))

# end of ik code

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',anonymous=True)

robot=moveit_commander.RobotCommander()

scene=moveit_commander.PlanningSceneInterface()
group=moveit_commander.MoveGroupCommander("arm")

display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory, queue_size=100)
# print(group.get_current_pose())
# print(group.get_current_rpy())
# print(group.get_current_state())

joint_goal = group.get_current_joint_values()
joint_goal[0] = theta_1
joint_goal[1] = theta_2
joint_goal[2] = theta_3

group.go(joint_goal, wait=True)

moveit_commander.roscpp_shutdown()