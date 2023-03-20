

class PropControl:
    '''! This class is meant to control a permanent DC motor through the use
         of PWM. The class has the ability to reset home, change desired motor
         position, and calcualting the error to produce a new PWM value.
    '''
    def __init__(self, Kp,Theta_Want):
        '''!
        This is initiliazing the object
        @param self placeholder for the motorcontrol
        @param Kp The Kp parameter specifies the proportional constant
        @Param Theta_Want This Variable indicates the desired motor location
        
        '''
        ##Creating the PWM variable that stores the current PWM Value
        self.PWM= 0
        ##Creating the Error variable that stores the difference from wanted and current position
        self.Error=0
        ##Creating the Theta_Count variable that stores the motor's position
        self.Theta_Count=0
        ##Creating and setting the proportional constant value
        self.Kp= Kp
        ##Creating and setting the desired position variable
        self.Theta_Want= Theta_Want
    
    def run(self, Theta_Count, Theta_Want):
        '''! This function determines the new PWM to be sent to the motor
            to acheive the desired position using the specified Kp.
            @param self placeholder for the motorcontrol object
            @param Theta_Count The current position of the motor
            @param Theta_Want The position of the motor that is wanted
            @return PWM The new PWM value to be used to run the motor
        '''
        self.Theta_Want= Theta_Want
        self.Theta_Count= Theta_Count
       
        PWM = self.Kp*(self.Theta_Want-self.Theta_Count)
        if PWM >= 0:
             if PWM>100:
                 PWM=100
        elif PWM<0:
             if PWM<-100:
                PWM=-100
        
        return PWM
    
    def set_setpoint(self, Theta_Want):
        '''! This function allows the setting of a new position to be achieved
            @param self a placeholder for the motorcontro object
            @Theta_Want The position of the motor that is wanted
        '''
        #Setting the wanted position to the wanted position as specified by the input parameter
        self.Theta_Want=Theta_Want
    
    
    def set_Kp(self, Value):
        '''! This function allows teh setting to the wanted Kp as specified by the input parameter
            @param self a placeholder for the motorcontrol object
            @param Value The value of Kp wanted to be set
        '''
        #Setting the Kp of the object to the new specified value
        self.Kp= Value
    def ResetHome (self):
        '''! This function allows for the home position to be reset
            @param self a placeholder for the motorcontrol
        '''
        #Resetting the position
        self.Theta_Count=0