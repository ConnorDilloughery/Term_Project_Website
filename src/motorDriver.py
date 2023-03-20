#@@ -0,0 +1,139 @@
import pyb
import time

# Code for motorDriver
class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety.
        @param self placeholder for the motor object
        @param en_pin Pin to enable motor
        @param in1pin Pin that collects the PWM signal
        @param in2pin Pin that collects the PWM signal
        @param timer  Timer that is associated with the pin
        """
        ## creates pin1 
        self.Pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        ## creates pin2
        self.Pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        ## creates EN pin, used to PULL_UP
        self.PinENA = pyb.Pin(en_pin, pyb.Pin.IN, pull =  pyb.Pin.PULL_UP)
        ## creates timer 1 using the imported timer and a frequency of 20000 Hz
        self.Timer1= pyb.Timer(timer, freq=20000)
        ## creates timer 2 using the imported timer and a frequency of 20000 Hz
        self.Timer2= pyb.Timer(timer, freq=20000)
        ## creates timer channel 1
        self.TimChannel1=self.Timer1.channel(1, pyb.Timer.PWM, pin = self.Pin1)
        ## creates timer channel 2
        self.TimChannel2=self.Timer2.channel(2, pyb.Timer.PWM, pin = self.Pin2)
        
        # calls the set_duty_cycle functins with a PWM of 10%
        self.set_duty_cycle(10)
        
        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param self placeholder for the motor object
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        @param level A signed integer holding the duty cycle of the voltage sent to the motor 
        """
        ## checks to see if the inputted PWM is positive, zero, or negative
        if level < 0 and level >=-100:
            # sets pin1 (negative terminal) to the PWM
            self.TimChannel1.pulse_width_percent(-level)
            # sets pin2 to 0
            self.TimChannel2.pulse_width_percent(0)
            # signals to the motor to run
            self.PinENA.value(True)
        # case for PWM = 0 
        elif level == 0:
            ## Sets pins to 0, since the motor will not be running
            self.TimChannel1.pulse_width_percent(0)
            self.TimChannel2.pulse_width_percent(0)
            ## gives motor time to recoginize this transaction
            
            ## turns to the motor to run, even though it will be running
            self.PinENA.value(True)
           
            
        elif level > 0 and level<=100:
            # Turns pin1 to low
            self.TimChannel1.pulse_width_percent(0)
            # Lets motor recongize action
            self.PinENA.value(False)
            # Sets pin2 to high
            self.TimChannel2.pulse_width_percent(level)
            # Lets code recognize action
            
            # Sends signal to motor to turn on
            self.PinENA.value(True)
        # Tells viewer is the duty cycle is changed    
        #print (f"Setting duty cycle to {level}")