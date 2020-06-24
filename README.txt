IntrigmaHelper program - provides additional functionality to help schedulers
work with the Intrigma scheduling program.

Conceptually there are three levels to the program...

Input Level:
assignments_module.py
calendar_module.py
(These read data in from XLS files exported from Intrigma.  They can be
replaced with other modules if the decision is made, later on, to obtain data
from Intrigma a different way, e.g. via its API).

Middle Level:
credit_lookup.py
request_module.py
scehdule_module.py
shift_module.py
exceptions.py
AACC_dates.py
units_scheduled.py
(These are the modules that do actual data processing/work.  Ideally they don't
have to be changed unless the nature of the data processing/work changes.)

User Level:
cli.py
(These are the modules that interact with the user.  They'll have to be
replaced if ever you decide to move from a command line interface to a GUI).

In addition, there are actual sub-directories...
Config Files - contains user-editable text files that configure the program.
Test Files - contains files used in unit testing the various modules.
Real Data - contains exported files from some months that have been previously
worked (ie, they're not going to be changed by any further trades)

Finally, here is a list of evil things that tripped us up when writing this
program...
1.  In Excel if you type ... (as in a shift name 8rp...), Excel will 
Auto-correct this from three periods to a single ellipse character.  It 
displays the same in Excel but not in Python.  When you try to compare
8rp...(ellipse) from Excel to 8rp...(three periods) in Python, it won't
work!  You have to go to File-->Options-->AutoCorrect in Excel to delete
this AutoCorrect entry.