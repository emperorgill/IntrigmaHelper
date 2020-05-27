"""AACC_dates.py - supplies functions for predicting when certain AACC shifts
will or will not occur. Uses Config Files/AACC Dates.txt to see when these
shifts occured in May 2020.  Can count backwards or forwards in time."""

# Standard Library Imports
import datetime as dt

# Third Party Imports

# Local Application Imports

# Constants
KEY_FILE = "Config Files/AACC Dates.txt"
# Make sure you read the file from disk just once

# Functions

def predict_AACC_dates(month = "July 2020", shift_type = "t24",
        shift_onoff = "ON"):
    """Returns a string telling when a specified AACC shift will or will not
    occur in a specified month.  Month can be specified in formats of
    "July 2020", "Jul 2020", "7/2020", "7/20".  Shift_type will be
    "T.", "T6.", "t8s", "t24".  Upper, lower, or mixed case is acceptable.  If
    shift_onoff is "ON" then the string will say what dates the shifts ARE
    occurring.  If shift_onoff is "OFF" then the string will say what dates
    the shifts ARE NOT occurring.  Again, upper/lower/mixed case is acceptable.
    If month is "-h" or "-help", return a user friendly explanation of how
    to use the function.  If input is bad in some other way, return a user
    friendly explanation."""
    pass

def is_it_AACC_shift(date, shift_type):
    """Called by predict_AACC_dates.  Given a date as a Datetime object and
    a shift_type as a string, returns true if that shift occurs on that date
    or false if it does not occur."""
    pass

def unit_tests():
    print("AACC_dates.py supplies functions needed to tell when AACC shifts")
    print("occur in the future.  When run directly (as you are doing now), it")
    print("runs a series of unit tests.\n")

    # Insert your file-reading/setup code here.
    
    assert is_it_AACC_shift(dt.datetime(2020, 6, 3), "T24") = True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 2), "T24") = False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 9), "T8S") = True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 12), "T8S") = False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 27), "T6.") = True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 28), "T6.") = True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 29), "T6.") = False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 12), "T.") = True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 11), "T.") = False

if __name__ == "__main__":
    unit_tests()
