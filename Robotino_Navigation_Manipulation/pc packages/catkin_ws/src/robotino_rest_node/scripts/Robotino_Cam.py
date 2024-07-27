#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20/5/22
"""
# import cv2
# import urllib.request
# import numpy as np
# import time
# while 1 :
#     req = urllib.request.urlopen('http://172.27.1.1/cam0')
#     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#     img = cv2.imdecode(arr, -1) # 'Load it as it is'

#     cv2.imshow('image_test', img)
#     # time.sleep(0.05)
#     if cv2.waitKey(1) & 0xff == 27: quit()
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import urllib.request
import numpy as np
import time

rospy.init_node('VideoPublisher', anonymous=True)
VideoRaw = rospy.Publisher('Robotino_Camera', Image, queue_size=10)

while 1 :
    while not rospy.is_shutdown():
        req = urllib.request.urlopen('http://172.27.1.1/cam0')
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'

        msg_img=CvBridge().cv2_to_imgmsg(img)
        VideoRaw.publish(msg_img)

        # cv2.imshow('image_test', img)
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xff == 27: quit()
