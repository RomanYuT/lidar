import lidar_func as ldf

is_test=1




data_full1=ldf.load_ydnew('lidar_top_left-3.json')
data_full2=ldf.load_ydnew('lidar_top_right-0.json')

#data_full1=[data_full1[0][:]]

#print('len(data_full1),len(data_full1[0]),data_full1[0]',len(data_full1),len(data_full1[0]),data_full1[0])
#print('len(data_full2),len(data_full2[0]),data_full2[0]',len(data_full2),len(data_full2[0]),data_full2[0])


try:
    if is_test:
        ldf.pygame_init()
        #print(min( len(data_full1),len(data_full2)))
        for k in range(min( len(data_full1),len(data_full2))):
            ldf.process_data(data_full1[k],
                             data_full2[k])

    else:
        
        if(Obj.Connect()):
            gen = Obj.StartScanning()
            while True:
                    line=next(gen)
                    scan_data2=[s for s in line.values()]
                    scan_data1=sample0YD_1.data_lidar1
                    if len(scan_data1) and len(scan_data1):
                            process_data(scan_data1,scan_data2)
        else:
            print("Error connecting to device")    

except KeyboardInterrupt:
    print('Stopping.')        
