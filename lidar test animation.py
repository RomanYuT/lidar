#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import json
import pickle
import matplotlib.animation as animation


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
  
def animate(n):
    ax.clear()
    plt.xlim([-shiftx1, dist_lidx-shiftx1])
    plt.ylim([-dist_lidy-shifty1, -shifty1])
    plt.grid(True)

    cs=plt.scatter(*dataxy_1pair(data_left_fl[n*360:(n+1)*360],
                                 data_right_fl[n*360:(n+1)*360],
                                 dist_lidx=dist_lidx))


ani = animation.FuncAnimation(fig, animate,
                              frames = min(len(data_left_fl)//360,
                                           len(data_right_fl)//360),
                              interval=10,repeat=False,)
plt.show()
        
