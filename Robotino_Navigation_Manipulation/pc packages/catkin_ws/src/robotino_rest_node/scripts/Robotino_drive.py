#! /usr/bin/env python3

import requests 
import rospy
import sys
import json
import time
import signal
from geometry_msgs.msg import Twist

# api end point

ROBOTINOIP = "172.27.1.1:80"
PARAMS = {'sid':'rest_api'}
run = True

def set_vel(vel):
    OMNIDRIVE_URL = "http://" + ROBOTINOIP + "/data/omnidrive"
    r = requests.post(url = OMNIDRIVE_URL, params = PARAMS, json = vel )
    if r.status_code != requests.codes.ok:
        raise RuntimeError("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)

def callback(data):
    set_vel([data.linear.x,data.linear.y,data.angular.z])

def navigate():
	rospy.init_node('robotino_omnidrive', anonymous=True)
	rospy.Subscriber("cmd_vel", Twist, callback)
	rospy.spin()

def signal_handler(sig, frame):
    global run
    print('You pressed Ctrl+C!')
    run = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    navigate()