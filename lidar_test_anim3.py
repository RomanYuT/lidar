#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
import matplotlib.animation as animation
import time
from lidar_edit_data import load_rp,dataxy_1pair


#объединение данных с 2х лидаров и обрезка
shiftx1=0 #смещение 1го лидара  от начала координат по оси х, см
shifty1=0  # мещение 1го лидара  от начала координат по оси у, см
dist_lidx=400 # горизонтальное расстояние между лидарами, см
dist_lidy=400 # вертикальное расстояние между лидарами, см




#загрузка данных из любых файлов
data_right=load_rp(filename='output4')
data_left=load_rp()
data_left_fl=[item for sublist in data_left for item in sublist][:] 
data_right_fl=[item for sublist in data_right for item in sublist][:]
#[:360] -сколько оборотов строим в градусах


#создание графиков
fig = plt.figure() 

ax=fig.add_subplot(111)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([-dist_lidy-shifty1, -shifty1])
plt.grid(True)
  

t=time.time()
for n in range(min(len(data_left_fl)//360,len(data_right_fl)//360)):
    ax.clear()
    plt.xlim([-shiftx1, dist_lidx-shiftx1])
    plt.ylim([-dist_lidy-shifty1, -shifty1])
    plt.grid(True)

    cs=plt.scatter(*dataxy_1pair(data_left_fl[n*360:(n+1)*360],
                                 data_right_fl[n*360:(n+1)*360],
                                 dist_lidx=dist_lidx))
    plt.pause(0.1)
    print(time.time()-t)



plt.show()
        

