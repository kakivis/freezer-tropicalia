import os
from datetime import datetime
from event import *

class EventLogger:
	def __init__(self, file_name):
		self.file_name = file_name
		self.event_id = None

# todo
	def add_entry(self, lunches, user_id):
		timestamp = str(datetime.now())

# todo
	def get_current_event_id(self):
#		if self.event_id is None:


# todo
	def get_last_event_id(self):
		file = open(self.file_name, "r")
		last_line = file.readlines()[-1]
		file.close()
		return self.json_decode(last_line).id


# todo
	def json_decode(self, line):
		event_id = None
		timestamp = None
		user_id = None
		lunches = None
		return Event(event_id, timestamp, user_id, lunches)
