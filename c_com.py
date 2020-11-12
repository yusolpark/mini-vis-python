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
csLen = len(cs) + 1

def Get-Version():
    for i in range(1,csLen)
            fwrite(cs(i).controller,0,'uint8') #command to send back version number
            cs(i) = Grating_C2M(cs(i)) #read version number

def Connect():
    for i in range(1,csLen)
            cs(i).controller = serial(cs(i).port,'BaudRate',9600) #define serial port
            fopen(cs(i).controller) #open connection to serial port
        
    time.sleep(3) #wait for connection(s) to be established
    for i in range(1,csLen)
            fwrite(cs(i).controller,104,'uint8') #turns display backlight on
            cs(i).data = [] #create empty data structure
            cs(i).datanames = {}
        
def Disconnect():
    for i in range(1,csLen)
            fwrite(cs(i).controller,103,'uint8') #turn backlight off
            cs(i) = Grating_C2M(cs(i)) #get data from controller  %collect serial data if any still available
            fclose(cs(i).controller) #close connection to controller
        
def Send-Parameters():
    for i in range(1,csLen)
            fwrite(cs(i).controller,101,'uint8') #send grating parameter values to controller
            cs(i) = Grating_M2C(cs(i)) 
    

def Fill-Background():
    for i in range(1,csLen)
            fwrite(cs(i).controller,102,'uint8') #fill display with background color
            time.sleep(1) #wait for display to fill
        

def Backlight-Off():
    for i in range(1,csLen)
            fwrite(cs(i).controller,103,'uint8') #turns display backlight off
        
        
def Backlight-On():
    for i in range(1,csLen)
            fwrite(cs(i).controller,104,'uint8') #turns display backlight on
    
        
def Start-Grating():
    for i in range(1,csLen)
            fwrite(cs(i).controller,105,'uint8') #start gratings of current parameters
            
def Start-Flicker():
    for i in range(1,csLen)
            fwrite(cs(i).controller,106,'uint8') #start gratings of current parameters
    
        
def Get-Data():
    for i in range(1,csLen)
            cs(i) = Grating_C2M(cs(i)) #get data from controller      
        
      
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
   

