#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, REC Robotics Equipment Corporation GmbH, Planegg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import requests 
import sys
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool

from robotino_rest_node.msg import AnalogReadings


from robotino_rest_node.msg import DistanceSenosorsReadings
from robotino_rest_node.msg import DigitalReadings
from robotino_rest_node.msg import PowerReadings
from robotino_rest_node.msg import OdomReadings

# api-endpoint 
URL_BUMPER = "http://172.27.1.1/data/bumper"
URL_ANALOGINPUTARRAY= "http://172.27.1.1/data/analoginputarray"
URL_DIGITALINPUTARRAY="http://172.27.1.1/data/digitalinputarray"
URL_ODOM="http://172.27.1.1/data/odometry"
URL_DISTANCE="http://172.27.1.1/data/distancesensorarray"
URL_POWER="http://172.27.1.1/data/powermanagement"
URL_CURRENT="http://172.27.1.1/data/poweroutputcurrent"


PARAMS = {'sid':'robotino_rest_node'} 

def talker():
	
	bumperPub = rospy.Publisher('bumper', Bool, queue_size=1)
	analog_readingsPub = rospy.Publisher('analog_readings', AnalogReadings, queue_size=1)
	digital_readingsPub = rospy.Publisher('digital_readings', DigitalReadings, queue_size=1)
	ODOM=rospy.Publisher('odomet',OdomReadings,queue_size=1)
	distance_readingsPub=rospy.Publisher('distance_readings',DistanceSenosorsReadings,queue_size=1)
	power_readingsPub=rospy.Publisher('power_readings',PowerReadings,queue_size=1)
	rospy.init_node('robotino_sensors', anonymous=True)
	rate = rospy.Rate(10) # 10hz

	while not rospy.is_shutdown():
		try:
			r = requests.get(url = URL_BUMPER, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				bumperPub.publish(data["value"])
			else:
				rospy.logwarn("get from %s with params %s failed", URL_BUMPER, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_ANALOGINPUTARRAY, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg = AnalogReadings()
				msg.stamp = rospy.get_rostime()
				msg.values = data
				analog_readingsPub.publish(msg)
			else:
				rospy.logwarn("get from %s with params %s failed", URL_ANALOGINPUTARRAY, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_ODOM, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg1 = OdomReadings()
				msg1.stamp = rospy.get_rostime()
				msg1.xpos = data[0]
				msg1.ypos = data[1]
				msg1.rot = data[2]
				msg1.xvel = data[3]
				msg1.yvel = data[4]
				msg1.rotvel = data[5]
				ODOM.publish(msg1)
			else:
				rospy.logwarn("get from %s with params %s failed", URL_ODOM, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_DISTANCE, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg2 = DistanceSenosorsReadings()
				msg2.stamp = rospy.get_rostime()
				msg2.distance = data
				distance_readingsPub.publish(msg2)
			else:
				rospy.logwarn("get from %s with params %s failed", URL_DISTANCE, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_DIGITALINPUTARRAY, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg3 = DigitalReadings()
				msg3.stamp = rospy.get_rostime()
				msg3.values = data
				digital_readingsPub.publish(msg3)
			else:
				rospy.logwarn("get from %s with params %s failed", URL_DIGITALINPUTARRAY, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_CURRENT, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg4 = PowerReadings()
				msg4.current = data["current"]
			else:
				rospy.logwarn("get from %s with params %s failed", URL_CURRENT, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		try:
			r = requests.get(url = URL_POWER, params = PARAMS)
			if r.status_code == requests.codes.ok:
				data = r.json() 
				msg4.stamp = rospy.get_rostime()
				msg4.empty = data["batteryLow"]
				msg4.voltage = data["voltage"]
				power_readingsPub.publish(msg4)
			else:
				rospy.logwarn("get from %s with params %s failed", URL_POWER, PARAMS)
		except requests.exceptions.RequestException as e:
			rospy.logerr("%s", e)
			pass
		rate.sleep()

if __name__ == '__main__':
	myargv = rospy.myargv(argv=sys.argv)
	if len(myargv)>1:
		URL = URL_BUMPER.replace("172.27.1.1",myargv[1])
	print("connecting to: ",URL_BUMPER)
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
