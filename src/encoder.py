
import pyb

class Encoder:
    '''!
    @brief This class sets up an encoder using the given parameters during initilization. Allows for reading operations annd zero reset

    '''
    
    def __init__(self,PinIn1, PinIn2, timer):

        ''' !
        @brief This initializes the encoder with the given parameters
        @self A place holder for objects that will eventually be orientated
        @PinIn1 Corresponds to the first timer channel pin being used
        @PinIn2 Correponds to the second timer channel pin being used
        @timer Corresponds to the timer sharesd between PinIn1 and PinIn2
        '''
        ##Initializing count. variable for the encoder. This contains the encoder count
        self.Count=0
        ##Initilizing the Previous variable for the encoder. Used to figure out change in position
        self.Previous =0
        ##Setting up the first timer pin
        self.Pin1 = pyb.Pin(PinIn1, pyb.Pin.IN)
        ##Setting up the second timer pin
        self.Pin2 = pyb.Pin(PinIn2, pyb.Pin.IN)
        ##Setting up the timer for pin 1
        self.ENC_Timer1= pyb.Timer(timer, prescaler=0, period =0xFFFF)
        ##Setting up the timer for pin 2
        self.ENC_Timer2= pyb.Timer(timer, prescaler=0, period =0xFFFF)
        ##Setting up the channel and timer to encoder count
        self.ENC_CHANNEL1=self.ENC_Timer1.channel(1, pyb.Timer.ENC_AB, pin=self.Pin1)
        ##Setting up the channel and timer to encoder count
        self.ENC_CHANNEL2=self.ENC_Timer1.channel(2, pyb.Timer.ENC_AB, pin=self.Pin2)
    
    
    def read(self):
        '''!
        @brief This returns the overall timer position after finding it through set conditions
        @self A place holder for objects that will eventually be orientated
        @return This returns the current position of the motor 
        '''
        #Finding the current position of the motor
        self.readd= self.ENC_Timer1.counter()
        #Calculates the change with the previous
        self.delta= self.readd-self.Previous
        #Determining if the delta change was positive
        
        #Determining if delta was absurdly high
        if self.delta< -((0xFFFF)+1)/2:
            self.delta+= (0xFFFF)+1
            self.Count+= self.delta
        elif self.delta> ((0xFFFF)+1)/2:
            self.delta-= (0xFFFF)+1
            self.Count+= self.delta
        else:
            self.Count += self.delta
                
        #Changing the Previous value to match the current read value
        self.Previous= self.readd
          
        
        return self.Count

    
    def zero(self):
      #Sets Count to 0
        '''!
        @brief This command will reset the coutn to 0, resetting the home position
        @self A place holder for objects that will eventually be orientated
        '''
        #Sets Count to 0
        self.Count=0
        

