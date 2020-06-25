"""credit_lookup_module.py - Supplies the credit_lookup function and 
associated other functions.  Relies on the presence of "Credit Scoring.txt"
(a plaintext configuration file) to simplify the code."""

# This file was scrapped when it was realized that it doesn't remove the
# requirement for SACROS Lookup Table.xlsx - we still need that file to get
# shift start times/end times/hours paid, etc.  So we might as well get 
# credit info from there too.

# TO-DO
# 1.  Make sure t8s/t8s, C4+/t1, C4+/t8 don't get double weekend credit
# 2.  Make it so we only load the config table once
# 3.  Finish the uncoded sections below (these are comments not followed by code)
# 4.  Unit tests (this file is poorly tested so be careful!)

# BEWARE: If a new shift that's supposed to get call credit OR no credit
# is added to the schedule but NOT added to Credit Scoring.txt, this program
# will proceed as if it that shift is just an ordinary, credit-deserving
# shift without flagging any error!

# Standard Library Imports
import datetime as dt

# Local Application Imports
from exceptions import BadInput, BadInputFile

# Functions
def credit_lookup(shift_name, start_time, end_time):
    """Receive shift_name as string and start_time and end_time as datetime 
    objects.  Use the "Credit Scoring.txt" configuration file to figure out 
    Early Credits, Late Credits, Night Credits, Call Credits, Friday Credits, 
    Weekend Credits, and Total Credits.  Sum these as appropriate and return a
    single credit score for the shift."""
    # Sensibility checking...
    if start_time > end_time:
        raise exceptions.BadInput("Start_time of " + str(start_time) + \
            " is greater than end time of " + str(end_time))
    
    # Read the contents of the configuration file into variables
    early_credits_table = {}
    late_credits_table = {}
    friday_credits_table = {}
    call_shifts_list = []
    no_credit_shifts_list = []
    early_credits_table, late_credits_table, friday_credits_table, \
        call_shifts_list, no_credit_shifts_list = read_config_file()
        
    # Initialize credit variables
    early_credits = 0
    late_credits = 0
    night_credits = 0
    call_credits = 0
    friday_credits = 0
    weekend_credits = 0
    
    # If the shift is on the no_credit_shifts list, then the values above
    # are the final values.
    if shift_name in no_credit_shifts_list:
        return 0
    
    # Use the start_time of the shift to figure out if there are any early
    # credits
    if start_time in early_credits_table:
        early_credits = early_credits_table[start_time]
        
    # Use the end_time of the shift to figure out late credits (if any)
    if end_time in late_credits_table:
        late_credits = late_credits_table[end_time]
        
    # A night shift is one that starts on a given day and ends at 0400 or
    # later on the FOLLOWING day.  Gets 1 night credit.
    
    
    # Give 1 call credit if the shift is in the call_shifts_list
    if shift_name in call_shifts_list:
        call_credits = 1
    
    # If the shift starts on Friday, consider awarding Friday credits
    
    # If the shift starts between midnight Fri/Sat and midnight Sun/Mon,
    # award a weekend credit.
    
    # Return the sum of all applicable credits to the calling function.
    total_credits = early_credits + late_credits + night_credits + \
        call_credits + friday_credits + weekend_credits
    return total_credits    
    
    
def read_config_file(filename = "Config Files/Credit Scoring.txt"):
    """Receive a filename to a credit lookup configuration file.  Read that
    file, remove the comments/blank lines, change times to datetime objects,
    and return a tuple of data structures of the contents."""
    
    # Useful variables
    file_contents = [] # Comes from the config file.  As we process the lines
                        # in this list, we'll remove them.
    
    # Variables to return to the calling function
    early_credits = {} # Key is datetime object of startime, value is # credits
    late_credits = {} # Same keys and values as above
    friday_credits = {} # Same keys and values as above
    call_shifts = [] # A simple list of call shifts
    no_credit_shifts = [] # A simple list of shifts that get no credit

    # Read the config file, leaving out the comments and blank lines
    try:
        file_handle = open(filename, "rt")
        for line in file_handle.readlines():
            if (line[0] == "#" or line == "\n"):
                continue
            else:
                file_contents.append(line)            
        file_handle.close()
    except FileNotFoundError:
        raise exceptions.BadInputFile("Error while attempting to open " + \
              filename)

    file_contents, early_credits = get_typea_list(file_contents, 
            "Early shifts\n")
    file_contents, late_credits = get_typea_list(file_contents, 
            "Late shifts\n")
    file_contents, friday_credits = get_typea_list(file_contents,
            "Friday shifts\n")
    file_contents, call_shifts = get_typeb_list(file_contents)
    file_contents, no_credit_shifts = get_typeb_list(file_contents)
    return (early_credits, late_credits, friday_credits, call_shifts,
            no_credit_shifts)


def get_typea_list(file_contents, first_delimiter):
    """Processes a "Type A list" from the configuration file.  The list will
    be found between the first delimiter and the next line that starts with a 
    letter.  The list will have a shift on each line.  First is the time (a 
    string in 24 hour format) and then is a tab and then is the shift credits 
    (a float in string format).  Process these into a dictionary and remove the 
    lines that were processed from file_contents.  Return the results."""
    output_dict = {}
    useful_data = []
    did_we_find_first_delimiter = False
    # Get the part of file_contents we're interested in.  Skip the line that
    # has the first_delimiter and then process till we hit a line that starts
    # with a #.
    for line in file_contents:
        if line == first_delimiter:
            did_we_find_first_delimiter = True
            continue
        if (line[0].isnumeric() == False and \
            did_we_find_first_delimiter == True):
            break
        if (line != first_delimiter and did_we_find_first_delimiter == True):
            useful_data.append(line)
            
    # Now remove the lines we pulled from file_contents (couldn't do this
    # above because we can't alter a list as we iterate through it)
    file_contents.remove(first_delimiter)
    for line in useful_data:
        file_contents.remove(line)
    # Use the contents of foo to populate the early_credits dictionary
    for line in useful_data:
        start_time = dt.datetime.strptime(line.split()[0], "%H%M")
        credit = float(line.split()[1])
        output_dict[start_time] = credit
    # All done!
    return file_contents, output_dict


def get_typeb_list(file_contents):
    """Processes a "Type B list" from the configuration file.  There's a title
    line which needs to be dumped.  The line after the title line is a line of 
    comma separated strings.  Grab, process, and return that list then dump
    that line as well.  Return the list and what remains of file_contents."""
    output_list = []
    title_line = file_contents[0]
    our_list = file_contents[1]
    output_list = our_list.strip().split(",")
    file_contents.remove(title_line)
    file_contents.remove(our_list)
    return file_contents, output_list


def run_tests():
    print("credit_lookup_module.py supplies functions to figure out the")
    print("credit of various shifts.  When run directly (as you are doing")
    print("now), it runs a series of tests on those functions.")

    credit_lookup("4m", dt.datetime(1900, 1, 1, 4, 0, 0), 
                  dt.datetime(1900, 1, 1, 12, 0, 0))


if __name__ == "__main__":
    run_tests()
