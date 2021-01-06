#open connection to controller
from c_com import c_com
import serial
ser = serial.Serial('/dev/cu.usbmodem14101',9600) 
#c_com('Connect')

class CS (object):
    def __init__(self, expname, directory, trial_duration, randomize,data,controller,datanames):
        self.expname = expname
        self.directory = directory
        self.trial_duration = trial_duration
        self.randomize = randomize #1=randomize order of conditions, 0=don't randomize
        self.data = data #where data is saved 
        self.controller = controller
        self.datanames = datanames

class PAR(object):
    def __init__(self, readdelay, bar1color, bar2color, backgroundcolor, barwidth, numgratings,angle, frequency, position, predelay, duration, output):
        self.readdelay = readdelay #delay between controller serial reads (in ms)
        self.bar1color = bar1color #RGB color values of bar 1 [R=0-31, G=0-63, B=0-31]
        self.bar2color = bar2color #RGB color values of bar 2
        self.backgroundcolor = backgroundcolor #RGB color values of background
        self.barwidth = barwidth # width of each bar (pixels)
        self.numgratings = numgratings # number of bright/dark bars in grating
        self.angle = angle # angle of grating (degrees) [0=drifting right, positive angles rotate clockwise]
        self.frequency = frequency # temporal frequency of grating (Hz) [0.1-25]
        self.position = position # x,y position of grating relative to display center (pixels)
        self.predelay = predelay # delay after start command sent before grating pattern begins (s) [0.1-25.5]
        self.duration = duration # duration that grating pattern is shown (s) [0.1-25.5]
        self.output = output # value of controller's output signal while grating is shown (V) [0-5]

#set starting/default grating parameters
#param = PAR(100,[0, 0, 30],[0, 0 ,0],[0, 0 ,15],20,1,0,1.5,[0, 0],0,2,5)
param = PAR(100,[1, 2, 3],[4, 5 ,6],[7, 8 , 9],20,1,30,1,[10, 10],0,2,5)

#set experiment parameters
#cs = CS('COM7','directional_test_stimulus1', 'Users/Matthew/Documents/Schaffer-Nishimura Lab/Visual Stimulation/Data', 3, 0, None, None,None) 
cs = CS('directional_test_stimulus1','/Users/yusolpark/python/mini-vis-python', 3, 0, None, None,{'counter', 'time', 'trial', 'repetition', 'readdelay', 
'bar1red', 'bar1green', 'bar1blue', 'bar2red', 'bar2green', 'bar2blue', 'backred', 
'backgreen', 'backblue', 'barwidth', 'numgratings', 'angle', 'frequency', 
'position1', 'position2', 'predelay', 'duration', 'output', 'benchmark'})


cs = c_com('Send-Parameters', cs,ser, param) #send grating parameters to controller
cs = c_com('Fill-Background',cs,ser) #fill display with background color

## send stimulus
#param.angle = 0

import time 
start_time = time.time()
cs = c_com('Send-Parameters', cs, ser,param) #send grating parameters to controller
cs = c_com('Start-Gratings',cs,ser) #start gratings

current_time = time.time()
elapsed_time = current_time - start_time

#while elapsed_time < cs.trial_duration : #delay until next trial
 #   time.sleep(0.001)

time.sleep(cs.trial_duration)

#end_time = time.time();
cs = c_com('Get-Data',cs, ser) #retrieve data sent from controller
#cs.data = cs

## save data for current experiment
filename =  time.strftime("%Y-%m-%d %H-%M-%S")+' '+cs.expname+' CS.py'

import os
newfolder = os.path.basename

if not os.path.exists(newfolder):
    os.makedirs(newfolder)

import pickle
with open (filename,'wb') as f:
    pickle.dump(cs,f)

# completeName = os.path.join(cs1.directory, filename)
# File = open(completeName,'cs')

# close connection
cs = c_com('Disconnect',cs,ser) #close connection to controller

print (cs.data)