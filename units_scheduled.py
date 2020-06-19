# units_scheduled.py - supples the units_scheduled function and associated
# helper functions.

# TO-DO
# 1.  Write the program.

# Standard Library Imports
import datetime as dt

# Local Application Imports
import shift_module
import request_module
import schedule_module
import assignments_module

def units_scheduled(filename):
    """Receives a Schedule object and returns a text table describing how
    many units were worked each day in the various areas the ED must staff.
    Ignores any shift whose "doctor" has a name that starts with three
    asterisks as these are placeholders for shifts that were not worked e.g.
    ***CANCELLED*** ***ORPHAN*** and the like."""
    schedule = assignments_module.read_assignments(filename)
    if schedule.is_empty == True:
        return str(filename) + " contains an empty schedule!\n")
    
