"""assignments_module.py - supplies functions for reading Intrigma's
Assignments Export and extracting useful information into a Schedule object.
When reviewing this module, it's good to have an example of Intrigma's
Assignments Export file in front of you or else none of the comments will
make any sense."""

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
# 1.  Detailed tests with test files in a test directory.
# 2.  Figure out how to redirect the xlrd "errors"

# Standard Library Imports
import sys
import datetime as dt

# Third Party Imports
import xlrd

# Local Application Imports
import shift_module
import request_module
import schedule_module
import exceptions

# Functions
def read_assignments(filename):
    """Read all of the assignments from a filename-specified Intrigma
    Assignments .xls file and return them in a Schedule object."""
    try:
        wb = xlrd.open_workbook(filename)
    except FileNotFoundError:
        raise FileNotFoundError("Error in assignments_module.py/" +
            "read_assignments - couldn't find file " + filename)
    try:
        s = wb.sheet_by_index(0) # Just need the first sheet
    
        # The name of the first sheet gives us the month and year of this
        # schedule... but we'll need them as integers (e.g. "March 2020" -->
        # 3 and 2020)
        sheet_name_as_list = s.name.split()
        month_as_text = sheet_name_as_list[0]
        list_of_months = ["January", "February", "March", "April", "May", 
                          "June", "July", "August", "September", "October", 
                          "November", "December"]
        month = list_of_months.index(month_as_text) + 1 # Months start at 1...
        year = int(sheet_name_as_list[1])
    except:
        raise BadInputFile("Error in assignments_module.py/read_assignments" +
            " - couldn't make sense of the name of the first sheet of " +
            filename)
        
    # In the first column, somewhere near the bottom of the sheet, is the
    # word "Users".  We need to find it because all of the users lie between
    # this row and the last row; we'll save both of these rows as variables
    # for later.
    start_row = 0
    end_row = 0
    for i in range(s.nrows-1, 0, -1):
        if (s.cell(i, 0).value) == 'Users':
            start_row = i
            end_row = s.nrows
            break
        if i == 0: # Finished searching without ever finding "Users"
            raise BadInputFile("Error in assignments_module/" +
                "read_assignments!  Never found 'Users' in file " + filename)

    # In the first row, there will be a cell that has the number "1" in it.
    # That's the first day of the month so we need that.  There will also be a
    # cell that precedes the last cell of the row; that will be the last day
    # of the month so we'll need that too.
    start_col = 0
    end_col = 0
    for i in range(s.ncols-1):
        split_text = s.cell(0, i).value.split()
        if len(split_text) > 1: # Need because 1st cell has just 1 word in it
                                # while all the other cells have 2
            if split_text[1] == "1":
                start_col = i
                end_col = s.ncols-1
                break
            if i == s.ncols-1:
                raise BadInputFile("Error in assignments_module/" +
                    "read_assignments!  Never found first day of month in " +
                    "file " + filename)

    # Now ready to iterate through the spreadsheet and get all the requests and
    # shifts.  The first doc is found 6 rows below "Users".
    output = schedule_module.Schedule()
    for row in range(start_row+6, end_row):
        doctor = s.cell(row, 0).value # The 1st cell of the row has doc's name
        for col in range(start_col, end_col):
            daydate = s.cell(0, col).value # String with day/date e.g. "Tu\n2"
            date_of_month = daydate.split()[1] # Now just the date - e.g. "2"
            date = dt.datetime(year, month, int(date_of_month))
            assignments = s.cell(row, col).value.split("/") # There can be
                # more than one assignment in a day
            # Now read through all the assignments, decide if they're requests
            # or shifts, and add them to the Schedule object
            for assignment in assignments:
                if assignment == "":
                    continue
                elif shift_module.is_a_shift(assignment) == True:
                    shift = shift_module.Shift(assignment, date, doctor)
                    output.add_shift(shift)
                elif request_module.is_a_request(assignment) == True:
                    request = request_module.Request(assignment, date, doctor)
                    output.add_request(request)
                else:
                    raise BadInputFile("Error in assignments_module/" +
                        "read_assignments!  Could not understand assignment " +
                        assignment + " in filename " + filename + 
                        "at row/col " + str(row) + "/" + str(col))
    return output


def unit_tests():
    print("assignments_module.py supplies functions needed to read Intrigma's")
    print("Assignments Export file into a Schedule object.  When run directly")
    print("(as you are doing now), it runs a series of unit tests.\n")

    July2020 = read_assignments("Test Files/Almost Empty July 2020" +
        " Assignments.xls")
    assert July2020.num_of_shifts() == 1
    assert July2020.num_of_requests() == 9
    print("1.  Passed Almost Empty July 2020 Assignments testing!\n")


if __name__ == "__main__":
    unit_tests()
