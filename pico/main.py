from machine import Pin, PWM
from L298N_motor import L298N
import time
import machine

uart = machine.UART(0, baudrorate=115200, tx=machine.Pin(16), rx=machine.Pin(17))

ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ENB = PWM(Pin(5))

deadzone = 50

left_motor = L298N(ENA, IN1, IN2) 
right_motor = L298N(ENB, IN3, IN4)


while True:
    if uart.any():
        try:
            log_line = uart.readline().decode('utf-8').rstrip()
            data = eval(log_line)
            left_axis = data.get('axisY')
            right_axis = data.get('axisRY')
            
            def translate(value, from_min, from_max, to_min, to_max):
                if value is None:
                    return None
                mod_value = value
                from_range = from_max - from_min
                to_range = to_max - to_min
                scaled_value = float(mod_value - from_min) / float(from_range)
                final_value = to_min + (scaled_value * to_range)
                return int(-final_value)
            
            print(f"left axis: {left_axis}")
            left_speed = translate(left_axis, -512, 512, -65534, 65534)
            print(f"left speed: {left_speed}")

            print(f"right axis: {right_axis}")
            right_speed = translate(right_axis, -512, 512, -65534, 65534)
            print(f"right speed: {right_speed}")
            
            if left_axis is None:
                pass
            elif abs(left_axis) < deadzone:
                left_motor.setSpeed(0)
                left_motor.forward() 
                print('stopped')
            else:
                if (left_speed < 0): 
                    left_motor.setSpeed(abs(left_speed))
                    left_motor.backward()
                elif (left_speed > 0):
                    left_motor.setSpeed(left_speed)
                    left_motor.forward()

            if right_axis is None:
                pass
            elif abs(right_axis) < deadzone:
                right_motor.setSpeed(0)
                right_motor.forward()
                print('stopped')
            else:
                if (right_speed < 0): 
                    right_motor.setSpeed(abs(right_speed))
                    right_motor.backward()
                elif (right_speed > 0):
                    right_motor.setSpeed(right_speed)
                    right_motor.forward()
                
        except (ValueError, SyntaxError):
            pass
    time.sleep(0.01)
