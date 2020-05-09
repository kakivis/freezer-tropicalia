import RPi.GPIO as GPIO
from time import sleep


class Servo:
    def __init__(self, out):
        # initialize
        GPIO.setwarnings(False)
        GPIO.setup(out, GPIO.OUT)
        self.pin = out
        self.pwm = GPIO.PWM(out, 50)  # setup frequency
        self.pwm.start(0)  # starts with 0% duty cycle

    # changes servo angle
    def set_angle(self, angle):
        if int(angle) < -60 or int(angle) > 60:
            return

        duty = (90 + int(angle)) / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)
