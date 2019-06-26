import RPi.GPIO as GPIO
import time
import sys
from load_cell import LoadCell


cell_1 = LoadCell(5, 6)


def clean_and_exit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


def setup():
    cell_1.set_offset(8449282.59375)
    cell_1.set_scale(182.18)
    # cell_1.tare()
    pass


def loop():

    try:
        val = cell_1.get_grams(32)
        print "{} lunch(es) weighing {}g\n".format(int(round(val/400)), val)

        cell_1.power_down()
        time.sleep(.001)
        cell_1.power_up()

        # time.sleep(2)
        raw_input("press enter to measure again\n")
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()


if __name__ == "__main__":

    setup()
    while True:
        loop()
