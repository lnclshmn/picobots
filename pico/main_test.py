from machine import Pin, PWM
from L298N_motor import L298N
import time
import machine

ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ENB = PWM(Pin(5))

motor1 = L298N(ENA, IN1, IN2)
motor1.setSpeed(65000)

motor2 = L298N(ENB, IN3, IN4)
motor2.setSpeed(65000)

while True:
    print('running forward')
    motor1.forward()
    motor2.forward()
    time.sleep(5)
    
    print('running backward')
    motor1.backward() 
    motor2.backward()
    time.sleep(5)
    
    print('stopping for 2 seconds')
    motor1.stop()
    motor2.stop()
    time.sleep(2)
