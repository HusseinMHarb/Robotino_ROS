#!/usr/bin/env python3
from __future__ import print_function
from multiprocessing.connection import wait

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

try:
    from math import pi, tau, dist, fabs, cos
except:  # For Python 2 compatibility
    from math import pi, fabs, cos, sqrt

    tau = 2.0 * pi

    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))

from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if the values in two lists are within a tolerance of each other.
    For Pose and PoseStamped inputs, the angle between the two quaternions is compared (the angle
    between the identical orientations q and -q is calculated correctly).
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float
    @returns: bool
    """
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        # Euclidean distance
        d = dist((x1, y1, z1), (x0, y0, z0))
        # phi = angle between orientations
        cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
        return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

    return True

class MoveGroupPythonInterfaceTutorial(object):
    def __init__(self):
        super(MoveGroupPythonInterfaceTutorial, self).__init__()

        ## First initialize `moveit_commander`_ and a `rospy`_ node:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python_interface", anonymous=True)

        ## Instantiate a `RobotCommander`_ object. Provides information such as the robot's
        ## kinematic model and the robot's current joint states
        robot = moveit_commander.RobotCommander()

        ## Instantiate a `PlanningSceneInterface`_ object.  This provides a remote interface
        ## for getting, setting, and updating the robot's internal understanding of the
        ## surrounding world:
        scene = moveit_commander.PlanningSceneInterface()

        ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
        ## to a planning group (group of joints).  In this tutorial the group is the primary
        ## arm joints in the Panda robot, so we set the group's name to "panda_arm".
        ## If you are using a different robot, change this value to the name of your robot
        ## arm planning group.
        ## This interface can be used to plan and execute motions:
        group_name = "arm"
        move_group = moveit_commander.MoveGroupCommander(group_name)

        ## Create a `DisplayTrajectory`_ ROS publisher which is used to display
        ## trajectories in Rviz:
        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )

        ## Getting Basic Information
        ## ^^^^^^^^^^^^^^^^^^^^^^^^^
        # We can get the name of the reference frame for this robot:
        planning_frame = move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Available Planning Groups:", robot.get_group_names())

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state")
        print(robot.get_current_state())
        print("")
        ## END_SUB_TUTORIAL

        # Misc variables
        self.box_name = ""
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    # def go_to_joint_state(self):

    #     move_group = self.move_group

    #     ## Planning to a Joint Goal
    #     ## ^^^^^^^^^^^^^^^^^^^^^^^^
    #     joint_goal = move_group.get_current_joint_values()
    #     joint_goal[0] = 0.7
    #     joint_goal[1] = -tau / 8
    #     joint_goal[2] = 0

    #     # The go command can be called with joint values, poses, or without any
    #     # parameters if you have already set the pose or joint target for the group
    #     move_group.go(joint_goal, wait=True)

    #     # Calling ``stop()`` ensures that there is no residual movement
    #     move_group.stop()

    #     ## END_SUB_TUTORIAL

    #     # For testing:
    #     current_joints = move_group.get_current_joint_values()
    #     return all_close(joint_goal, current_joints, 0.01)
    
    def plan_cartesian_path(self, scale=1):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.move_group

        ## BEGIN_SUB_TUTORIAL plan_cartesian_path
        ##
        ## Cartesian Paths
        ## ^^^^^^^^^^^^^^^
        ## You can plan a Cartesian path directly by specifying a list of waypoints
        ## for the end-effector to go through. If executing  interactively in a
        ## Python shell, set scale = 1.0.
        ##
        waypoints = []

        wpose = move_group.get_current_pose().pose
        wpose.position.z +=scale*1.2  # First move up (z)
        # wpose.position.y = 0.4  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        # wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
        # waypoints.append(copy.deepcopy(wpose))

        # wpose.position.y -= scale * 0.1  # Third move sideways (y)
        # waypoints.append(copy.deepcopy(wpose))

        # We want the Cartesian path to be interpolated at a resolution of 1 cm
        # which is why we will specify 0.01 as the eef_step in Cartesian
        # translation.  We will disable the jump threshold by setting it to 0.0,
        # ignoring the check for infeasible jumps in joint space, which is sufficient
        # for this tutorial.
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:
        return plan, fraction

    def display_trajectory(self, plan):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        robot = self.robot
        display_trajectory_publisher = self.display_trajectory_publisher

        ## BEGIN_SUB_TUTORIAL display_trajectory
        ##
        ## Displaying a Trajectory
        ## ^^^^^^^^^^^^^^^^^^^^^^^
        ## You can ask RViz to visualize a plan (aka trajectory) for you. But the
        ## group.plan() method does this automatically so this is not that useful
        ## here (it just displays the same trajectory again):
        ##
        ## A `DisplayTrajectory`_ msg has two primary fields, trajectory_start and trajectory.
        ## We populate the trajectory_start with our current robot state to copy over
        ## any AttachedCollisionObjects and add our plan to the trajectory.
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        # Publish
        display_trajectory_publisher.publish(display_trajectory)

    def execute_plan(self, plan):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.move_group

        ## BEGIN_SUB_TUTORIAL execute_plan
        ##
        ## Executing a Plan
        ## ^^^^^^^^^^^^^^^^
        ## Use execute if you would like the robot to follow
        ## the plan that has already been computed:
        move_group.execute(plan, wait=True)

    # def wait_for_state_update(
    #     self, box_is_known=False, box_is_attached=False, timeout=4
    # ):
    #     # Copy class variables to local variables to make the web tutorials more clear.
    #     # In practice, you should use the class variables directly unless you have a good
    #     # reason not to.
    #     box_name = self.box_name
    #     scene = self.scene

    #     ## Ensuring Collision Updates Are Received
    #     ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #     ## If the Python node dies before publishing a collision object update message, the message
    #     ## could get lost and the box will not appear. To ensure that the updates are
    #     ## made, we wait until we see the changes reflected in the
    #     ## ``get_attached_objects()`` and ``get_known_object_names()`` lists.
    #     ## For the purpose of this tutorial, we call this function after adding,
    #     ## removing, attaching or detaching an object in the planning scene. We then wait
    #     ## until the updates have been made or ``timeout`` seconds have passed
    #     start = rospy.get_time()
    #     seconds = rospy.get_time()
    #     while (seconds - start < timeout) and not rospy.is_shutdown():
    #         # Test if the box is in attached objects
    #         attached_objects = scene.get_attached_objects([box_name])
    #         is_attached = len(attached_objects.keys()) > 0

    #         # Test if the box is in the scene.
    #         # Note that attaching the box will remove it from known_objects
    #         is_known = box_name in scene.get_known_object_names()

    #         # Test if we are in the expected state
    #         if (box_is_attached == is_attached) and (box_is_known == is_known):
    #             return True

    #         # Sleep so that we give other threads time on the processor
    #         rospy.sleep(0.1)
    #         seconds = rospy.get_time()

    #     # If we exited the while loop without returning then we timed out
    #     return False
    
    # def go_to_pose_goal(self):

    #     move_group = self.move_group
    

    #     ## Planning to a Pose Goal
    #     ## ^^^^^^^^^^^^^^^^^^^^^^^
    #     ## We can plan a motion for this group to a desired pose for the
    #     ## end-effector:
    #     print(move_group.get_current_pose())
    #     move_group.set_goal_position_tolerance(0.1)
    #     move_group.set_max_velocity_scaling_factor(1)
    #     pose_goal = geometry_msgs.msg.Pose()
    #     # pose_goal.orientation.w = 0.7
    #     pose_goal.position.x = 0.014
    #     pose_goal.position.y = 0.17
    #     pose_goal.position.z = 0.70
    #     # pose_goal.position.x = 0.9
    #     # pose_goal.position.y = -3.3
    #     # pose_goal.position.z = 0.0005

    #     # move_group.set_pose_target(pose_goal,"L3")
    #     move_group.set_num_planning_attempts(50)

    #     ## Now, we call the planner to compute the plan and execute it.
    #     move_group.set_position_target(pose_goal)
    #     # plan = move_group.go(wait=True)
    #     plan=move_group.go(wait=True)
    #     # Calling `stop()` ensures that there is no residual movement
    #     move_group.stop()
    #     # It is always good to clear your targets after planning with poses.
    #     # Note: there is no equivalent function for clear_joint_value_targets()
    #     move_group.clear_pose_targets()

    #     ## END_SUB_TUTORIAL

    #     # For testing:
    #     # Note that since this section of code will not be included in the tutorials
    #     # we use the class variable rather than the copied state variable
    #     current_tolerance=move_group.get_goal_position_tolerance ()
    #     current_pose = self.move_group.get_current_pose().pose
    #     print(current_tolerance)
    #     print(move_group.get_current_pose())
    #     return all_close(pose_goal, current_pose, 0.01)
    
    def pose(self):
        move_group=self.move_group
        print(move_group.get_current_pose())
        pose_goal = geometry_msgs.msg.Pose()
        # pose_goal.orientation.w = 1.0
        # pose_goal.position.x = 0.9
        # pose_goal.position.y = 0.1
        # pose_goal.position.z = 0.6
        plan = move_group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        move_group.stop()
        # It is always good to clear your targets after planning with poses.
        # Note: there is no equivalent function for clear_joint_value_targets()
        current_pose = self.move_group.get_current_pose().pose
        move_group.clear_pose_targets()
        print(move_group.get_known_constraints())
        return all_close(pose_goal, current_pose, 0.01)
        

def main():
    try:
        print("")
        print("----------------------------------------------------------")
        print("Gripping motion initiated")
        print("----------------------------------------------------------")
        # print("Press Ctrl-D to exit at any time")
        print("")
        input(
            # "============ Press `Enter` to begin the tutorial by setting up the moveit_commander ..."
        )
        tutorial = MoveGroupPythonInterfaceTutorial()

        # input(
        #     "============ Press `Enter` to execute a movement using a joint state goal ..."
        # )
        # tutorial.go_to_joint_state()

        # input("============ Press `Enter` to execute a movement using a pose goal ...")
        # tutorial.go_to_pose_goal()
        # tutorial.pose()

        # input("============ Press `Enter` to plan and display a Cartesian path ...")
        cartesian_plan, fraction = tutorial.plan_cartesian_path()

        # input(
        #     "============ Press `Enter` to display a saved trajectory (this will replay the Cartesian path)  ..."
        # )
        tutorial.display_trajectory(cartesian_plan)

        # input("============ Press `Enter` to execute a saved path ...")
        tutorial.execute_plan(cartesian_plan)

        # print("============ Python tutorial demo complete!")
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return
if __name__ == "__main__":
    main()