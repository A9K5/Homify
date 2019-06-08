
import RPi.GPIO as GPIO
import time

#######################
# Pin config over here
NightLamp = 3
TubeLight = 5
Fan = 7
#######################
# Pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(NightLamp, GPIO.OUT)
GPIO.setup(TubeLight, GPIO.OUT)
GPIO.setup(Fan, GPIO.OUT)
#######################



GPIO.add_event_detect(3, GPIO.BOTH)
GPIO.add_event_detect(5, GPIO.BOTH)
GPIO.add_event_detect(7, GPIO.BOTH)

def my_callback():
    print("Detected first callback");

GPIO.add_event_callback(3, my_callback)









# import RPi.GPIO as GPIO
# import time
# LedPin = 11    # pin11
# ###############################
# #   the other pin is connected to the
# #   
# ###############################
# def setup():
#   GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
#   GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
#   GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led

# def blink():
#   while True:
#     GPIO.output(LedPin, GPIO.HIGH)  # led on
#     time.sleep(1)
#     GPIO.output(LedPin, GPIO.LOW) # led off
#     time.sleep(1)

# def destroy():
#   GPIO.output(LedPin, GPIO.LOW)   # led off
#   GPIO.cleanup()                  # Release resource

# if __name__ == '__main__':     # Program start from here
#   setup()
#   try:
#     blink()
#   except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#     destroy()