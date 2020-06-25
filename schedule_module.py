# schedule_module.py - Supplies the Schedule class and associated helper
# functions.  The Schedule class is essentially a list of Shift objects and a
# list of Request objects with methods to search both lists.

# TO-DO
# 1.  Schedule.__str__()
# 2.  Remove shifts/requests by date and short name?  Right now can only remove
# by having a handle to the shift/request object to be removed.
# 3.  How can we combine two Schedule objects into one?
# 4.  When adding Shift/Requests OR when combining two Schedule objects, we
# need to weed out duplicates.

# Standard Library Imports
import datetime as dt

# Local Application Imports
import shift_module
import request_module
import assignments_module

# The actual Schedule class
class Schedule:
    def __init__(self):
        self.requests = [] # Will be a list of Request objects
        self.shifts = [] # Will be a list of Shift objects

    def add_request(self, request):
        self.requests.append(request)

    def add_shift(self, shift):
        self.shifts.append(shift)

    def remove_request(self, request):
        self.requests.remove(request)

    def remove_shift(self, shift):
        self.shifts.remove(shift)

    def num_of_shifts(self):
        return len(self.shifts)

    def num_of_requests(self):
        return len(self.requests)

    def is_empty(self):
        """Returns True if there are no Shift or Request objects in this
        Schedule; False otherwise."""
        if self.num_of_shifts() > 0:
            return False
        if self.num_of_requests() > 0:
            return False
        return True

    def first_date(self):
        """Returns a DateTime object with the earliest date (NOT time!) that 
        a Request or Shift object in this Schedule has.  Returns None if there 
        are no Request or Shift objects in this Schedule."""
        if self.is_empty() == True:
            return None
        dates_in_sched = []
        for shift in self.shifts:
            dates_in_sched.append(shift.start_time)
        for request in self.requests:
            dates_in_sched.append(request.date)
        first_datetime = min(dates_in_sched)
        first_date = first_datetime.date()
        return first_date

    def last_date(self):
        """Returns a DateTime object with the latest date (NOT time!) that a 
        Request or Shift object in this Schedule has.  Returns None if there 
        are no Request or Shift objects in this Schedule."""
        if self.is_empty() == True:
            return None
        dates_in_sched = []
        for shift in self.shifts:
            dates_in_sched.append(shift.start_time)
        for request in self.requests:
            dates_in_sched.append(request.date)
        last_datetime = max(dates_in_sched)
        last_date = last_datetime.date()
        return last_date

# Unit test script for the Schedule class
def unit_tests():
    print("schedule_module.py supplies the Schedule class and associated")
    print("helper functions.  When run directly (as you are doing now), it ")
    print("runs a series of unit tests on the class and helper functions.\n")

    test_shift = shift_module.Shift("8m", dt.datetime(1978, 9, 17))
    test_request = request_module.Request("B", dt.datetime(1215, 6, 15))
    test_schedule = Schedule()

    assert test_schedule.num_of_shifts() == 0
    assert test_schedule.num_of_requests() == 0
    assert test_schedule.is_empty() == True
    test_schedule.add_shift(test_shift)
    test_schedule.add_request(test_request)
    assert test_schedule.num_of_shifts() == 1
    assert test_schedule.num_of_requests() == 1
    assert test_schedule.is_empty() == False
    test_schedule.remove_shift(test_shift)
    test_schedule.remove_request(test_request)
    assert test_schedule.num_of_shifts() == 0
    assert test_schedule.num_of_requests() == 0
    assert test_schedule.is_empty() == True
    print("1.  Schedule passes tests for add/subtract shifts/requests, \n"
          "num_of_shifts/requests, and is_empty()!")

    test_schedule = assignments_module.read_assignments("Test Files/" + \
        "February 2020 Assignments.xls")
    print(test_schedule.num_of_shifts())
    print(test_schedule.num_of_requests())
    print(test_schedule.first_date())
    print(test_schedule.last_date())

if __name__ == "__main__":
    unit_tests()
