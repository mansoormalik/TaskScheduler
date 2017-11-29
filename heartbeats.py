import time
import threading

"""
This class uses locks to ensure that it is thread safe. The heartbeats 
are being updated as messages are received from slaves. They are also
being examined and updated in a seperate thread that runs at fixed intervals
to verify which slaves have timed out. Therefore locks are required.
"""
class Heartbeats:
    def __init__(self):
        self.last_heartbeat = time.time()
        self.missed_consec_heartbeats = 0
        self._lock = threading.Lock()

    def set_new_heartbeat(self):
        self.last_heartbeat = time.time()
        with self._lock:
            self.missed_consec_heartbeats = 0
        
    def add_missed_heartbeat(self):
        with self._lock:
            self.missed_consec_heartbeats += 1

    def get_last_heartbeat(self):
        return self.last_heartbeat

    def get_missed_consec_heartbeats(self):
        return self.missed_consec_heartbeats

