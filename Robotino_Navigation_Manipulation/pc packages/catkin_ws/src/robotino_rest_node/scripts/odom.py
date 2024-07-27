#!/usr/bin/env python3

import rospy

import math
from math import sin, cos, pi
from robotino_rest_node.msg import OdomReadings
from nav_msgs.msg import Odometry
import tf 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

pub = rospy.Publisher('odom', Odometry, queue_size=10)
odom_broadcaster = tf.TransformBroadcaster()

rospy.init_node('odometry_publisher', anonymous=True)
current_time = rospy.Time.now()
last_time = rospy.Time.now()
# odometry initializing
x = 0.0
y = 0.0
th = 0.0
# -----


def callback(data):
    
    global last_time
    global th
    global y
    global x

    vx=data.xvel
    vy=data.yvel
    vth=data.rotvel
    
    current_time = rospy.Time.now()

    # compute odometry in a typical way given the velocities of the robot
    dt = (current_time - last_time).to_sec()
    delta_x = (vx * cos(th) - vy * sin(th)) * dt
    delta_y = (vx * sin(th) + vy * cos(th)) * dt
    delta_th = vth * dt

    x += delta_x
    y += delta_y
    th += delta_th

    # since all odometry is 6DOF we'll need a quaternion created from yaw
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)

    # first, we'll publish the transform over tf
    odom_broadcaster.sendTransform(
        (x, y, 0.),
        odom_quat,
        current_time,
        "base_link",
        "odom"
    )

    # next, we'll publish the odometry message over ROS
    odom = Odometry()
    odom.header.stamp = current_time
    odom.header.frame_id = "odom"

    # set the position
    odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))

    # set the velocity
    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(data.xvel, data.yvel, 0), Vector3(0, 0, data.rotvel))

    # publish the message
    pub.publish(odom)

    last_time = current_time

    # rospy.loginfo(rospy.get_caller_id() + " xvel %s", data.xvel)
    # rospy.loginfo(rospy.get_caller_id() + " yvel %s", data.yvel)
    # rospy.loginfo(rospy.get_caller_id() + " rotvel %s", data.rotvel)
    
def listener():


    rospy.Subscriber("odomet", OdomReadings, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()