#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle



# функции для загрузки данных из файлов разных лидаров
def load_yd(filename='YDlidar.txt',saving=False):
     # YDlidar.txt
    data_yd=[]
    with open(filename, mode='r') as filestr:
        k=0
        for l in filestr:
           # print(k)
            if k!=0:
                data_yd.append([[int(s.split(':')[0]), int(s.split(':')[1])]
                    for s in l.strip('{}\n').split(',')])
                
            k+=1
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
    


#загрузка данных из любых файлов
data_right=load_rp()
data_left=load_yd()
data_left_fl=[item for sublist in data_left for item in sublist][:1] #[:360] -сколько оборотов строим в градусах
data_right_fl=[item for sublist in data_right for item in sublist][:1]


#создание графиков
fig = plt.figure(figsize=(18,6))
ax1=fig.add_subplot(131, projection='polar')
ax1.set_title('left lidar')
ax1.set_ylim(0,700)
ax1.scatter([x[0]/(180/3.1415) for x in data_left_fl],
            [x[1] for x in data_left_fl])


ax3=fig.add_subplot(133, projection='polar')
ax3.set_title(' right lidar')               
ax3.set_ylim(0,700)

ax3.scatter([x[0]/(180/3.1415) for x in data_right_fl],
            [x[1] for x in data_right_fl])


ax2=fig.add_subplot(132)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([dist_lidy-shifty1, -shifty1])
plt.grid(True)
ax2.set_title('1 and 2 lidar')

plt.scatter(*dataxy_1pair(data_left_fl,data_right_fl,dist_lidx=dist_lidx))
print(*dataxy_1pair(data_left_fl,data_right_fl,dist_lidx=dist_lidx))
plt.pause(0.01)
plt.plot(-shiftx1,-shifty1,'go',alpha=0.3,markersize=30)
plt.plot(-shiftx1+dist_lidx,-shifty1+dist_lidy,'ro',alpha=0.3,markersize=30)
plt.text(-shiftx1,-shifty1,' left lidar')
plt.text(-shiftx1+dist_lidx,-shifty1+dist_lidy,' right lidar')

plt.show()
        
