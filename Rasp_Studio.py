# Raspberry Pi studio control software
# Version 0.1.2
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

print "Initializing, please wait ..."
main_sw_pin = 25 # Pin for main switch
sub_sw_pin = 24 # Pin for secondary switch

led_pin = 23 # Pin for main status LED

main_power_pins = [7, 8, 9} # TODO: figure out which is which
sub_power_pins = [10, 11, 22, 21]

power_delay = 0.5 # Delay in s between sequentially powering on devices

power_flag = 0 # Flag for main power status
sub_flag = 0 # Flag for sub power status

GPIO.setup(main_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Initializing input pins
GPIO.setup(sub_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(led_pin, GPIO.OUT) # Initializing led pin

GPIO.setup(main_power_pins + sub_power_pins, GPIO.OUT, initial=GPIO.HIGH) # Initilizing power pins

def power_off(channel):# Turning main power off sequentially in reverse order
    global power_flag
    if sub_flag: # Turning sub power off if on
        print "Turning off sub power first"
        sleep(2.5)
        sub_off(main_sw_pin)
    for pin in main_power_pins:
        GPIO.output(relay_1c_pin, GPIO.HIGH)
        time.sleep(power_delay)
    GPIO.output(led_pin, GPIO.LOW) # Led off
    power_flag = 0
    print "Main power turned off"

def power_on(channel):
    print "Toggling main power"
    global power_flag
    for pin in main_power_pins:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(power_delay)
    power_flag = 1 # Led on
    print "Main power turned on"

def sub_off(channel):
    global sub_flag # Turning sub power off sequentially in reverse order
    print "Turning off sub power"
    for pin in sub_power_pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(power_delay)
    sub_flag = 1
    print "Sub power turned off"
        
def sub_on(channel):
    global sub_flag # Turning sub power on sequentially
    if power_flag: 
    print "Turning on sub power"
    for pin in sub_power_pins:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(power_delay)
    sub_flag = 0
    print "Sub power turned on"

GPIO.add_event_detect(main_sw_pin, GPIO.FALLING, callback=power_on, bouncetime=1000) # Set up triggers
GPIO.add_event_detect(main_sw_pin, GPIO.RISING, callback=power_off, bouncetime=1000)
GPIO.add_event_detect(sub_sw_pin, GPIO.FALLING, callback=sub_on bouncetime=1000)
GPIO.add_event_detect(sub_sw_pin, GPIO.RISING, callback=sub_off bouncetime=1000)

print "Waiting for input ... "

try:
    while 1: # Keep idle and listen for input
        time.sleep(1)
except KeyboardInterrupt:
    print "Exiting ..."
    GPIO.cleanup()
    print "Have a nice day!"