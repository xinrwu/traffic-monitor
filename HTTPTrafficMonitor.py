import operator
import time
from datetime import datetime
from LogMonitor import LogMonitor
from threading import Timer

SUMMARY_INTERVAL = 10 # seconds
FILE_NAME = input("Path to access log:\n")
THRESHOLD = int(input("Threshold to be alerted at:\n"))
FMT = "%d/%b/%Y:%H:%M:%S"

monitor = LogMonitor(THRESHOLD)

def schedule_report(task):
    thread = Timer(SUMMARY_INTERVAL, schedule_report, [task])
    task()
    thread.start()

def get_info():
    section_stats = monitor.get_section_stats()
    status_stats = monitor.get_status_stats()
    ip_stats = monitor.get_ip_stats()
    byte_stats = monitor.get_top_objects()
    sorted_section_stats = sorted(section_stats.items(), key=operator.itemgetter(1), reverse=True)
    print("Section Summary")
    print("---------------------------")
    for section in sorted_section_stats:
        print("%s - %d" % (section[0], section[1]))
    print("Status Summary")
    print("---------------------------")
    for status in status_stats:
        print("%s - %d" % (status, status_stats[status]))
    print("IP Summary")
    print("---------------------------")
    for ip in ip_stats:
        print("%s - %d" % (ip, ip_stats[ip]))
    print("Top 10 object data returned to client")
    print("---------------------------------------")
    for obj in byte_stats:
        print("%s - %s" % (obj[1], obj[0]))

file = open(FILE_NAME, 'r')
schedule_report(get_info)
# credit to http://code.activestate.com/recipes/157035-tail-f-in-python/ for accessing data constantly written
while True:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
        new_time = datetime.now().strftime(FMT)
        monitor.check_traffic(new_time)
    else:
        try:
            monitor.add(line)
        except ValueError:
            pass

