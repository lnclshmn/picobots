from machine import Pin, PWM
from L298N_motor import L298N
import time
import machine

# UART0 with TX on Pin 0 and RX on Pin 1
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(16), rx=machine.Pin(17))
#ser = serial.Serial(uart)

ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ENB = PWM(Pin(5))

deadzone = 50

left_motor = L298N(ENA, IN1, IN2)     #create a motor1 object
motor2 = L298N(ENB, IN3, IN4)
#motor1.setSpeed(40000)            #set the speed of motor1. Speed value varies from 25000 to 65534

while True:
    if uart.any():
        try:
            log_line = uart.readline().decode('utf-8').rstrip()
            data = eval(log_line)
            left_axis = abs(data.get('axisY'))
            right_axis = data.get('axisRY')
            
            if left_axis or right_axis is not None:
                print(f"Left Axis value: {left_axis}")
                print(f"Right Axis value: {right_axis}")
                
                if left_axis < deadzone:
                    left_motor.setSpeed(0)
                    left_motor.forward()
                    print('speed at 0')
                elif left_axis > deadzone and left_axis < 100:
                    left_motor.setSpeed(30000)
                    left_motor.forward()
                elif left_axis >= 100 and left_axis < 200:
                    left_motor.setSpeed(40000)
                    left_motor.forward()
                    print('speed at 40000')
                elif left_axis >= 200 and left_axis < 300:
                    left_motor.setSpeed(45000)
                    left_motor.forward()
                    print('speed at 45000')
                elif left_axis >= 300 and left_axis < 400:
                    left_motor.setSpeed(50000)
                    left_motor.forward()
                    print('speed at 50000')
                elif left_axis >= 400 and left_axis < 512:
                    left_motor.setSpeed(65000)
                    left_motor.forward()
                    print('speed at 65000')
            else:
                pass
                
        except (ValueError, SyntaxError):
            # print("Error: Invalid JSON data received")
            pass
    time.sleep(0.05)
        



