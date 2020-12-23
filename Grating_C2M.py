def grating_C2M(cs):
  
#Function to retrieve serial communication data from Arduino.


import numpy as np

#Retrieve all serial data waiting in the cache
 while ser.in_waiting >0 :
    msgtype = ser.read()
    if msgtype == 200 : #version number
        Bytes = ser.read(4)
        versionID = np.uint32(Bytes)
        print(f"Arduino program version ID: {versionID}  \n")
    elif msgtype == 201 : #display start; record parameters and timestamp
        Bytes = ser.read(4)
        counter = np.uint32(Bytes) #counter for number of controller starts
        Bytes = ser.read(4) 
        time = np.uint32(Bytes) #start timestamp from controller
        readdelay = ser.read(1)
        bar1color = ser.read(3)
        bar2color = ser.read(3)
        backgroundcolor = ser.read(3)
        barwidth = ser.read(1)
        numgratings = ser.read(1)
        angle2b = ser.read(2)
        frequency = ser.read(1)/10
        position = ser.read(2)
        predelay = ser.read(1)/10
        duration = ser.read(1)/10
        output = ser.read(1)*5/255
        angle = sum(angle2b)
        Bytes = ser.read(4)
        benchmark = np.uint32(Bytes)
                    
        #for flicker, change all irrelevant parameters to empty
        if numgratings==0 :
            bar1color = np.empty([1,3])
            bar2color = np.empty([1,3])
            barwidth = None
            position = None
            angle = None
            benchmark = None   
        #save current data and parameters
        if hasattr(cs,'trial')==True:
            trial = cs.trial
        else:
            trial = 0
                    
        if hasattr(cs,'rep')==True:
            rep = cs.rep
        else:
            rep = 0
                            
            addData = np.array([counter, time, 
            trial, rep, readdelay, bar1color, bar2color, 
            backgroundcolor, barwidth, numgratings, angle, frequency, position, 
            predelay, duration, output, benchmark]) 
            np.vstack = (cs.data, addData)  
    elif msgtype == 225 :
        ID = ser.read(1)
        cache = {}
        while ser.in_waiting > 0 :
            cache = [cache , ser.read(1)]
            print (f"ID: {ID}")   
        raise ValueError(f"message type ID ({ID}) not recognized by controller. cache cleared ({cache}).")     
    else:
        cache = {}
        while ser.in_waiting > 0 :
        cache = [cache , ser.read(1)]
               
        raise ValueError(f"message type from controller not recognized ({msgtype}). cache cleared ({cache}).")

    
   
        
    

    