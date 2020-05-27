"""AACC_dates.py - supplies functions for predicting when certain AACC shifts
will or will not occur. Uses Config Files/AACC Dates.txt to see when these
shifts occured in May 2020.  Can count backwards or forwards in time."""

# Standard Library Imports
import datetime as dt
import sys

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
    
    # check/process user input: make uppercase
    # if bad, return explanation
    output = ""
    month = month.upper().strip()
    shift_type = shift_type.upper().strip()
    shift_onoff = shift_onoff.upper().strip()
    # Check the user input for month; format into 7/2020
    try:
        acceptable_months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", \
                             "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", \
                             "NOVEMBER", "DECEMBER"]
        month = month.replace(" ", "/", 1)
        month_parts = month.split("/")
        if len(month_parts) != 2:
            output = output + \
                     "Please enter a month in the format 'July 2020', "+ \
                     "'Jul 2020' '7/2020', or '7/20'.\n"
            return output
        month_parts[0] = month_parts[0].strip()
        month_parts[1] = month_parts[1].strip()
        
        if month_parts[0].isalpha(): # If the month is spelled out
                        
    except Exception as e:
        print(e)
        # Probably bad month input
        output = output + \
                 "Please enter a month in the format 'July 2020', "+ \
                 "'Jul 2020' '7/2020', or '7/20'.\n"
        return output
    #check shift_type is ok
    #check shift_onoff is ok
        

    # load file + create list of shift dates for the given shift_type
    shift_dates = []
    try:
        file_handle = open(KEY_FILE, "rt")
        lines = file_handle.readlines()
        """
            if (line[0] == "#" or line == "\n"):
                continue
            else:
        """
        #find correct shift header. add dates to shift_dates
        #(make datetime objects?)
        file_handle.close()
    except Exception as e:
        print(e)
        # Probably file not found
        print("Error in AACC_dates/predict_AACC_dates - could not" +
              " open " + KEY_FILE)
        sys.exit(1)
    
    # parse user input: either a month or -help
        #if -help: return explanation
        # if month: call is_it_AACC_shift for each date & given shift type
            # also pass list shift_dates from the files

    
    output = "WARNING: This output does NOT take into account TPMG holidays.\n"
    output = output + "You will have to sort those out on your own!\n"
    return output

def is_it_AACC_shift(date, shift_type, shift_dates):
    """Called by predict_AACC_dates.  Given a date as a Datetime object and
    a shift_type as a string, returns true if that shift occurs on that date
    or false if it does not occur. Uses the list shift_dates as a guide."""
    pass

def unit_tests():
    print("AACC_dates.py supplies functions needed to tell when AACC shifts")
    print("occur in the future.  When run directly (as you are doing now), it")
    print("runs a series of unit tests.\n")

    # Insert your file-reading/setup code here.
    predict_AACC_dates("8/19")
    
    assert is_it_AACC_shift(dt.datetime(2020, 6, 3), "T24") == True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 2), "T24") == False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 9), "T8S") == True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 12), "T8S") == False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 27), "T6.") == True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 28), "T6.") == True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 29), "T6.") == False
    assert is_it_AACC_shift(dt.datetime(2020, 6, 12), "T.") == True
    assert is_it_AACC_shift(dt.datetime(2020, 6, 11), "T.") == False

if __name__ == "__main__":
    unit_tests()
