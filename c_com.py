#def c_com(cs,command):
'''
FUNCTION cs = c_com(cs, command)

Function to manage serial communication between Matlab and Arduino.

LIST OF COMMANDS:
'Connect': opens serial connection to Arduino
'Disconnect': closes serial connection to Arduino
'Get-Version': gets Arduino program version number (ID 0)
'Send-Parameters': sets current grating parameters (ID 101)
'Fill-Background': fills screen with background color (ID 102):
'Backlight-Off': turns off backlight (ID 103)
'Backlight-On': turns on backlight (ID 104)
'Start-Display': start current grating (ID 105)
'Start-Flicker': flicker backlight at current frequency (ID 106)
'Get-Data': retrieve data sent back from controller 
'''
#set-up
import time
import serial
with serial.Serial('/dev/cu.usbmodem142101',9600) as ser:


def Get-Version():
    ser.write(0) #command to send back version number
    cs = Grating_C2M(cs) #read version number

def Connect():
   ser.write(104) #turns display backlight on
    
        
def Disconnect():
    ser.write(103) #turn backlight off
    cs = Grating_C2M(cs) #get data from controller  %collect serial data if any still available
    #fclose(cs(i).controller) #close connection to controller
        
def Send-Parameters():
   ser.write(101) #send grating parameter values to controller
    cs = Grating_M2C(cs) 
    

def Fill-Background():
    ser.write(102) #fill display with background color
    time.sleep(1) #wait for display to fill
        

def Backlight-Off():
   ser.write(103) #turns display backlight off
        
        
def Backlight-On():
    ser.write(104) #turns display backlight on
    
        
def Start-Grating():
    ser.write(105) #start gratings of current parameters
            
def Start-Flicker():
      ser.write(106) #start gratings of current parameters
    
        
def Get-Data():
     cs = Grating_C2M(cs) #get data from controller      
        
      
def default():
        raise ValueError(f"Command {command} not recognized. Type "help Controller_stimcomm" for list of valid commands")
   
command = {
'Connect': Connect,
'Disconnect': Disconnect,
'Get-Version': Get-Version,
'Send-Parameters': Send-Parameters,
'Fill-Background': Fill-Background,
'Backlight-Off': Backlight-Off,
'Backlight-On': Backlight-On,
'Start-Display': Start-Display,
'Start-Flicker': Start-Flicker,
'Get-Data': Get-Data,
}

def c_com(cs,command):
    return command.get(x,default)
   

