def grating_M2C():
    from minigratings_teststimulus import param, cs
    '''
    FUNCTION cs = Grating_M2C(cs)

    Function to send grating parameters from Matlab to Arduino.

    Parameter list
    command 101: set parameters:
        parameter 1: read delay (ms) (1 data byte)
        parameter 2: bar1 color [R G B] (3 data bytes)
        parameter 3: bar2 color [R G B] (3 data bytes)
        parameter 4: background color [R G B] (3 data bytes)
        parameter 5: bar width (# of pixels), depending on number of gratings) (1 data byte)
        parameter 6: number of gratings (bar1 + bar2 = 1 grating) (1 data byte)
        parameter 7: angle (0-360) (2 data bytes)
        parameter 8: frequency (Hz) (1 data byte)
        parameter 9: position [x, y] of grating center (pixels) (2 data bytes)
        parameter 10: pre delay (s) (1 data byte)
        parameter 11: duration (s) (1 data byte)
        parameter 12: output signal voltage (pwm) (1 data byte)
        total bytes: 20
    '''

    ## check for errors in parameters
    max_size = 70 #maximum window half-width that can fit inside viewable area   

    #check that readdelay parameter is in range
    assert param.readdelay>0 and param.readdelay<=255 , "readdelay value must be integer between 1-255"

    #check that color values are integers within range for 16-bit color
    assert param.bar1color(1)>= 0 and param.bar1color(1)<32,"red value of bar 1 must be between 0-31"
    assert param.bar1color(2)>=0 and param.bar1color(2)<64,"green value of bar 1 must be between 0-63"
    assert param.bar1color(3)>=0 and param.bar1color(3)<32,"blue value of bar 1 must be between 0-31"
    assert param.bar2color(1)>=0 and param.bar2color(1)<32,"red value of bar 2 must be between 0-31"
    assert param.bar2color(2)>=0 and param.bar2color(2)<64,"green value of bar 2 must be between 0-63"
    assert param.bar2color(3)>=0 and param.bar2color(3)<32,"blue value of bar 2 must be between 0-31"
    assert param.backgroundcolor(1)>=0 and param.backgroundcolor(1)<32,"red value of background must be between 0-31"
    assert param.backgroundcolor(2)>=0 and param.backgroundcolor(2)<64,"green value of background must be between 0-63"
    assert param.backgroundcolor(3)>=0 and param.backgroundcolor(3)<32,"blue value of background must be between 0-31"
    assert all( param.bar1color % 1 == 0),"bar 1 color values must be integers"
    assert all(param.bar2color % 1 ==0),"bar 2 color values must be integers"
    assert all(param.backgroundcolor %1 ==0),"background color values must be integers"

    #check that bar width is within allowed range
    assert param.barwidth % 1 ==0 and param.barwidth>0 and param.barwidth<=60,"bar width must be an integer between 1-60"

    #check that number of gratings is within allowed range
    assert param.numgratings % 1 ==0 and param.numgratings>0 and param.numgratings<=60,"num gratings must be an integer between 1-60"

    #check that angle is within range
    assert param.angle>=0 and param.angle<=360,"angle must be an integer between 0-360"
    
    if param.angle %1 >0:
        param.angle = round(param.angle)
        print(f"angle rounded to {param.angle} degrees")

    if param.angle==360:
        param.angle=0 


    #separate angle into 2 bytes
    param.angle2b = min(180, param.angle), max(0, param.angle-180)

    #check that frequency is within range
    if (param.frequency*10) % 1 > 0:
        param.frequency = round(param.frequency*10)/10
        print(f"frequency rounded to {param.frequency}  Hz (nearest 0.1 Hz)")


    #check that position is in allowed range
    assert all(param.barwidth %1 ==0) and all(param.position>=-max_size) and all(param.position<=max_size),f"bar width must be an integer between +/- {max_size}"

    #check that position will not cause grating to be clipped
    assert all(abs(param.position)+param.barwidth*param.numgratings<= max_size) , "grating of current size/position will not fit inside viewable area"

    #check that duration is within range
    assert param.duration>=0 and param.duration<=25.5,"duration must be between 0-25.5 seconds"
    if (param.duration*10)%1>0:
        param.duration = round(param.duration*10)/10
        print(f"duration rounded to {param.duration}  s (nearest 0.1 ms)")


    #check that pre delay is within range
    assert param.predelay>=0 and param.predelay<=25.5,"predelay must be between 0-25.5 seconds"
    if (param.predelay*10)%1>0:
        param.predelay = round(param.predelay*10)/10
        print(f"predelay rounded to {param.predelay} s (nearest 0.1 ms)")


    #check that trial duration is longer than display duration
    if hasattr(cs,'trial_duration')==True:
        assert cs.trial_duration > param.predelay+param.duration,"trial duration must be longer than predelay + duration"


    #check that signal is within range
    assert param.output>=0 and param.output<=5,"output signal must be between 0-5 volts"


    ## send parameters to controller if no errors found
    import serial 
    with serial.Serial('/dev/cu.usbmodem14101',9600) as ser:

        ser.write(param.readdelay)
        ser.write(param.bar1color)
        ser.write(param.bar2color)
        ser.write(param.backgroundcolor)
        ser.write(param.barwidth)
        ser.write(param.numgratings)
        ser.write(param.angle2b)
        ser.write(param.frequency*10) #converts frequency to units of 100 mHz for uint8 data transfer
        ser.write(param.position)
        ser.write(param.predelay*10) #converts pre delay to units of 100 ms for uint8 data transfer
        ser.write(param.duration*10) #converts duration to units of 100 ms for uint8 data transfer
        ser.write(round(param.output*255/5)) #convert 0-5 V range to 1 byte (0-255)],'uint8')
 
            
   