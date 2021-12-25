#function are needing for work 1-4 lidars

import os
from math import cos, sin, pi, floor
import pygame
import PyLidar3
import time
import matplotlib.pyplot as plt

import json
import pickle

# функции для загрузки данных из файлов разных лидаров
def load_yd(filename='YDlidar.txt',saving=False): #old version
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

def load_ydnew(filename='lidar_top_right-0.json',saving=False): #new ver
     # YDlidar.txt
    
    data_yd=[]
    with open(filename, 'r') as file:
            items = json.load(file)

    for data in items:
        point_data=[]
        for point in data.get('points'):
            # Distance set to 0 when measurment is invalid.
            # Skip distances more than 3m.
            if (point.get('distance', 0) == 0):
                continue

            distance = point.get('distance')
            angle = point.get('angle')
                
            point_data.append([angle,distance])
        data_yd.append(point_data)
                
            
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


def pygame_init():

    import pygame
    # Screen width & height
    W = 640
    H = 480
    global lcd
    # Set up pygame and the display
    #os.putenv('SDL_FBDEV', '/dev/fb1')
    pygame.display.init()
    lcd = pygame.display.set_mode((W,H))
    pygame.mouse.set_visible(False)
    lcd.fill((200,0,0))
    pygame.display.update()


def mplt_init():
    #создание графиков
    fig = plt.figure() 

    ax=fig.add_subplot(111)
    plt.xlim([xw1, xw2])
    plt.ylim([yw1,yw2])
    plt.grid(True)

def mplot(): # do for 4 lidar
##     cs=plt.scatter(*dataxy_1pair.dataxy_1pair(data1,data2,
##                                              x1=x1,y1=y1,
##                                              dist_lidx=dist_lidx,
##                                              dist_lidy=dist_lidy,
##                                              xw1=xw1,yw1=yw1,
##                                              xw2=xw2,yw2=yw2)
    return None


# Screen width & height
W = 640
H = 480
#print(5)
limdist=900
max_distance=5000
x1=0;y1=0; x2=400;y2=-400;
fi01=0;fi02=0
    
def process_data(data1,data2): #добавить для 4х лидаров
    global max_distance
    lcd.fill((0,0,0))
    point = ( int(W / 2) , int(H / 2) )
    #print(800)
    pygame.draw.circle(lcd,pygame.Color(255, 255, 255),point,10 ,1)
    pygame.draw.circle(lcd,pygame.Color(100, 100, 100),point,100 , 2 )
    pygame.draw.circle(lcd,pygame.Color(0, 0, 250),
                       ( int(W / 2) + int((x1) / max_distance * (W/2)),
                         int(H/2) + int((y1) / max_distance * (H/2) )),
                       5,3  )
    pygame.draw.circle(lcd,pygame.Color(0, 250, 0),
                       ( int(W / 2) + int((x2) / max_distance * (W/2)), int(H/2) + int((y2) / max_distance * (H/2) )),
                       5 , 3 )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( 0, int(H/2)),( W , int(H/2) ) )
    pygame.draw.line( lcd,pygame.Color(100, 100, 100) , ( int(W/2),0),( int(W/2) , H ) )
    pygame.display.update()

    for ind_p in range(len(data1)):
        #print('data1',data1)
        #print('len(data1),data1[0]',len(data1),data1[0])
        distance1 = data1[ind_p][1]
        angle=data1[ind_p][0]
        if distance1 > 0:                  # ignore initially ungathered data points
            #max_distance = max([min([limdist, distance1]), max_distance])
            radians = (angle+fi01) * pi / 180.0
            x = distance1 * cos(radians)
            y = distance1 * sin(radians)
            point = ( int(W / 2) + int((x+x1) / max_distance * (W/2)), int(H/2) + int((y+y1) / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(0, 0, 255),point,2 )
            #print('ind_p=',ind_p)
            #print('coord1',ind_p,data1[ind_p],x,y)

    for ind_p in range(len(data2)):
        distance2 = data2[ind_p][1]
        angle=data2[ind_p][0]
        if distance2 > 0:                  # ignore initially ungathered data points
            #max_distance = max([min([limdist, distance1]), max_distance])
            radians = (angle+fi02) * pi / 180.0
            x = distance2 * cos(radians)
            y = distance2 * sin(radians)
            point = ( int(W / 2) + int((x+x2) / max_distance * (W/2)), int(H/2) + int((y+y2) / max_distance * (H/2) ))
            pygame.draw.circle(lcd,pygame.Color(0, 255, 0),point,2 )
            #print('point2',x,y)
    pygame.display.update()
    time.sleep(0.1)



    def dataxy_1pair(turn1,turn2,x1,y1,dist_lidx,dist_lidy,xw1,yw1,xw2,yw2):
        fi01=0
        fi02=0
        turn1=np.array(turn1)
        turn2=np.array(turn2)
        datax=datay=dataxy1=dataxy2=np.array([])
        
        if len(turn1):
            dataxy1=[[r*np.cos((fi01+fi)*np.pi/180)+x1,r*np.sin((fi01+fi)*np.pi/180)+y1]
                    for fi,r in turn1
                   if xw1<r*np.cos((fi01+fi)*np.pi/180)+x1<xw2 and
                    yw1<r*np.sin((fi01+fi)*np.pi/180)+y1<yw2]

    
        if len(turn2):
            dataxy2=[[r*np.cos((fi02+fi)*np.pi/180)+x1+dist_lidx,
                        r*np.sin((fi02+fi)*np.pi/180)+y1+dist_lidy]
                        for fi,r in turn2
                       if xw1<r*np.cos((fi02+fi)*np.pi/180)+x1+dist_lidx<xw2 and
                        yw1<r*np.sin((fi02+fi)*np.pi/180)+y1+dist_lidy<yw2]
            
        return {'time':time.time(),1:dataxy1, 2:dataxy2}


def rec_data():
    with open('data_yd', 'wb') as f:
            pickle.dump(data_yd, f)
        
