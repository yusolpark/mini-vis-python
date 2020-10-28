#open connection to controller
cs = c_com(cs, 'Connect')

class CS (object):
    def __init__(self, port, expname, directory, trial_duration, randomize):
        self.port = port 
        self.expname = expname
        self.directory = directory
        self.trial_duration = trial_duration
        self.randomize = randomize #1=randomize order of conditions, 0=don't randomize


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
param1 = PAR(100,[0 0 30],[0 0 0],[0 0 15],20,1,0,1.5,[0, 0],0,2,5)

#set experiment parameters
cs1 = CS('COM7','directional_test_stimulus1', 'Users/Matthew/Documents/Schaffer-Nishimura Lab/Visual Stimulation/Data', 3, 0) 

cs = c_com(cs, 'Send-Parameters') #send grating parameters to controller
cs = c_com(cs, 'Fill-Background') #fill display with background color

## send stimulus
#param1.angle = 0

import time 
start_time = time.time()
cs = c_com(cs, 'Send-Parameters') #send grating parameters to controller
cs = c_com(cs, 'Start-Grating') #start gratings

current_time = time.time()
elapsed_time = current_time - start_time

while elapsed_time < cs1.trial_duration : #delay until next trial
    time.sleep(0.001)

#end_time = time.time();
cs = c_com(cs, 'Get-Data') #retrieve data sent from controller


## save data for current experiment
filename =  time.strftime("%Y-%m-%d %H-%M-%S")+' '+cs1.expname+' CS.py'

import os
newfolder = os.path.basename

if not os.path.exists(newfolder):
    os.makedirs(newfolder)

completeName = os.path.join(cs1.directory, filename)
File = open(completeName,'cs')

# close connection
cs = c_com(cs, 'Disconnect') #close connection to controller

