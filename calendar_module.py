"""calendar_module.py - supplies functions for reading Intrigma's
Calendar Export and extracting useful information into a Schedule object.
When reviewing this module, it's good to have an example of Intrigma's
Calendar Export file in front of you or else none of the comments will make
any sense."""

# Note that we have to use the xlrd module rather than the more modern openpyxl
# (or others) because Intrigma exports in the older .xls format rather than
# .xlsx

# Note that in xlrd, the first row of the spreadsheet is 0 while in Excel, the
# first row is 1.  Similarly, the first col of the spreadsheet is 0 in xlrd
# but A in Excel.

# WARNING!!  Intrigma spreadsheets list MD names as first initial, last name
# so we do the same thing here.  If we ever get two docs with the same first
# initial, last name, things could BREAK!

# To Do
# 1.  ARE WE READING ALL SHIFTS IN THE FILE OR JUST THIS MONTH'S!!!
# 2.  Implement errors that bubble up smoothly to the user rather than simply
#       crash the program (see assignments_module for examples)
# 3.  Figure out how to redirect the xlrd "errors" (maybe... see URL noted in
# assignments_module for more details)
# 4.  Test to ensure handling two doctors assigned to one shift properly.

# Standard Library Imports
import sys
import datetime as dt

# Third Party Imports
import xlrd

# Local Application Imports
import shift_module
import schedule_module
from exceptions import BadInputFile

# Functions
def read_calendar(filename):
    """Read all of the assignments from a filename-specified Intrigma
    Calendar .xls file and return them in a Schedule object."""
    try:
        wb = xlrd.open_workbook(filename)
    except FileNotFoundError:
        raise FileNotFoundError("Error in calendar_module.py/read_calendar" + \
            " - couldn't find file " + filename)
    try:
        s = wb.sheet_by_index(0) # Just need the first sheet
        # The month and year of this calendar are in the first row, fifth cell...
        target_cell = s.cell(0, 4).value.split()
        month_as_text = target_cell[0]
        list_of_months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November",
                      "December"]
        month = list_of_months.index(month_as_text) + 1 # Months start at 1...
        year = int(target_cell[1])
    except:
        raise BadInputFile("Error in calendar_module/read_calendar" + \
            " - couldn't make sense of the first row, fifth column of " +
            filename)

    output = schedule_module.Schedule()
    
    # We need to find date headers but they can be almost anywhere in the file.
    # They do, however, take the form of month/number - e.g. 2/17 - and 
    # is_date_header will use that to find them.  Once we find one, we'll call 
    # read_shifts to read in all the shifts that are under that date header.  
    # We're done once we've done this for all of the date headers in the file.
    # Throw an exception if we didn't find 35 date headers because the file
    # is likely corrupted.
    num_headers = 0
    for row in range(3, s.nrows): # Rows 0-2 are unhelpful headers
        for col in range(s.ncols):
            if is_date_header(s.cell(row, col).value, month):
                read_shifts(row, col, month, year, s, output)
                num_headers += 1
    if num_headers != 35:
        raise BadInputFile("Error in calendar_module/read_calendar - " + \
            "Expected 35 date headers in " + str(filename) + " but found " + \
            str(num_headers))
    
    return output


def is_date_header(cell_value, month):
    split_cell_value = cell_value.split("/")
    # To be a date header, you must pass three tests!  First, there must be
    # two elements...
    if len(split_cell_value) != 2:
        return False
    # Second, the first element must be equal to the month
    if int(split_cell_value[0]) != month:
        return False
    # Third, the second element must be a number
    if split_cell_value[1].isnumeric() == False:
        return False
    # If you pass all these tests, you're a date header!
    return True


def read_shifts(row, col, month, year, s, output):
    # row, col are the location of the date header.  Get the date from that...
    date = int(s.cell(row, col).value.split("/")[1])
    
    # Now move downward from the date header and process each cell (shift).
    # We're at the end if we hit a blank cell, a new date header, or the last
    # row of the sheet
    counter = 1
    while True:
        if s.cell((row + counter), col).value == "": # Blank cell
            break
        if is_date_header((s.cell((row + counter), col)).value, month):
            break
        if (row + counter) == s.nrows - 1: # Last row of sheet
            break
        # If we get here, we found a shift to add to the list
        shift_name = s.cell((row + counter), col).value.split("(")[0].strip()
        shift_date = dt.datetime(year, month, date)
        # The next cell over has the names of the doctors assigned to this
        # shift
        doctors = s.cell((row + counter), (col + 1)).value.split("\n")
        for doctor in doctors:
            shift = shift_module.Shift(shift_name, shift_date, doctor)
            output.add_shift(shift)
        
        counter = counter + 1


def unit_tests():
    print("calendar_module.py supplies functions needed to read Intrigma's")
    print("Calendar Export file into a Schedule object.  When run directly")
    print("(as you are doing now), it runs a series of unit tests.\n")

    try:
        nosuchfile = read_calendar("No such file")
    except FileNotFoundError as e:
        if str(e) == "Error in calendar_module.py/read_calendar - " + \
            "couldn't find file No such file":
            print("1.  Passed File Not Found Testing!")
        else:
            print("1.  !!!FAILED FILE NOT FOUND TESTING!!!")

    try:
        badfirstsheet = read_calendar("Test Files/Bad First Sheet" + \
            " Calendar.xls")
    except BadInputFile as e:
        if str(e) == "Error in calendar_module/read_calendar - couldn't " + \
            "make sense of the first row, fifth column of Test Files/Bad " + \
            "First Sheet Calendar.xls":
            print("2.  Passed Bad Date Header testing!")
        else:
            print("2.  !!!FAILED BAD DATE HEADER TESTING!!!")

    try:
        badheader = read_calendar("Test Files/Bad Date Header" + \
            " Calendar.xls")
    except BadInputFile as e:
        print(e)
        if str(e) == "Error in calendar_module/read_calendar - couldn't " + \
            "make sense of the first row, fifth column of Test Files/Bad " + \
            "First Sheet Calendar.xls":
            print("3.  Passed Bad Month/Year testing!")
        else:
            print("3.  !!!FAILED BAD MONTH/YEAR TESTING!!!")

    July2020 = read_calendar("Test Files/Almost Empty July 2020 Calendar.xls")
    assert July2020.num_of_shifts == 1
    assert July2020.num_of_requests == 0 # Should always be 0; Calendar files
                                        # don't have requests!
    print("NNN.  Passed Almost Empty July 2020 Calendar testing!\n")

if __name__ == "__main__":
    unit_tests()
