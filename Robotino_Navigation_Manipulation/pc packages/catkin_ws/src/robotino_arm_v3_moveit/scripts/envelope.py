from numpy import *
import numpy as np
a=[0,140,76,77]
resultx=[]
# posx=int()
print("start")

for x in range(0,103,4):
    for y in range(-103,103,4):
        for z in range(-103,103,4):
            posx=a[1]*np.cos(np.deg2rad(x))+a[2]*np.cos(np.deg2rad(x+y))+a[3]*np.cos(np.deg2rad(z))
            posx=round(posx,2)
            # print(posx)
            # resultx.append(posx)
            file = open("posx.txt", "a")

            file.write("%s \n" % str(posx))

file.close()

# print(posx)

print("finsh x position")

for x in range(0,103,4):
    for y in range(-103,103,4):
        for z in range(-103,103,4):
            posy=a[1]*np.sin(np.deg2rad(x))+a[2]*np.sin(np.deg2rad(x+y))+a[3]*np.sin(np.deg2rad(z))
            posy=round(posy,2)
            # print(posx)
            # resultx.append(posx)
            file = open("posy.txt", "a")

            file.write("%s \n" % str(posy))
file.close()

# print(posx)

print("finsh y position")
