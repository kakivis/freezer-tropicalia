from Modules.LoadCell.LoadCell import LoadCell
import RPi.GPIO as GPIO

A_IN = 5
A_OUT = 6
B_IN = 7  # check that pin
B_OUT = 8  # check that pin
C_IN = 9  # check that pin
C_OUT = 10  # check that pin
D_IN = 11  # check that pin
D_OUT = 12  # check that pin


class StorageManager:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.stack_a = LoadCell(A_OUT, A_IN)
		self.stack_b = LoadCell(B_OUT, B_IN)
		self.stack_c = LoadCell(C_OUT, C_IN)
		self.stack_d = LoadCell(D_OUT, D_IN)

	def getStorageState(self):
		a_lunches = self.stack_a.get_packed_lunches()
		b_lunches = self.stack_b.get_packed_lunches()
		c_lunches = self.stack_c.get_packed_lunches()
		d_lunches = self.stack_d.get_packed_lunches()
		return [a_lunches, b_lunches, c_lunches, d_lunches]

	def initializeLoadCells(self):
		self.stack_a.tare()
		self.stack_b.tare()
		self.stack_c.tare()
		self.stack_d.tare()

# TODO autocalibration ?
