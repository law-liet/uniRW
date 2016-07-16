# install uniRW by running: pip install uniRW
# simple data processing for one file
# run this file: python example1.py

import uniRW as RW

# Suppose we want to read the grade file example1.csv and only record
# the highest grade for each student.

# example1.csv format:
#
#       # xxxxxx
#       Name,Grade
#       Student1,Grade1
#       Student2,Grade2
#       ...
#       StudentN,GradeN
#

Name  = RW.Key(name= 'Name')
Grade = RW.Value(name= 'Grade', map_f= RW.pureR(float), reduce_f= max)
Line  = RW.Line(split_by= ',')

def read_grade(file_name):

    def skip_first_line(line):
        return line.get_by_index(0)[0] == '#'

    GradeFile     = RW.DataFile(file_name= file_name, line= Line, header_lineno= 1)
    GradeReader   = RW.Reader(Key= Name, Values= [Grade], filter_f= RW.pureR(skip_first_line))
    grade_dict, _ = GradeReader.read(data_file= GradeFile)
    return grade_dict

def sort_grade(file_name):
    grade_dict = read_grade(file_name)

    OutputLine = RW.OuputLine(split_char= ',')
    OutputFile = RW.OutputFile(
        file_name= '.'.join(file_name.split('.')[:-1]) + '_sorted.csv',
        line= OutputLine,
        header= ['Name','Grade']
    )
    
    GradeWriter = RW.Writer(KeyValues= [Name,Grade])
    GradeWriter.write(out_file= OutputFile, key_val_dict= grade_dict, sort_by='Grade')

def percentile_grade():
    pass

if __name__ == '__main__':
    sort_grade('./data/example1.csv')