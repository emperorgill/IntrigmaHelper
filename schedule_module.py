# schedule_module.py - Supplies the Schedule class and associated helper
# functions.  The Schedule class is essentially a list of Shift objects and a
# list of Request objects with methods to search both lists.

# TO-DO
# 1.  Schedule.__str__()

# Standard Library Imports
import datetime as dt

# Local Application Imports
import shift_module
import request_module

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
    test_schedule.add_shift(test_shift)
    test_schedule.add_request(test_request)
    assert test_schedule.num_of_shifts() == 1
    assert test_schedule.num_of_requests() == 1
    test_schedule.remove_shift(test_shift)
    test_schedule.remove_request(test_request)
    assert test_schedule.num_of_shifts() == 0
    assert test_schedule.num_of_requests() == 0
    print("Schedule passes tests for add/subtract shifts/requests and "
          "num_of_shifts/requests!")

if __name__ == "__main__":
    unit_tests()
