import time
import matplotlib.pyplot as plt
from threading import Thread

print('111111111cript^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
def random_increase(quantity):
    cur = 0
    print('1111quantity=quantity=quantity=',quantity,'quantity=!up func***',)
    def ggg(x):
        dataxy1=[[x-5, x+5] for x in range(int(time.time()*10000000)%7+20)]
        print('11111111111111111111111111',
              time.time(),int(time.time()*10000000)%7+2,quantity,
              '11111111down fun+++11')
        dataxy2=[[x-3, x*2] for x in range(int(time.time()*10000000)%3+20)]
        #print(time.time(),end='\n\n')

##        datax2=[[x-5, x+5] for x in range(int(time.time()*10000)%5+6)]
##        datay2=[[x-5, x+5] for x in range(int(time.time()*10000)%3+6)]
        return {'time':time.time(),1:dataxy1,
                2:dataxy2}
    while quantity > 0:
        print('1111whilerandom_increase',)
        cur += 5
        quantity -= 1
        yield ggg(cur)

motorspeed=0
def out_numb():
    print('11111111def out_numbdef out_numbdef out_numbdef out_numbdef out_numb')
    global motorspeed
    a=random_increase(7)
    for i in random_increase(5):
        print(i[1],next(a),'----111')
        #print(*i[0],i[1])
        x=[]; y=[]
        motorspeed=i
        time.sleep(1)
        for lid in range(1,3):
            for k in i[lid]:
               
                x+=[k[0]]
                y+=[k[1]]
                #cs=plt.scatter(x,y) #,c=[5,5,5] if lid==1 else 7)
    ##    cs=plt.scatter(x,y)
        #plt.pause(1)

    
#plt.show()
print('111111111befthreadbefthreadbefthreadbefthreadbefthread')
Thread(target=out_numb).start()
