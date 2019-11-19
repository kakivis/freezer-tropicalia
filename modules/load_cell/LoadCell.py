import RPi.GPIO as GPIO
import time
import sys


class LoadCell:
	AVERAGE_LUNCH_WEIGHT = 400

	def __init__(self, dout, pd_sck, gain=128):
		self.GAIN = 0
		self.OFFSET = 0
		self.SCALE = 1

		GPIO.setmode(GPIO.BCM)

		self.PD_SCK = pd_sck
		self.DOUT = dout

		GPIO.setup(self.PD_SCK, GPIO.OUT)

		GPIO.setup(self.DOUT, GPIO.IN)

		self.power_up()
		self.set_gain(gain)

	def set_gain(self, gain=128):

		if gain is 128:
			self.GAIN = 3
		elif gain is 64:
			self.GAIN = 2
		elif gain is 32:
			self.GAIN = 1
		else:
			self.GAIN = 3  # Sets default GAIN at 128

		GPIO.output(self.PD_SCK, False)
		self.read()

	def set_scale(self, scale):
		self.SCALE = scale

	def set_offset(self, offset):
		self.OFFSET = offset

	def get_scale(self):
		return self.SCALE

	def get_offset(self):
		return self.OFFSET

	def read(self):

		while not (GPIO.input(self.DOUT) == 0):
			pass

		count = 0

		for i in range(24):
			GPIO.output(self.PD_SCK, True)
			count = count << 1
			GPIO.output(self.PD_SCK, False)
			if GPIO.input(self.DOUT):
				count += 1

		GPIO.output(self.PD_SCK, True)
		count = count ^ 0x800000
		GPIO.output(self.PD_SCK, False)

		for i in range(self.GAIN):
			GPIO.output(self.PD_SCK, True)
			GPIO.output(self.PD_SCK, False)

		return count

	def read_average(self, times=32):
		total = 0
		for i in range(times):
			total += self.read()
		return total / times

	def get_grams(self, times=32):
		value = (self.read_average(times) - self.OFFSET)
		grams = (value / self.SCALE)
		return grams

	def tare(self, times=32):
		weight = self.read_average(times)
		self.set_offset(weight)

	def power_down(self):
		GPIO.output(self.PD_SCK, False)
		GPIO.output(self.PD_SCK, True)

	def power_up(self):
		GPIO.output(self.PD_SCK, False)

	def get_packed_lunches(self):
		n_lunches = int(round(self.get_grams() / self.AVERAGE_LUNCH_WEIGHT))
		self.power_down()
		time.sleep(.001)
		self.power_up()
		return n_lunches
