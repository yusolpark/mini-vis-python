#open connection to controller
cs.port = 'COM7'
cs = c_com(cs, 'Connect')

##set experiment parameters
cs.expname = 'directional_test_stimulus1'
cs.directory = 'C:\Users\Matthew\Documents\Schaffer-Nishimura Lab\Visual Stimulation\Data';
cs.trial_duration = 3
cs.randomize = 0 #1=randomize order of conditions, 0=don't randomize

'''
set starting/default grating parameters
param.readdelay = 100; %delay between controller serial reads (in ms)
param.bar1color = [0 0 30]; %RGB color values of bar 1 [R=0-31, G=0-63, B=0-31]
param.bar2color = [0 0 0]; %RGB color values of bar 2
param.backgroundcolor = [0 0 15]; %RGB color values of background
param.barwidth = 20; % width of each bar (pixels)
param.numgratings = 1; % number of bright/dark bars in grating
param.angle = 0; % angle of grating (degrees) [0=drifting right, positive angles rotate clockwise]
param.frequency = 1.5; % temporal frequency of grating (Hz) [0.1-25]
param.position = [0, 0]; % x,y position of grating relative to display center (pixels)
param.predelay = 0; % delay after start command sent before grating pattern begins (s) [0.1-25.5]
param.duration = 2; % duration that grating pattern is shown (s) [0.1-25.5]
param.output = 5; % value of controller's output signal while grating is shown (V) [0-5]
'''

cs.param = param
cs = c_com(cs, 'Send-Parameters') #send grating parameters to controller
cs = c_com(cs, 'Fill-Background') #fill display with background color

## send stimulus
cs.param.angle = 0

import time 
start_time = time.time()
cs = c_com(cs, 'Send-Parameters') #send grating parameters to controller
cs = c_com(cs, 'Start-Grating') #start gratings

current_time = time.time()
elapsed_time = current_time - start_time

while elapsed_time < cs.trial_duration #delay until next trial
    time.sleep(0.001)

#end_time = time.time();
cs = c_com(cs, 'Get-Data') #retrieve data sent from controller


## save data for current experiment
filename =  time.strftime(%Y-%m-%d %H-%M-%S)+' '+cs.expname+' CS.py'
import os
newfolder = os.path.basename

if not os.path.exists(newfolder):
    os.makedirs(newfolder)

completeName = os.path.join(cs.directory, filename)
File = open(completeName,'cs')

# close connection
cs = c_com(cs, 'Disconnect') #close connection to controller

