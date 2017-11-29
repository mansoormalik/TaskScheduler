import time

class Heartbeats:
    def __init__(self):
        self.last_heartbeat = time.time()
        self.missed_consec_heartbeats = 0

    def set_new_heartbeat(self):
        self.last_heartbeat = time.time()
        self.missed_consec_heartbeats = 0
        
    def add_missed_heartbeat(self):
        self.missed_consec_heartbeats += 1

    def get_last_heartbeat(self):
        return self.last_heartbeat

    def get_missed_consec_heartbeats(self):
        return self.missed_consec_heartbeats

