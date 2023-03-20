"""!
@file main.py
Author: Connor Dilloughery, Erik Torres

"""
import utime as time
import mlx_cam as Cam
from machine import Pin, I2C
import gc
import pyb
import motorDriver as Vroom
import encoder
import MotorControl

gc.collect()

def main():
    '''! This function is the main function to run the code neccessary to activate our system
         It includes 13 states that determine what steps we want to run
         It takes in no parameters and returns no values
    '''
    ##Initializes the state variable to start at state 0
    state = 0
    ##Initializes the middle variable to tell us how many consectutive times middle has been detected
    middle = 0
    gc.collect()
    ##Creates a camera peripheral
    i2c_bus = I2C(1)
    print("MXL90640 Easy(ish) Driver Test")
    gc.collect()
    ##Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
    
    
    gc.collect()
    ##Create the camera object and set it up in default mode
    camera = Cam.MLX_Cam(i2c_bus)
    gc.collect()
    
    try:
        PinC2 = pyb.Pin (pyb.Pin.board.PC2, pyb.Pin.IN)
        while True:
            if state == 0:
                ##Initialization state
                ##must wait for button to be pressed, set state = 1 when pressed
                if PinC2.value() == 1:
                    ##Sets state equal to the initial base rotation state
                    state = 1
                else:
                    state = 0
                ##Delays the code for 100 ms
                time.sleep_ms(100)
            
            elif state == 1:
                ##Initial Rotation state
                ##rotate motor to rotate the base 180 degrees
                ##check to see if position of base is complete
                ##Set state equal to the thermal case
                state = 2
                ##rotates the base of the motor to the theta 1 position
                theta1 = 250000
                ##Runs the base motor function
                task1_Motor(theta1)
                ##Delays the motor for 100 ms
                time.sleep_ms(100)

                
            elif state == 2:
                ##Thermal Camera State
                ##Runs the thermal camera
                try:
                    ##Get and image and see how long it takes to grab that image
                    print("Click.", end='')
                    begintime = time.ticks_ms()
                    ##Gathers image details
                    image = camera.get_image()
                    print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
                    ##Creates array of camera pixels
                    pixel_array = camera.get_array(image.pix)
                    ##Delays the code 1 s
                    time.sleep_ms(1000)
                except KeyboardInterrupt:
                    break
                ##Finds the warmest area of the pixels array
                max_val = max(pixel_array)
                ##Initializes the index variable
                index = 0
                ##Iterates through the pixel array
                for i in pixel_array:
                    ##If the the iterative value is equal to max value in the array, stop the for loop
                    ##Sets the index equal to the index of the max value in the array
                    if i == max_val:
                        break
                    ##Iterate the index value
                    index += 1
                
                ##Finds the location of the max pixel in the matrix, creates a 3x3 matrix
                row = index // 32
                column = index % 32
                ##Tests to see if location is in the top row of matrix
                if row < 8:
                    ##Tests to see if location is in the left column of matrix
                    if column < 11:
                        ##Sets state to the top left case
                        state = 3
                    ##Tests to see if location is in the middle column of matrix
                    elif column < 21:
                        ##Sets state to the top middle case
                        state = 4
                    ##Tests to see if location is in the right column of matrix
                    else:
                        ##Sets state to the top right case
                        state = 5
                ##Tests to see if location is in the middle row of matrix
                elif row >= 8 and row < 16:
                    ##Tests to see if location is in the left column of matrix
                    if column < 11:
                        ##Sets state to the middle left case
                        state = 6
                    ##Tests to see if location is in the middle column of matrix
                    elif column < 21:
                        ##Sets state to the middle case
                        state = 7
                    ##Tests to see if location is in the right column of matrix
                    else:
                        ##Sets state to the middle rihgt case
                        state = 8
                ##Tests to see if location is in the bottom row of matrix
                else:
                    ##Tests to see if location is in the left column of matrix
                    if column < 11:
                        state = 9
                    ##Tests to see if location is in the middle column of matrix
                    elif column < 21:
                        state = 10
                    else:
                    ##Tests to see if location is in the right column of matrix
                        state = 11
                    ##Delays the code for 100 ms
                    time.sleep_ms(100)
                    
            elif state == 3:
                ##Top Left State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = 100000
                theta2 = -200
                ##rotate base right
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate down
                task2_Motor(theta2)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                
            elif state == 4:
                ##Top Middle State 
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = 0
                theta2 = -200
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate down
                task2_Motor(theta2)
                
            elif state == 5:
                ##Top Right State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = -100000
                theta2 = -200
                ##rotate base left
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate down
                task2_Motor(theta2)
                
            elif state == 6:
                ##Middle Left State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = 100000
                theta2 = 0
                ##rotate base right
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                #task2_Motor(theta2)
                
            elif state == 7:
                ##Middle State
                ##Adds the middle value
                middle += 1
                ##Runs activation state when the middle state has been detected two times in a row
                if middle == 2:
                    print('go time')
                    ##Sets state back to the activation case
                    state = 12
                else:
                    ##Sets state back to the thermal case
                    state = 2
                ##Delays the code 100 ms
                time.sleep_ms(100)
                
            elif state == 8:
                ##Middle Right State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = -100000
                theta2 = 0
                ##rotate base left
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                
            elif state == 9:
                ##Bottom Left State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = 100000
                theta2 = 200
                ##rotate base right
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate up
                task2_Motor(theta2)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                
            elif state == 10:
                ##Bottom Middle Case
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = 0
                theta2 = 200
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate up
                task2_Motor(theta2)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                
            elif state == 11:
                ##Bottom Right State
                ##Sets state back to the thermal case
                state = 2
                ##Clears middle value
                middle = 0
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##Sets up desired positions
                theta1 = -100000
                theta2 = 200
                ##rotate base left
                task1_Motor(theta1)
                ##Delays the code 100 ms
                time.sleep_ms(100)
                ##rotate up
                task2_Motor(theta2)
                ##Delays the code 100 ms
                time.sleep_ms(100)

                
            elif state == 12:
                print('Activating the gun')
                ##Turn on the gun's motors by running the fire state
                state = 13
                ##Runs the fire code
                fire()
                ##Delays the code 3 seconds
                time.sleep_ms(3000)
            else:
                print('YAYUHH bullets have been fire')
                ##Deactivates system
                break
        print ("Done.")
                
    except KeyboardInterrupt:
        print('Keyboard Interrupted')
        
        
    
def task1_Motor(theta1):
        '''!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
        @ param theta1 Tells the code what the desired postion value is
        @return Boolean
        '''
        ##Initiating the communication interface through UART
        ser= pyb.UART(2,baudrate= 115200)
        ##Specifying the motor shield EN pin
        EN_PIN= 'PC1'
        ##Specifyinng the In1 pin for the motor shield
        IN1= 'PA0'
        ##Specifying the IN2 pin for the motor shield
        IN2= 'PA1'
        ##SPecifying the Timer 
        TIMER=5;
        ##Specifying the first encoder input pin
        ENC1= 'PC6'
        ##Specifying the second encoder input pin
        ENC2= 'PC7'
        ##Specifying the encoder Timer
        ENCT= 8
        ##Specifying the Theta value that is wanted
        Theta_Want= theta1
        ##Specifying the value for Kp
        Kp= .0012
        ##Creating the motor object
        Motor1= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        ##Creating the encoder object for the motor
        Motor1E= encoder.Encoder(ENC1, ENC2, ENCT)
        ##Setting the motor to 0. Off
        Motor1.set_duty_cycle(0)
        
        while True:
            ##Creating the motor proprtional control object
            Motor1PC= MotorControl.PropControl(Kp, Theta_Want)
            ##Setting Theta Old to a nonzero value to prevent delta theta from initializing at zero
            Theta_Count_Old = -1000
            ##Creating counter variable
            counter = 0
            while True:
                 ##Reading the current position of the motor
                 Theta_Count= Motor1E.read()
                 ##If Theta_want is zero, runs code to make delta_Theta positive
                 if Theta_Want < 0:
                     delta_Theta = Theta_Count_Old - Theta_Count
                 ##Calculats delta theta
                 else:
                     delta_Theta = Theta_Count - Theta_Count_Old
                 ##Creates a new PWM value
                 PWM = Motor1PC.run(Theta_Count, Theta_Want)
                 ##Updates the motor with the new PWM
                 Motor1.set_duty_cycle(PWM)
                 ##If motor is slowing down near desired position, run this code
                 if abs(delta_Theta) <= 300 and counter > 50:
                     ##Resets the PWM
                     PWM = 0
                     ##Stops the motor
                     Motor1.set_duty_cycle(PWM)
                     print('done')
                     return True
                 ##Updates the old theta count with the current theta count
                 Theta_Count_Old = Theta_Count
                 #Calculating the new PWM value depending on the current position of the motor
                 ##Creates a new PWM value
                 PWM = Motor1PC.run( Theta_Count, Theta_Want)
                 ##Setting the PWM of the motor using the new value that was created
                 Motor1.set_duty_cycle(PWM)
                 ##Iterates the counter value
                 counter += 1
                 ##Delays code for 50 ms
                 time.sleep_ms(50)
            ##Resets the motor
            Motor1.set_duty_cycle(0)
            Motor1PC.ResetHome()
            Motor1E.zero()

            
        
    
    
def task2_Motor(theta2):#Kp2, theta2):
        """!
        Task which controls the position of the first motor. There are no input parameters as the values chosen were selected withing
        the function itself
        @ param theta2 Tells the code what the desired postion value is
        @return Boolean
        """
        ##Initiating the communication interface through UART
        ser= pyb.UART(2,baudrate= 115200)
        ##Specifying the motor shield EN pin
        EN_PIN= 'PA10'
        ##Specifyinng the In1 pin for the motor shield
        IN1= 'PB4'
        ##Specifying the IN2 pin for the motor shield
        IN2= 'PB5'
        ##SPecifying the Timer 
        TIMER=3;
        ##Specifying the first encoder input pin
        ENC2= 'PB6'
        ##Specifying the second encoder input pin
        ENC1= 'PB7'
        ##Specifying the encoder Timer
        ENCT= 4
        ##Specifying the Theta value that is wanted
        Theta_Want2= theta2
        ##Specifying the value for Kp
        Kp= 0.012#Kp2
        ##Creating the motor object
        Motor2= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        ##Creating the encoder object for the motor
        Motor2E= encoder.Encoder(ENC1, ENC2, ENCT)
        ##Setting the motor to 0. Off
        Motor2.set_duty_cycle(0)
        
        while True:
            ##Creating the motor proprtional control object
            Motor2PC= MotorControl.PropControl(Kp, Theta_Want2)
            ##Setting Theta Old to a nonzero value to prevent delta theta from initializing at zero
            Theta_Count_Old2 = -1000
            ##Creating counter variable
            counter = 0
            while True :
                 ##Reading the current position of the motor
                 Theta_Count2= Motor2E.read()
                 ##If Theta_want is zero, runs code to make delta_Theta positive
                 if Theta_Want2 < 0:
                     delta_Theta2 = Theta_Count_Old2 - Theta_Count2
                 ##Calculates delta theta
                 else:
                     delta_Theta2 = Theta_Count2 - Theta_Count_Old2
                 ##Calculating the new PWM value depending on the current position of the motor
                 PWM2 = Motor2PC.run(Theta_Count2, Theta_Want2)
                 ##Setting the PWM of the motor using the new value that was created
                 Motor2.set_duty_cycle(PWM2)
                 ##If motor is slowing down near desired position, run this code
                 if abs(delta_Theta2) <= 300 and counter > 50:
                     ##Sets PWM to a value to stop the motor
                     PWM2 = 0
                     ##Stops the motor
                     Motor2.set_duty_cycle(PWM2)
                     print('done')
                     return True
                 ##Updates Theta Old
                 Theta_Count_Old2 = Theta_Count2
                 ##Calculating the new PWM value depending on the current position of the motor
                 PWM2 = Motor2PC.run( Theta_Count2, Theta_Want2)
                 ##Setting the PWM of the motor using the new value that was created
                 Motor2.set_duty_cycle(PWM2)
                 ##Iterates the counter
                 counter += 1
                 ##Delays the code for 50 ms
                 time.sleep_ms(50)
            ##Resets the motor
            Motor2.set_duty_cycle(0)
            Motor2PC.ResetHome()
            Motor2E.zero()
            
def fire():
    '''! This code sets up the turns of the gun motors and solenoid to start launching bullets.
         It takes in no parameters and returns no values
    '''
    ##Sets up the gun motor gate pin
    PinC0 = pyb.Pin (pyb.Pin.board.PC0, pyb.Pin.OUT)
    ##Sets up the solenoid gate poon
    PinC3 = pyb.Pin (pyb.Pin.board.PC3, pyb.Pin.OUT)
    ##Turns on the motor
    PinC0.value(1)
    ##Delays code to let the motor flywheels to maximize their spin
    time.sleep_ms(5000)
    ##Creates counter variable
    counter = 0
    ##Runs loop to launch several darts
    while True:
        ##Delays code for 50 ms
        time.sleep_ms(50)
        ##Turns on solenoid 
        PinC3.value(1)
        ##If counter is 2000, stop activating the solenoid
        if counter == 2000:
            break
        ##Leaves solenoid on for 50 ms
        time.sleep_ms(50)
        ##Turns off the solenoid by retracting the pin
        PinC3.value(0)
        ##Iterates the counter
        counter+=1
    ##Turns off gun motors after while loop has been complete
    PinC0.value(0)
    
            
if __name__ == "__main__":
    ##Runs main script
    main()