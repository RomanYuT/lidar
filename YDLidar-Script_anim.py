import PyLidar3
import time # Time module
import matplotlib.pyplot as plt
import numpy as np
port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)


#объединение данных с 2х лидаров и обрезка
shiftx1=0 #смещение 1го лидара  от начала координат по оси х, см
shifty1=0  # мещение 1го лидара  от начала координат по оси у, см
dist_lidx=400 # горизонтальное расстояние между лидарами, см
dist_lidy=400 # вертикальное расстояние между лидарами, см

def dataxy_1pair(turn1,turn2,shiftx1=0,shifty1=0,dist_lidx=0.5):
    angle_list1=list(range(270,360))+[0] #диапазон углов от 270 до 360 градусов
    angle_list2=list(range(180,271)) #диапазон углов от 180 до 270 градусов
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
            datay=np.r_[datay, [r*np.sin(fi*np.pi/180)+shifty1
                                for fi,r in turn2[[k*360+n for n in angle_list2]]]]
    return datax,datay

#создание графиков
fig = plt.figure() 

ax=fig.add_subplot(111)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([-dist_lidy-shifty1, -shifty1])
plt.grid(True)


if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        line=next(gen)
        data_yd.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                    for s in line.strip('{}\n').split(',')])
        print(s)
        ax.clear()
        plt.xlim([-shiftx1, dist_lidx-shiftx1])
        plt.ylim([-dist_lidy-shifty1, -shifty1])
        plt.grid(True)
        cs=plt.scatter(*dataxy_1pair(data_yd,[], dist_lidx=dist_lidx))
        plt.pause(0.001)
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
