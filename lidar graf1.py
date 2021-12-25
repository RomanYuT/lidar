#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
import numpy
import matplotlib.animation as animation
import time

with open('data_rp', 'rb') as f:
    data_rp = pickle.load(f)

#объединение данных с 2х лидаров и обрезка
shiftx1=0 #смещение 1го лидара  от начала координат по оси х, см
shifty1=0  # мещение 1го лидара  от начала координат по оси у, см
dist_lidx=150 # горизонтальное расстояние между лидарами, см
dist_lidy=100 # вертикальное расстояние между лидарами, см

def dataxy_1pair(turn1,turn2,shiftx1=0,shifty1=0,dist_lidx=0.5,lidar_type1='rp',lidar_type2='rp'):
    angle_list1=list(range(270,360))+[0] #диапазон углов от 270 до 360 градусов
    angle_list2=list(range(180,271)) #диапазон углов от 180 до 270 градусов
    turn1=np.array(turn1)
    turn2=np.array(turn2)
    datax=datay=np.array([])
    
    if len(turn1):
        if lidar_type1=='rp':
            datax=[r*np.cos(fi*np.pi/180)+shifty1 for fi,r in zip(angle_list1, turn1[angle_list1])]
            datay=[r*np.sin(fi*np.pi/180)+shifty1 for fi,r in zip(angle_list1, turn1[angle_list1])]

        else:
            datax=[r*np.cos(fi*np.pi/180)+shiftx1 for fi,r in turn1[angle_list1]]
            datay=[r*np.sin(fi*np.pi/180)+shifty1 for fi,r in turn1[angle_list1]]
    
    if len(turn2):
        if lidar_type2=='rp':
            datax=np.r_[datax, [r*np.cos(fi*np.pi/180)+shiftx1+dist_lidx for fi,r in zip(angle_list2, turn2[angle_list2])]]
            datay=np.r_[datay, [r*np.sin(fi*np.pi/180)+shifty1 for fi,r in zip(angle_list2, turn2[angle_list2])]]
        else:
            datax=np.r_[datax, [r*np.cos(fi*np.pi/180)+shiftx1+dist_lidx for fi,r in turn2[angle_list2]]]
            datay=np.r_[datay, [r*np.sin(fi*np.pi/180)+shifty1 for fi,r in turn2[angle_list2]]]
    
    return datax,datay


fig = plt.figure() #figsize=(19,5)

ax=fig.add_subplot(111)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([-dist_lidy-shifty1, -shifty1])
plt.grid(True)
  
def animate(n):
    ax.clear()
    plt.plot(0,0,'ro')
##    cs=plt.scatter(*dataxy_1pair(data_rp[n][:360],
##                              [],
##                              lidar_type2='yd',dist_lidx=dist_lidx))
    #plt.pause(0.05)
    #plt.draw()
    print(time.time()-t)
    plt.text(0,0,time.time()-t)
    
    #ax1.plot(xar,yar)
t=time.time()    
ani = animation.FuncAnimation(fig, animate,frames = 10,
                              interval=10,repeat=False,)
plt.show()
print(time.time()-t)
