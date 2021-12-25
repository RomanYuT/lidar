#  модуль для обработки 2х лидаров в функциях
import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import PyLidar3
import time # Time module

#объединение данных с 2х лидаров и обрезка


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




