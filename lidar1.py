#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
fi1=270
fi2=360


# load data from files
def load_yd(filename='YDlidar.txt',saving=False):
     #output3 YDlidar.txt
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
    filenamerp=r'output3'  #RPLidar.txt
    data_rp=[]

    with open(filenamerp, mode='r') as filestr:
        #print(filestr[:60])
        k=0
        for l in filestr:
            if 'Stopping' not in l:
                data_rp.append(json.loads(l))
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
    


data_yd=load_yd()
data_rp=load_rp()
    

fig = plt.figure(figsize=(18,5))
ax1=fig.add_subplot(131, projection='polar')
#plt.scatter([1,2,3], [2,1,1])
ax1.set_title(' yd fi,r')

for n in range(len(data_yd)):
    ax1.scatter([x[0]/(180/3.1415) for x in data_yd[n][:360]],
                [x[1] for x in data_yd[n][:360]])
    plt.pause(0.001)




ax3=fig.add_subplot(133, projection='polar')
ax3.set_title(' rp r')               
#plt.scatter([1,2,3], [2,1,1])
data_rpflat=[item for sublist in data_rp for item in sublist]
#for n in range(len(data_rp)):
plt.scatter([fi/(180/3.1415) for fi in list(range(360))*311],
            data_rpflat)
plt.pause(0.001)


ax2=fig.add_subplot(132)
plt.xlim([-shiftx1, dist_lidx-shiftx1])
plt.ylim([-dist_lidy-shifty1, -shifty1])
plt.grid(True) 
#plt.scatter([1,2,3], [2,1,1])
for n in range(5):
    plt.scatter(*dataxy_1pair(data_rp[n][:360],data_yd[n][:360],lidar_type2='yd',dist_lidx=dist_lidx))
    plt.pause(0.01)
plt.show()
        
