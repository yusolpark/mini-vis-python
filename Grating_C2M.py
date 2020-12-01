def grating_C2M(cs):
    '''
    FUNCTION cs = Grating_C2M(cs)
    
    Function to retrieve serial communication data from Arduino.
    '''
    #list of data types retrieved from Arduino
    cs.datanames = {'counter', 'time', 'trial', 'repetition', 'readdelay', 
    'bar1red', 'bar1green', 'bar1blue', 'bar2red', 'bar2green', 'bar2blue', 'backred', 
    'backgreen', 'backblue', 'barwidth', 'numgratings', 'angle', 'frequency', 
    'position1', 'position2', 'predelay', 'duration', 'output', 'benchmark'}
   
    import serial 
    import numpy as np

    with serial.Serial('/dev/cu.usbmodem142101',9600) as ser:
        cs.controller = ser
        #Retrieve all serial data waiting in the cache
        while cs.controller.in_waiting >0 :
            msgtype = cs.controller.read()
            if msgtype == 200 : #version number
                Bytes = cs.controller.read(4)
                versionID = np.uint32(Bytes)
                print(f"Arduino program version ID: {versionID}  \n")
            elif msgtype == 201 : #display start; record parameters and timestamp
                    row = len(cs.data)+1 #next row of data
                    
                    Bytes = cs.controller.read(4)
                    counter = np.uint32(Bytes) #counter for number of controller starts
                    Bytes = cs.controller.read(4) 
                    time = np.uint32(Bytes) #start timestamp from controller
                    readdelay = cs.controller.read(1)
                    bar1color = cs.controller.read(3)
                    bar2color = cs.controller.read(3)
                    backgroundcolor = cs.controller.read(3)
                    barwidth = cs.controller.read(1)
                    numgratings = cs.controller.read(1)
                    angle2b = cs.controller.read(2)
                    frequency = cs.controller.read(1)/10
                    position = cs.controller.read(2)
                    predelay = cs.controller.read(1)/10
                    duration = cs.controller.read(1)/10
                    output = cs.controller.read(1)*5/255
                    angle = sum(angle2b)
                    Bytes = cs.controller.read(4)
                    benchmark = np.uint32(Bytes)
                    
                    #for flicker, change all irrelevant parameters to NaN
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
                    
                    namerange = range(1, len(cs.datanames)+1)
                    cs.data(row,namerange) = [counter, time, 
                    trial, rep, readdelay, bar1color, bar2color, 
                    backgroundcolor, barwidth, numgratings, angle, frequency, position, 
                    predelay, duration, output, benchmark]           
            elif msgtype == 225 :
                ID = cs.controller.read(1)
                cache = {}
                while cs.controller.in_waiting > 0 :
                    cache = [cache , cs.controller.read(1)]
                    
                raise ValueError(f"message type ID ({ID}) not recognized by controller. cache cleared ({cache}).")     
            else:
                cache = {}
                while cs.controller.in_waiting > 0 :
                    cache = [cache , cs.controller.read(1)]
               
                raise ValueError(f"message type from controller not recognized ({msgtype}). cache cleared ({cache}).")
            
    
   
        
    

    