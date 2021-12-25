from time import sleep
import time
import matplotlib.pyplot as plt

#print('2cimpimpimpimpimpimp')
# from script1 import motorspeed will not work
#import pri_yeld


#print('2c2c2c2c2c2c2c2c2c')

def random_increase(quantity):
    cur = 0
    print(quantity,'up func***222',)
    def ggg(x):
        dataxy1=[[x-5, x+5] for x in range(int(time.time()*10000000)%7+2)]
        #print(time.time(),int(time.time()*10000000)%7+2,quantity,'down fun+++222')
        dataxy2=[[x-3, x*2] for x in range(int(time.time()*10000000)%3+2)]
        #print(time.time(),end='\n\n')

##        datax2=[[x-5, x+5] for x in range(int(time.time()*10000)%5+6)]
##        datay2=[[x-5, x+5] for x in range(int(time.time()*10000)%3+6)]
        return {'time':time.time(),1:dataxy1,
                2:dataxy2}
    while quantity > 0:
        cur += 5
        quantity -= 1
        yield ggg(cur)

while True:
    
    #print('222while222while222while')
    
    
    #def out_numb():
    #global motorspeed
    a=random_increase(7)
    for i in random_increase(5):
        #print(i[1],next(a),'222forforforforforforforforforforforfor')
        #print(*i[0],i[1])
        x=[]; y=[]
       
        for lid in range(1,3):
            for k in i[lid]:
               
                x+=[k[0]]
                y+=[k[1]]
                cs=plt.scatter(x,y,c=[[1,0,0]]) #,c=[5,5,5] if lid==1 else 7)
                #pri_yeld.motorspeed
    ##    cs=plt.scatter(x,y)
##        i=pri_yeld.motorspeed
##        x=[]; y=[]
##        for lid in range(1,3):
##            for k in i[lid]:
##               
##                x+=[k[0]]
##                y+=[k[1]]
##                cs=plt.plot(x,y)
        plt.pause(1)

    
plt.show()
