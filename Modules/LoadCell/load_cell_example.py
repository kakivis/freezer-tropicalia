import RPi.GPIO as GPIO
import time
import sys
from LoadCell import LoadCell

DOUT_BCM = 4
PD_SCK_BCM = 18
GPIO.setmode(GPIO.BCM)
cell_1 = LoadCell(DOUT_BCM, PD_SCK_BCM)


def clean_and_exit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


def setup():
    # cell_1.set_offset(8449282.59375)
    # cell_1.set_scale(182.18)
    # cell_1.tare()
    pass


def loop():

    try:
        val = cell_1.read_average(32)
        print "{}\n".format(val)

        cell_1.power_down()
        time.sleep(2)
        cell_1.power_up()

        # time.sleep(2)
        # raw_input("press enter to measure again\n")
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()


if __name__ == "__main__":

    setup()
    while True:
        loop()
