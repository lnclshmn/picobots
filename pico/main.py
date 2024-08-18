import machine
import utime

# UART0 with TX on Pin 0 and RX on Pin 1
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

while True:
    if uart.any():
        log_line = uart.readline()
        print(log_line.decode('utf-8').strip())
    utime.sleep(0.05)