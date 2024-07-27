#! /usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
from numpy import * 
import numpy as np

# define the angles you need to send to the robot
theta_1=50
theta_2=50
theta_3=50

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
joint_goal[0] = np.deg2rad(theta_1)
joint_goal[1] = np.deg2rad(theta_2)
joint_goal[2] = np.deg2rad(theta_3)

# actuate the order and shutdown moveit commander
group.go(joint_goal, wait=True)

moveit_commander.roscpp_shutdown()