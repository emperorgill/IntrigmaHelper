# request_module.py - Supplies the Request class and associated helper functions.

# TO-DO
# 1.  Implement the hours in a pp/pp2 request
# 2.  More tests

# Standard Library Imports
import datetime as dt
import sys

# Third Party Imports
import openpyxl as xl

# Local Application Imports
import exceptions

# Global variables
RECOGNIZED_REQUEST_TYPES = [] # Will load from config file

# Helper functions
def load_request_types(filename = "Config Files/Request Types.txt"):
    """Given a lookup table of request types, load the types into a global
    variable list."""
    global RECOGNIZED_REQUEST_TYPES

    # Read the request type file, leaving out the comments and blank lines
    try:
        file_handle = open(filename, "rt")
        for line in file_handle.readlines():
            if (line[0] == "#" or line == "\n"):
                continue
            else:
                RECOGNIZED_REQUEST_TYPES.append(line.strip())
        file_handle.close()
    except Exception as e:
        print(e)
        # Probably file not found
        print("Error in request_module/load_request_types - could not" +
              " open " + filename)
        sys.exit(1)

def is_a_request(request_type):
    """Tell if the received request_type (a string) is a a request type that
    this module knows about."""
    # If RECOGNIZED_REQUEST_TYPES is an empty list, load from file
    if not RECOGNIZED_REQUEST_TYPES:
        load_request_types()
    if request_type in RECOGNIZED_REQUEST_TYPES:
        return True
    else:
        return False

# Individual unit test functions
def test_request_properties(request, expected_properties):
    """Receive a Request object and make sure its properties match those in the
    expected_properties list.  For unit testing, not production."""
    assert request.request_type == expected_properties[0]
    assert request.date == expected_properties[1]

# The actual Request class
class Request:
    def __init__(self, request_type, date, doctor = None):        
        # If request_name is not a recognized type of request, complain
        if is_a_request(request_type) == False:
            raise exceptions.BadRequestType("Error in request_module/Request " +
                "constructor.  {} is not in the list of " +
                "RECOGNIZED_REQUEST_TYPES.".format(request_type))
        self.request_type = request_type # String
        self.date = date # Datetime object
        self.doctor = doctor # String or None
        # Leave the hours in a pp/pp2 request unimplemented for now

    def __str__(self):
        """Return a human readable string representation of the Request object"""
        output = self.request_type + " is a request on " + \
            self.date.strftime("%m/%d/%Y") + " for " + str(self.doctor)
        return output

# Unit test script for the Request class
def unit_tests():
    print("request_module.py supplies the Request class and associated helper")
    print("functions.  When run directly (as you are doing now), it runs a")
    print("series of unit tests on the class and helper functions.\n")

    test_request = Request("P", dt.datetime(1918, 11, 11))
    test_request_properties(test_request, ["P", dt.datetime(1918, 11, 11)])
    print("P Request object properties test OK!\n")

    print("And here's the __str__ for the P request...")
    print(test_request)

    try:
        Request("foo", dt.datetime(1974, 8, 1))
    except exceptions.BadRequestType:
        print("\nBad Request object error catching tests OK!")

    assert is_a_request("B") == True
    print("\nis_a_request() tests OK for true case!")
    assert is_a_request("Gill da Great") == False
    print("is_a_request() tests OK for false case!")

if __name__ == "__main__":
    unit_tests()
