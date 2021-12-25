#  модуль для обработки 2х лидаров в функциях
import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import PyLidar3
import time # Time module

#объединение данных с 2х лидаров и обрезка
dataxy_1pair(x1=-2400,y1=320,x2=3865,y2=340,xw1=-1800,yw1=200,xw2=2000,yw2=3800,
             type_lidar1='rp', type_lidar2='rp',port_lidar1='/dev/ttyUSB7',
             port_lidar2='/dev/ttyUSB14'):
dist_lidx=x2-x1
dist_lidy=y2-y1 #смещение 2 относительно 1го лидара

def dataxy_1pair(turn1,turn2,x1,y1,dist_lidx,dist_lidy,xw1,yw1,xw2,yw2):

    
    fi01=0
    fi02=0
    turn1=np.array(turn1)
    turn2=np.array(turn2)
    datax=datay=dataxy=np.array([])
    
    if len(turn1):
        dataxy=[[r*np.cos((fi01+fi)*np.pi/180)+x1,r*np.sin((fi01+fi)*np.pi/180)+y1]
            for fi,r in turn1
           if xw1<r*np.cos((fi01+fi)*np.pi/180)+x1<xw2 and
            yw1<r*np.sin((fi01+fi)*np.pi/180)+y1<yw2]


    if len(turn2):
        dataxy+=[[r*np.cos((fi02+fi)*np.pi/180)+x1+dist_lidx,
                    r*np.sin((fi02+fi)*np.pi/180)+y1+dist_lidy]
                    for fi,r in turn2
                   if xw1<r*np.cos((fi02+fi)*np.pi/180)+x1+dist_lidx<xw2 and
                    yw1<r*np.sin((fi02+fi)*np.pi/180)+y1+dist_lidy<yw2]
        datax,datay=np.hsplit(np.array(dataxy),2)
    return [datax,datay]


if type_1lidar=='pr':
    # Setup the RPLidar
    PORT_NAME = port_lidar1
    lidar1 = RPLidar(None, PORT_NAME, timeout=3)
elif type_1lidar=='yd':
     # Setup the YdLidar
    port = port_lidar1 #linux
    Obj1 = PyLidar3.YdLidarX4(port)

if type_lidar2=='pr':
    PORT_NAME = port_lidar2
    lidar2 = RPLidar(None, PORT_NAME, timeout=3)
elif type_lidar2=='yd':
    # Setup the YdLidar
    port = port_lidar2 #linux
    Obj2 = PyLidar3.YdLidarX4(port)
    




scan_data = [[0,0]]*360


#создание графиков
fig = plt.figure() 

ax=fig.add_subplot(111)
plt.xlim([xw1, xw2])
plt.ylim([yw1,yw2])
plt.grid(True)


try:
    data1=[]; data2=[];
    if type_lidar1==type_lidar2 and type_lidar1=='rp':
        scan_data1=scan_data2 = [[0,0]]*360
        for scan1,scan1 in zip(lidar1.iter_scans(),lidar2.iter_scans()):
            for (_, angle, distance) in scan:
                scan_data1[min([359, floor(angle)])] = [min([359, floor(angle)]),distance]
            for (_, angle, distance) in scan:
                scan_data2[min([359, floor(angle)])] = [min([359, floor(angle)]),distance]
            data1=scan_data1
            data2=scan_data2
            yield dataxy_1pair(data1,data2,x1=x1,y1=y1,dist_lidx=dist_lidx,dist_lidy=dist_lidy,
                         xw1=xw1,yw1=yw1,xw2=xw2,yw2=yw2)
            ax.clear()
            plt.xlim([xw1, xw2])
            plt.ylim([yw1,yw2])
            plt.grid(True)
            cs=plt.scatter(*dataxy_1pair.dataxy_1pair(data1,data2,
                                                      x1=x1,y1=y1,
                                                      dist_lidx=dist_lidx,
                                                      dist_lidy=dist_lidy,
                                                      xw1=xw1,yw1=yw1,
                                                      xw2=xw2,yw2=yw2))
            plt.pause(0.1)

        
    elif type_lidar1!=type_lidar2:
        if type_lidar1=='rp':
            
            if(Obj2.Connect()):
                gen = Obj2.StartScanning()

                data_yd=[]
                scan_data = [[0,0]]*360
                for scan in lidar1.iter_scans():
                    for (_, angle, distance) in scan:
                        scan_data[min([359, floor(angle)])] = [min([359, floor(angle)]),distance]
                    
                    line=next(gen)
                    data_yd.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                            for s in line.strip('{}\n').split(',')])

                    data1=scan_data
                    data2=data_yd
                    yield dataxy_1pair(data1,data2,x1=x1,y1=y1,dist_lidx=dist_lidx,dist_lidy=dist_lidy,
                             xw1=xw1,yw1=yw1,xw2=xw2,yw2=yw2)

                    ax.clear()
                    plt.xlim([xw1, xw2])
                    plt.ylim([yw1,yw2])
                    plt.grid(True)
                    cs=plt.scatter(*dataxy_1pair.dataxy_1pair(data1,data2,
                                                              x1=x1,y1=y1,
                                                              dist_lidx=dist_lidx,
                                                              dist_lidy=dist_lidy,
                                                              xw1=xw1,yw1=yw1,
                                                              xw2=xw2,yw2=yw2))
                    plt.pause(0.1)
                    
                Obj.StopScanning()
                Obj.Disconnect()

                    
                
            else:
            print("Error connecting to device")

        else:
            if(Obj1.Connect()):
                gen = Obj1.StartScanning()
                
                for scan in lidar2.iter_scans():
                    for (_, angle, distance) in scan:
                        scan_data[min([359, floor(angle)])] = [min([359, floor(angle)]),distance]
                    
                    line=next(gen)
                    data_yd.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                            for s in line.strip('{}\n').split(',')])
                    
                    data1=data_yd
                    data2=scan_data
                    yield dataxy_1pair(data1,data2,x1=x1,y1=y1,dist_lidx=dist_lidx,dist_lidy=dist_lidy,
                             xw1=xw1,yw1=yw1,xw2=xw2,yw2=yw2)

                    ax.clear()
                    plt.xlim([xw1, xw2])
                    plt.ylim([yw1,yw2])
                    plt.grid(True)
                    cs=plt.scatter(*dataxy_1pair.dataxy_1pair(data1,data2,
                                                              x1=x1,y1=y1,
                                                              dist_lidx=dist_lidx,
                                                              dist_lidy=dist_lidy,
                                                              xw1=xw1,yw1=yw1,
                                                              xw2=xw2,yw2=yw2))
                    plt.pause(0.1)
                    
                Obj.StopScanning()
                Obj.Disconnect()

                

                
            else:
            print("Error connecting to device")

    else:
        
        if(Obj1.Connect()) and (Obj2.Connect()):
            gen1 = Obj1.StartScanning()
            gen2 = Obj2.StartScanning()
            
            while True:
                
                line1=next(gen1)
                data1.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                        for s in line1.strip('{}\n').split(',')])

                line2=next(gen2)
                data2.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                        for s in line2.strip('{}\n').split(',')])

                yield dataxy_1pair(data1,data2,x1=x1,y1=y1,dist_lidx=dist_lidx,dist_lidy=dist_lidy,
                             xw1=xw1,yw1=yw1,xw2=xw2,yw2=yw2)

                ax.clear()
                plt.xlim([xw1, xw2])
                plt.ylim([yw1,yw2])
                plt.grid(True)
                cs=plt.scatter(*dataxy_1pair.dataxy_1pair(data1,data2,
                                                          x1=x1,y1=y1,
                                                          dist_lidx=dist_lidx,
                                                          dist_lidy=dist_lidy,
                                                          xw1=xw1,yw1=yw1,
                                                          xw2=xw2,yw2=yw2))
                plt.pause(0.1)
                
                
            Obj.StopScanning()
            Obj.Disconnect()

        else:
        print("Error connecting to device")

        
except KeyboardInterrupt:
    print('Stopping.')
lidar.stop()
lidar.disconnect()
plt.show()

