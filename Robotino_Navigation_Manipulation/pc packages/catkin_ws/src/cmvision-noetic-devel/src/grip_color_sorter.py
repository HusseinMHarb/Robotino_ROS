#! /usr/bin/env python3

import rospy
from cmvision.msg import Blobs

def callback(data):
    try:
        ms=data.blobs[0]
        name=ms.name
        posx=ms.x
        posy=ms.y
        area=ms.area
        # if(2000<area<2300):
        #     print("ok")

        print("color is ",name)
        print("The area is",area)
        print("At posx= ",posx)
        print("posy= ",posy)
        print("--------------------------------------------------------------------")
        print("")
    
    except IndexError:
        print ("no color exist!")


def color_sorter():

    rospy.init_node('color_sorter', anonymous=True)

    rospy.Subscriber("blobs", Blobs, callback)

    rospy.spin()

if __name__ == '__main__':
    color_sorter()
    
