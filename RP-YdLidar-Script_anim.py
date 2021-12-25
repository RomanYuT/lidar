import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import PyLidar3
import time # Time module

#объединение данных с 2х лидаров и обрезка
shiftx1=0 #смещение 1го лидара  от начала координат по оси х, см
shifty1=0  # мещение 1го лидара  от начала координат по оси у, см
dist_lidx=400 # горизонтальное расстояние между лидарами, см
dist_lidy=400 # вертикальное расстояние между лидарами, см

def dataxy_1pair(turn1,turn2,shiftx1=0,shifty1=0,dist_lidx=0.5):
    angle_list1=list(range(270,360))+[0] #диапазон углов от 270 до 360 градусов
    angle_list2=list(range(90,181)) #диапазон углов от 180 до 270 градусов
    turn1=np.array(turn1)
    turn2=np.array(turn2)
    datax=datay=np.array([])
    
    if len(turn1):
        for k in range(len(turn1)//360):
            datax=[r*np.cos(fi*np.pi/180)+shiftx1 for fi,r in turn1[[k*360+n for n in angle_list1]]]
            datay=[r*np.sin(fi*np.pi/180)+shifty1 for fi,r in turn1[[k*360+n for n in angle_list1]]]
    
    if len(turn2):
        for k in range(len(turn2)//360):
            datax=np.r_[datax, [r*np.cos(fi*np.pi/180)+shiftx1+dist_lidx
                                for fi,r in turn2[[k*360+n for n in angle_list2]]]]
            datay=np.r_[datay, [r*np.sin(fi*np.pi/180)+shifty1+dist_lidy
                                for fi,r in turn2[[k*360+n for n in angle_list2]]]]
    return datax,datay

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Setup the YdLidar
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)

# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_data = [[0,0]]*360


#создание графиков
fig = plt.figure() 

ax=fig.add_subplot(111)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([-dist_lidy-shifty1, -shifty1])
plt.grid(True)


try:
#    print(lidar.get_info())
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = [min([359, floor(angle)]),distance]
            process_data(scan_data)

            line=next(gen)
            data_yd.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                    for s in line.strip('{}\n').split(',')])
            
            ax.clear()
            plt.xlim([-shiftx1, dist_lidx-shiftx1])
            plt.ylim([dist_lidy-shifty1, -shifty1])
            plt.grid(True)
            cs=plt.scatter(*dataxy_1pair(scan_data,data_yd,
                                         dist_lidx=dist_lidx))
            plt.pause(0.1)
        Obj.StopScanning()
        Obj.Disconnect()
    else:
    print("Error connecting to device")
        
except KeyboardInterrupt:
    print('Stopping.')
plt.show()
lidar.stop()
lidar.disconnect()

