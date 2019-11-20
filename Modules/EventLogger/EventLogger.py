import os
from datetime import datetime
from Event import *
import json


class EventLogger:
	def __init__(self, file_name):
		self.file_name = file_name
		self.event_id = self.get_last_event_id()

	def add_entry(self, lunches, user_id):
		timestamp = str(datetime.now())
		events = self.get_events_from_file()
		new_event = Event(self.event_id+1, timestamp, user_id, lunches)
		events.append(new_event.__dict__)
		self.save_event_log(events)
		self.event_id = self.event_id + 1

	def get_current_event_id(self):
		return self.event_id

# todo
	def get_last_event_id(self):
		if os.path.exists(self.file_name):
			events = self.get_events_from_file()
			last_event = events[-1]
			return last_event["id"]
		else:
			return 0

	def get_events_from_file(self):
		if not os.path.exists(self.file_name):
			return []
		file = open(self.file_name, "r")
		contents = file.read()
		events = json.loads(contents)
		file.close()
		return events

	def save_event_log(self, events):
		if os.path.exists(self.file_name):
			os.remove(self.file_name)
		file = open(self.file_name, 'w+')
		json.dump(events, file)
		file.close()

	def get_storage_state(self):
		events = self.get_events_from_file()
		if not events:
			exit("ERROR 01 - NO LOG FILE FOUND WHEN TRYING TO GET STORAGE STATE")
		return events[-1]["lunches"]


if __name__ == '__main__':
	logger = EventLogger('log.txt')
	# initialize log with full storage
	logger.add_entry([8, 8, 8, 8], 00)
	storage = logger.get_storage_state()
	storage[3] -= 1
	logger.add_entry(storage, 32)
	storage[1] -= 2
	logger.add_entry(storage, 2)
	storage[0] -= 3
	logger.add_entry(storage, 5)
