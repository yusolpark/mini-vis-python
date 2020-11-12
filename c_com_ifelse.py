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
    cs.controller = ser

def c_com(cs,command):
        if command == 'Start-Gratings':
            cs.controller.write(bytearray([105])) #start gratings of current parameters
        elif command == 'Backlight-Off':
            cs.controller.write(bytearray([103])) #turns display backlight off
        elif command == 'Backlight-On':
            cs.controller.write(bytearray([104])) #turns display backlight on
        elif command == 'Connect':
            cs.controller.write(bytearray([0])) #command to send back version number
            cs = Grating_C2M(cs) #read version number
        elif command == 'Disconnect':
            cs.controller.write(bytearray([103])) #turn backlight off
            cs = Grating_C2M(cs) #get data from controller  %collect serial data if any still available
        elif command == 'Send-Parameters':
            cs.controller.write(bytearray([101])) #send grating parameter values to controller
            cs = Grating_M2C(cs) 
        elif command == 'Fill-Background':
            cs.controller.write(bytearray([102])) #fill display with background color
            time.sleep(1) #wait for display to fill
        elif command == 'Start-Flicker':
            cs.controller.write(bytearray([106])) #start gratings of current parameters
        elif command == 'Get-Data':
            cs = Grating_C2M(cs) #get data from controller      
        else:
            raise ValueError(f"Command {command} not recognized. Type "help Controller_stimcomm" for list of valid commands")
           