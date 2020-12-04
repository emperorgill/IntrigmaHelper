# units_scheduled.py - supples the units_scheduled function and associated
# helper functions.

# TO-DO
# 1.  Unit tests.
# 2.  Write to output in varying formats as needed.
# 3.  Make calendar input work so that we can do calcs on months that
# aren't fully scheduled yet.

# Standard Library Imports
import datetime as dt
import pprint  # For printing dictionaries nicely in unit_tests()

# Local Application Imports
import shift_module
import request_module
import schedule_module
import calendar_module
import assignments_module


def units_scheduled(filename):
    """Receives a Schedule object and returns a text table describing how
    many units were worked each date in the various areas the ED must staff.
    Ignores any shift whose "doctor" has a name that starts with three
    asterisks as these are placeholders for shifts that were not worked e.g.
    ***CANCELLED*** ***VOLUNTEER*** and the like.  The only exception is
    ***ORPHAN*** which probably WAS worked but the call doctor didn't put
    his name in the correct slot."""
    # schedule = calendar_module.read_calendar(filename)
    schedule = assignments_module.read_assignments(filename)
    if schedule.is_empty is True:
        return (str(filename) + " contains an empty schedule!\n")

    # Our data structure will be a dictionary of dictionaries.  The outer-
    # most dictionary will have one key for each date in the period we're
    # looking at.  The value of each of these keys will be another
    # dictionary.
    # This innermost dictionary will have keys corresponding to the various
    # areas that the ED must staff - e.g. "ROS ED" "EPRP" etc.  The value
    # of each key will be a number corresponding to how many units were
    # scheduled in that area on that date.

    # Construct the data structure
    data = {}
    date = schedule.first_date()
    last_date = schedule.last_date()
    while date <= last_date:
        data[date] = {"SAC ED": 0, "SAC PIT": 0, "ROS ED": 0, "ROS PIT": 0,
            "CDA": 0, "EPRP": 0, "AACC": 0, "Regional Lab": 0, "Call": 0,
            "South Sac": 0, "AFM FU": 0, "BAM": 0}
        date += dt.timedelta(days=1)

    # Now run through all the shifts in schedule and add their units paid
    # to the appropriate section of data.  Remember that hours_paid is a
    # timedelta object in the Shift class and that 4 hours is 1 unit.  Skip
    # any shift with a doctor whose name starts with *** or for whom doctor is
    # None.
    for shift in schedule.shifts:
        if shift.doctor is None:
            continue
        if shift.doctor[0:3] == "***" and shift.doctor != "***ORPHAN***":
            continue
        date = shift.start_time.date()
        if shift.location == "Sacramento" and shift.is_PIT is False:
            data[date]["SAC ED"] += shift.hours_paid.seconds/(3600*4)
        elif shift.location == "Sacramento" and shift.is_PIT is True:
            data[date]["SAC PIT"] += shift.hours_paid.seconds/(3600*4)
        elif shift.location == "Roseville" and shift.is_PIT is False:
            data[date]["ROS ED"] += shift.hours_paid.seconds/(3600*4)
        elif shift.location == "Roseville" and shift.is_PIT is True:
            data[date]["ROS PIT"] += shift.hours_paid.seconds/(3600*4)
        elif shift.location == "Other":
            pass
        else:  # Handles AACC, EPRP, Regional Lab, CDA, Call, BAM
            data[date][shift.location] += shift.hours_paid.seconds/(3600*4)

    return data


# Unit test script/basic use case for the units_scheduled.py module
def unit_tests(filename = "December 2020.xls"):
    if filename == "":  # Run unit tests
        data = units_scheduled("Test Files/Test Units Scheduled Assignments.xls")
        assert data[dt.date(2020, 7, 6)]["SAC ED"] == 4
        assert data[dt.date(2020, 7, 7)]["SAC PIT"] == 4.75
        assert data[dt.date(2020, 7, 8)]["ROS ED"] == 5
        assert data[dt.date(2020, 7, 9)]["ROS PIT"] == 3.75
        assert data[dt.date(2020, 7, 10)]["AACC"] == 4
        assert data[dt.date(2020, 7, 11)]["Regional Lab"] == 3.75
        assert data[dt.date(2020, 7, 12)]["EPRP"] == 7.5
        assert data[dt.date(2020, 7, 13)]["CDA"] == 4
        assert data[dt.date(2020, 7, 14)]["Call"] == 0
        assert data[dt.date(2020, 7, 15)]["South Sac"] == 5.5
        assert data[dt.date(2020, 7, 16)]["SAC ED"] == 4
        assert data[dt.date(2020, 7, 17)]["ROS ED"] == 5.5
        assert data[dt.date(2020, 7, 18)]["AACC"] == 3
        assert data[dt.date(2020, 7, 19)]["Call"] == 0
        print("units_scheduled.py passed unit testing!")
    else:  # Run this basic version that we currently have urgent need for
        data = units_scheduled(filename)
        list_dates = data.keys()
        SACEDUnits = 0
        SACPITUnits = 0
        ROSEDUnits = 0
        ROSPITUnits = 0
        CDAUnits = 0
        EPRPUnits = 0
        AACCUnits = 0
        RLSUnits = 0
        AFMFUunits = 0
        BAMUnits = 0
        for date in list_dates:
            SAC_capacity = data[date]["SAC ED"]*5.7 + data[date]["SAC PIT"]*9.3
            ROS_capacity = data[date]["ROS ED"]*5.7 + data[date]["ROS PIT"]*9.3
            SACEDUnits += data[date]["SAC ED"]
            SACPITUnits += data[date]["SAC PIT"]
            ROSEDUnits += data[date]["ROS ED"]
            ROSPITUnits += data[date]["ROS PIT"]
            CDAUnits += data[date]["CDA"]
            EPRPUnits += data[date]["EPRP"]
            AACCUnits += data[date]["AACC"]
            RLSUnits += data[date]["Regional Lab"]
            AFMFUunits += data[date]["AFM FU"]
            BAMUnits += data[date]["BAM"]
            print(str(data[date]["ROS ED"] + data[date]["ROS PIT"]))
            #print(str(ROS_capacity))
        print("SAC ED Units = " + str(SACEDUnits))
        print("SAC PIT Units = " + str(SACPITUnits))
        print("ROS ED Units = " + str(ROSEDUnits))
        print("ROS PIT Units = " + str(ROSPITUnits))
        print("CDA Units = " + str(CDAUnits))
        print("EPRP Units = " + str(EPRPUnits))
        print("AACC Units = " + str(AACCUnits))
        print("RLS Units = " + str(RLSUnits))
        print("AFM FU Units = " + str(AFMFUunits))
        print("BAM Units = " + str(BAMUnits))


if __name__ == "__main__":
    unit_tests()
