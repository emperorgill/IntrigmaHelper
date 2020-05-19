# request_module.py - Supplies the Request class and associated helper functions.

# TO-DO
# 1.  Implement the hours in a pp/pp2 request

# Imports
import datetime as dt
import openpyxl as xl

# Global variables
RECOGNIZED_REQUEST_TYPES = ["pp", "pp2", "P", "P*", "K", "?", "F", "B", "B*",
                            "s", "h", "AS", "W", "W*", "Wc", "We", "Wa", "Wd",
                            "Wn", "X", "J", "SS", "SE", "M", "MD"]

# Helper functions
def is_a_request(request_type):
    """Tell if the received request_type (a string) is a a request type that
    this module knows about."""
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
        if request_type not in RECOGNIZED_REQUEST_TYPES:
            raise ValueError("Error in Request constructor.  {} not in list of"
                             " RECOGNIZED_REQUEST_TYPES.".format(request_type))
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
    except ValueError:
        print("\nBad Request object error catching tests OK!")

    assert is_a_request("B") == True
    print("\nis_a_request() tests OK for true case!")
    assert is_a_request("Gill da Great") == False
    print("is_a_request() tests OK for false case!")

if __name__ == "__main__":
    unit_tests()
