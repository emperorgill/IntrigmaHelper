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
(These are the modules that do actual data processing/work.  Ideally they don't
have to be changed unless the nature of the data processing/work changes.)

User Level:
cli.py
(These are the modules that interact with the user.  They'll have to be
replaced if ever you decide to move from a command line interface to a GUI).

In addition, there are actual sub-directories...
Config Files - contains user-editable text files that configure the program.
Test Files - contains files used in unit testing the various modules.