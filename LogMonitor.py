from datetime import datetime, timedelta
from llist import dllist
from LogInfo import LogInfo
import heapq

class LogMonitor(object):

    def __init__(self, threshold, recent_time=120):
        """Processes information received from log data

        Args:
            threshold (int): greater than this amount within recent_time causes alert
            recent_time (int): time window in seconds to consider traffic
        """
        self.recent_traffic = dllist()
        self.recent_time = recent_time
        self.threshold = threshold
        self.section_stats = dict()
        self.status_stats = dict()
        self.ip_stats = dict()
        self.bytes = []
        self.alert = False

    def add(self, line):
        """Adds line of log data to stats.

        Args:
            line (str): line of Common Log Format data
        Raises:
            ValueError: invalid format of string
        """
        log = LogInfo(line)
        # add
        new_time = log.get_datetime()
        self.recent_traffic.appendright(new_time)
        # statistics update
        self._update_stats(self.section_stats, log.get_section())
        self._update_stats(self.status_stats, log.get_status())
        self._update_stats(self.ip_stats, log.get_ip())
        size = log.get_bytes()
        site = log.get_resource()
        if len(self.bytes) > 9:
            heapq.heappushpop(self.bytes, (size, site))
        else:
            heapq.heappush(self.bytes, (size, site))
        self.check_traffic(new_time)

    def check_traffic(self, new_time):
        """Checks the traffic relative to new_time.

        Args;
            new_time (str): current time in the format DD/mm/YYYY:HH:MM:SS
        """
        self._remove_overdue(new_time)
        self._alert_change(len(self.recent_traffic) > self.threshold, new_time)

    def get_section_stats(self):
        """Returns sections visited amount.
        """
        return self.section_stats

    def get_status_stats(self):
        """Returns status returned amount.
        """
        return self.status_stats

    def get_ip_stats(self):
        """Returns ip address visited amount.
        """
        return self.ip_stats

    def get_top_objects(self):
        """Returns the top 10 objects returned to client.
        """
        return self.bytes

    def _update_stats(self, storage, data):
        if data in storage:
            storage[data] += 1
        else:
            storage[data] = 1

    def _remove_overdue(self, new_time):
        fmt = "%d/%b/%Y:%H:%M:%S"
        while len(self.recent_traffic) > 0:
            old_time = self.recent_traffic[0]
            tdelta = datetime.strptime(new_time, fmt) - datetime.strptime(old_time, fmt)
            if tdelta.total_seconds() > self.recent_time:
                self.recent_traffic.popleft()
            else:
                break

    def _alert_change(self, new_alert, time):
        if self.alert != new_alert:
            if new_alert:
                print("High traffic generated an alert - hits =", len(self.recent_traffic)
                      , "trigger at", time)
            else:
                print("Alert recovered at", time)
            self.alert = new_alert

