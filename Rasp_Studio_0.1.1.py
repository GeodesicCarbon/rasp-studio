import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

print "Initializing, please wait ..."
main_sw_pin = 25 # Pin for main switch
sub_sw_pin = 24 # Pin for secondary switch

led_pin = 23 # Pin for main status LED

relay_1a_pin = 7 # TODO: figure out which is which
relay_1b_pin = 8
relay_1c_pin = 9

relay_2a_pin = 10
relay_2b_pin = 11
relay_2c_pin = 22
relay_2d_pin = 21

power_delay = 0.5 # Delay in s between sequentially powering on devices

power_flag = 0 # Flag for main power status
sub_flag = 0 # Flag for sub power status

GPIO.setup(main_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Initializing input pins
GPIO.setup(sub_sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(led_pin, GPIO.OUT) # Initializing led pin

GPIO.setup(relay_1a_pin, GPIO.OUT, initial=GPIO.HIGH) # Initilizing main power pins
GPIO.setup(relay_1b_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relay_1c_pin, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(relay_2a_pin, GPIO.OUT, initial=GPIO.HIGH) # Initializing sub power pins
GPIO.setup(relay_2b_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relay_2c_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relay_2d_pin, GPIO.OUT, initial=GPIO.HIGH)

def power_off(channel):# Turning main power off sequentially in reverse order
	global power_flag
	if sub_flag: # Turning sub power off if on
		print "Turning off sub power first"
		sleep(2.5)
		sub_off(main_sw_pin)
	GPIO.output(relay_1c_pin, GPIO.HIGH)
	time.sleep(power_delay)
	GPIO.output(relay_1b_pin, GPIO.HIGH)
	time.sleep(power_delay)
	GPIO.output(relay_1a_pin, GPIO.HIGH)
	GPIO.output(led_pin, GPIO.LOW) # Led on
	power_flag = 0
	print "Main power turned off"

def power_on(channel):
    print "Toggling main power"
    global power_flag
	GPIO.output(relay_1a_pin, GPIO.LOW)
	time.sleep(power_delay)
	GPIO.output(relay_1b_pin, GPIO.LOW)
	time.sleep(power_delay)
	GPIO.output(relay_1c_pin, GPIO.LOW)
	GPIO.output(led_pin, GPIO.HIGH)
	power_flag = 1 # Led off
	print "Main power turned on"

def sub_off(channel):
    global sub_flag # Turning sub power off sequentially in reverse order
	print "Turning off sub power"
	GPIO.output(relay_2a_pin, GPIO.HIGH)
	time.sleep(power_delay)
	GPIO.output(relay_2b_pin, GPIO.HIGH)
	time.sleep(power_delay)
	GPIO.output(relay_2c_pin, GPIO.HIGH)
	time.sleep(power_delay)
	GPIO.output(relay_2d_pin, GPIO.HIGH)
	sub_flag = 1
	print "Sub power turned off"
		
def sub_on(channel):
	global sub_flag # Turning sub power on sequentially
	if power_flag: 
	print "Turning on sub power"
	GPIO.output(relay_2d_pin, GPIO.LOW)
	time.sleep(power_delay)
	GPIO.output(relay_2c_pin, GPIO.LOW)
	time.sleep(power_delay)
	GPIO.output(relay_2b_pin, GPIO.LOW)
	time.sleep(power_delay)
	GPIO.output(relay_2a_pin, GPIO.LOW)
	sub_flag = 0
	print "Sub power turned on"

GPIO.add_event_detect(main_sw_pin, GPIO.FALLING, callback=power_on, bouncetime=1000) # Set up triggers
GPIO.add_event_detect(main_sw_pin, GPIO.RISING, callback=power_off, bouncetime=1000)
GPIO.add_event_detect(sub_sw_pin, GPIO.FALLING, callback=sub_on bouncetime=1000)
GPIO.add_event_detect(sub_sw_pin, GPIO.RISING, callback=sub_off bouncetime=1000)

print "Waiting for input ... "

try:
    while 1: # Wait until input
        time.sleep(1)
except KeyboardInterrupt:
    print "Exiting ..."
    GPIO.cleanup()
    print "Have a nice day!"