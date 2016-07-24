# install uniRW by running: pip install uniRW
# simple data processing for one file
# run this file: python example1H.py

import uniRW as RW

# This example is a rewrite of example1oo.py using the more general hierarchical approach.

# example1.csv format:
#
#       # xxxxxx
#       Name,Grade
#       Student1,Grade1
#       Student2,Grade2
#       ...
#       StudentN,GradeN
#

Name  = RW.Value(name= 'Name')
Grade = RW.Value(name= 'Grade', map_f= RW.pureR(float), reduce_f= max)
Line  = RW.Line(delimiter= ',')
OutputLine = RW.OuputLine(delimiter= ',')

def read_grade(file_name):
    pass

def sort_grade(file_name):
    pass

def percentile_grade(file_name):
    pass