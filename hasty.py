# hasty.py - a hasty script written to track down missing shifts in a
# schedule object.

# Standard Library Imports
import datetime as dt

# Local Application Imports
import shift_module
import request_module
import schedule_module
import assignments_module


schedule = assignments_module.read_assignments("September 2020.xls")
if schedule.is_empty == True:
    print (str(filename) + " contains an empty schedule!\n")

for shift in schedule.shifts:
    if shift.location == "Sacramento"and shift.start_time.date() == \
            dt.datetime(2020, 9, 29).date():
        print(shift)