import os
from datetime import datetime
from event import *
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
		file = open(self.file_name, "r")
		contents = file.read()
		events = json.loads(contents)["events"]
		file.close()
		return events

	def save_event_log(self, events):
		if os.path.exists(self.file_name):
			os.remove(self.file_name)
		file = open(self.file_name, 'w+')
		json.dump(events, file)
		file.close()
