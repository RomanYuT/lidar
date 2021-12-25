#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
import data_pair



# функции для загрузки данных из файлов разных лидаров
def load_yd(filename='YDlidar.txt',saving=False):
     # YDlidar.txt
    data_yd=[]
    with open(filename, 'r') as file:
            items = json.load(file)

    for data in items:
        for point in data.get('points'):
            # Distance set to 0 when measurment is invalid.
            # Skip distances more than 3m.
            if (point.get('distance', 0) == 0):
                continue

            distance = point.get('distance')
            angle = point.get('angle')
                
            data_yd.append([angle,distance])
                
            
    if saving==True:
        with open('data_yd', 'wb') as f:
            pickle.dump(data_yd, f)
    return data_yd



def load_rp(filename='output3',saving=False):
    #RPLidar.txt    output3   output4
    data_rp=[]

    with open(filename, mode='r') as filestr:
        #print(filestr[:60])
        k=0
        for l in filestr:
            if 'Stopping' not in l:
                data_rp.append([[ind,item]
                               for ind,item in enumerate(json.loads(l))])
            else:
                break
            k+=1
    if saving==True:
        with open('data_rp', 'wb') as f:
            pickle.dump(data_rp, f)
    return data_rp



#объединение данных с 2х лидаров и обрезка
shiftx1=0 #смещение 1го лидара  от начала координат по оси х, см
shifty1=0  # мещение 1го лидара  от начала координат по оси у, см
dist_lidx=400 # горизонтальное расстояние между лидарами, см
dist_lidy=-400 # вертикальное расстояние между лидарами, см


    


#загрузка данных из любых файлов
data_right=load_yd()
data_left=load_yd(filename='output4')
data_left_fl=data_right[:360] #[:360] -сколько оборотов строим в градусах
data_right_fl=data_left[:360]

x1=-2400,y1=320,x2=3865,y2=340,xw1=-1800,yw1=200,xw2=2000,yw2=3800
dist_lidx=x2-x1
dist_lidy=y2-y1

    
#создание графиков
fig = plt.figure(figsize=(18,6))
ax1=fig.add_subplot(131, projection='polar')
ax1.set_title('left lidar')
ax1.set_ylim(0,500)
ax1.scatter([x[0]/(180/3.1415) for x in data_left_fl],
            [x[1] for x in data_left_fl])


ax3=fig.add_subplot(133, projection='polar')
ax3.set_title(' right lidar')               
ax3.set_ylim(0,500)

ax3.scatter([x[0]/(180/3.1415) for x in data_right_fl],
            [x[1] for x in data_right_fl])


ax2=fig.add_subplot(132)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([dist_lidy-shifty1, -shifty1])
plt.grid(True)
ax2.set_title('1 and 2 lidar')

plt.scatter(*dataxy_1pair(data_left_fl,data_right_fl,x1=-2400,y1=320,
                          dist_lidx=dist_lidx,dist_lidy=dist_lidy,
                          xw1=-1800,yw1=200,xw2=2000,yw2=3800))
plt.pause(0.01)
plt.plot(-shiftx1,-shifty1,'go',alpha=0.3,markersize=30)
plt.plot(-shiftx1+dist_lidx,-shifty1+dist_lidy,'ro',alpha=0.3,markersize=30)
plt.text(-shiftx1,-shifty1,' left lidar')
plt.text(-shiftx1+dist_lidx,-shifty1+dist_lidy,' right lidar')

plt.show()
        
