#! /usr/bin/env python3

from multiprocessing.connection import wait
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from numpy import * 
import numpy as np
# from math import *

# Length of links in cm
a1= 14
a2 = 7.7
a3 = 7.6

# Desired Position of End effector
px = -14
py = 3

phi = 90
phi = np.deg2rad(phi)

# Equations for Inverse kinematics
wx = px - a3*np.cos(phi)
wy = py - a3*np.sin(phi)

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
# group.set_goal_position_tolerance(1)
# group.set_planning_pipeline_id("trac_ik")
# group.set_planner_id("RRT")



display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory, queue_size=100)
print(group.get_current_pose())
# cpose=group.get_current_pose()
# group.set_num_planning_attempts(100000)
# group.set_planning_time(100)

pose_target=geometry_msgs.msg.Pose()
# pose_target.orientation.w= cpose.orientation.w
# pose_target.orientation.x=cpose.orientation.x
# pose_target.orientation.y=cpose.orientation.y
# pose_target.orientation.z=cpose.orientation.z

pose_target.position.x=-0.015
pose_target.position.y=0.18
pose_target.position.z=0.58
xp=[0.014,-0.008,0.86]
# group.set_random_target()

group.set_position_target(xp,"L3")

# group.set_pose_target(pose_target)

# group.set_named_target(pose_target)

plan1=group.plan()
# if not plan1.joint_trajectory.points:
#     print("error")

group.go(wait=True)
group.stop()
group.clear_pose_targets()

rospy.sleep(5)

moveit_commander.roscpp_shutdown()