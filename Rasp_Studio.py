# Raspberry Pi studio control software
# Version 0.2.1
import RPi.GPIO as GPIO
import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600) # IMPORTANT: change this to actual address
GPIO.setmode(GPIO.BCM)

print ("Initializing, please wait ...")
main_sw_pin = 25 # Pin for main switch
sub_sw_pin = 24 # Pin for secondary switch

led_pin = 23 # Pin for main status LED

power_delay = 1 # Delay in s between sequentially powering on devices

power_flag = 0 # Flag for main power status
sub_flag = 0 # Flag for sub power status

main_power_pins = [1,2,3,4,11,12]
sub_power_pins = [2,3,4,5,6,7,8,9,10]
GPIO.setup(main_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Initializing input pins
GPIO.setup(sub_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(led_pin, GPIO.OUT) # Initializing led pin

def power_off(channel):# Turning main power off sequentially in reverse order
    global power_flag
    for 1 to 3:
        if(GPIO.input(main_sw_pin, GPIO.UP)):
            return
        time.sleep(0.1)
    if sub_flag: # Turning sub power off if on
        print ("Turning off sub power first")
        sub_off(main_sw_pin)
        sleep(0.3)
    for pin in main_power_pins:
        ser.write(bytes([ord('0') + pin * 2]))
        time.sleep(power_delay)
    GPIO.output(led_pin, GPIO.LOW) # Led off
    power_flag = 0
    GPIO.remove_event_detect(25)
    GPIO.add_event_detect(main_sw_pin, GPIO.RISING, callback=power_on, bouncetime=1000)
    print ("Main power turned off")

def power_on(channel):
    print ("Toggling on main power")
    global power_flag
    for 1 to 3:
        if(GPIO.input(main_sw_pin, GPIO.DOWN)):
            return
        time.sleep(0.1)
    for pin in main_power_pins:
        ser.write(bytes([ord('0') + pin * 2 + 1]))
        time.sleep(power_delay)
    GPIO.output(led_pin, GPIO.HIGH) # LED on
    power_flag = 1 # Led on
    GPIO.remove_event_detect(main_sw_pin)
    GPIO.add_event_detect(main_sw_pin, GPIO.FALLING, callback=power_off, bouncetime=1000) # Set up triggers
    print ("Main power turned on")

def sub_off(channel):
    global sub_flag # Turning sub power off sequentially in reverse order
    print ("Turning off sub power")
    for 1 to 3:
        if(GPIO.input(sub_sw_pin, GPIO.UP) and GPIO.input(main_sw_pin, GPIO.UP)):
            return
        time.sleep(0.1)
    for pin in sub_power_pins:
        ser.write(bytes([ord('0') + pin * 2 + 1]))
        time.sleep(power_delay
    sub_flag = 1
    GPIO.remove_event_detect(sub_sw_pin)
    GPIO.add_event_detect(sub_sw_pin, GPIO.RISING, callback=sub_on, bouncetime=1000)
    print ("Sub power turned off")

def sub_on(channel):
    global sub_flag # Turning sub power on sequentially
    if power_flag:
        print ("Turning on sub power")
        for 1 to 3:
            if(GPIO.input(sub_sw_pin, GPIO.DOWN)):
                return
            time.sleep(0.1)
        for pin in sub_power_pins:
            ser.write(bytes([ord('0') + pin * 2 + 1]))
            time.sleep(power_delay)
        sub_flag = 0
        GPIO.remove_event_detect(sub_sw_pin)
        GPIO.add_event_detect(sub_sw_pin, GPIO.FALLING, callback=sub_off, bouncetime=1000)
        print ("Sub power turned on")

GPIO.add_event_detect(main_sw_pin, GPIO.RISING, callback=power_on, bouncetime=1000) # Set up triggers
# GPIO.add_event_detect(main_sw_pin, GPIO.RISING, callback=power_off, bouncetime=1000)
# GPIO.add_event_detect(sub_sw_pin, GPIO.FALLING, callback=sub_on, bouncetime=1000)
GPIO.add_event_detect(sub_sw_pin, GPIO.RISING, callback=sub_on, bouncetime=1000)

print ("Waiting for input ... ")

try:
    while 1: # Keep idle and listen for input
        time.sleep(1)
except KeyboardInterrupt:
    print ("Exiting ...")
    GPIO.cleanup()
    power_off(25)
    ser.close()
    print ("Have a nice day!")
