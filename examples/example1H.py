# install uniRW by running: pip install uniRW
# simple data processing for one file
# run this file: python example1H.py

import uniRW as RW

# example1.csv format:
#
#       # xxxxxx
#       Name,Grade
#       Student1,Grade1
#       Student2,Grade2
#       ...
#       StudentN,GradeN
#

# Common Structure of Both Input and Output:
#
#   Value: Student Name
#   Value: Grade
#       - map: convert to float
#       - reduce: only keep the maximum for one student
#   File:
#       - line:
#          - name the columns according to header
#               ("Name" for column 0, "Grade" for column 1)
#          - delimiter ','
#   Hierarchy - { name : [grade] }
#   (Note that we no longer need Key here, since the key-value relation can be defined by a hierarchy_spec of values)
#

name  = RW.Value('Name')
grade = RW.Value('Grade', map_f=RW.pureR(float), reduce_f=max)
line  = RW.Line(',')
outputLine = RW.OutputLine(',')
gradeBook = {
    name: [
        grade
    ]
}


#
# Suppose we want to read the grade file example1.csv and only record
# the highest grade for each student.
# Idea:
#   Expected output: { Name : { Grade: Grade value } }
#   Skip first line (start with #)
#   Header is in line 1 (start from 0)
#

def read_grade(file_name):
    def skip_first_line(line):
        return not line.get_by_index(0)[0] == '#'

    gradeFile     = RW.DataFile(file_name, line, header_lineno= 1)
    gradeReader   = RW.HReader(gradeBook, filter_f= RW.pureR(skip_first_line))
    grade_dict, _ = gradeReader.read(gradeFile)
    return grade_dict


#
# Suppose we want to create a file to sort the students by their grades.
# Idea:
#   Expected input: { Name : { Grade: value } }
#   Output format: (Common structure)
#
#         Name,Grade
#         Student1,Grade1
#         Student2,Grade2
#         ...
#         StudentN,GradeN
#
#   Sort by: Grade (Descending)
#
def sort_grade(file_name, grade_dict):
    outputFile = RW.OutputFile(
        '.'.join(file_name.split('.')[:-1]) + '_sorted.csv',
        outputLine
    )
    gradeWriter = RW.HWriter(gradeBook, [name, grade])
    gradeWriter.write(outputFile, grade_dict, sort_by='Grade', reverse=True)


#
# Suppose we want to create a file with each student's grade, rank and percentile.
# Idea:
#   Input: sorted by grade, header is in line 0
#   To calculate percentile, need to know: rank -- line number
#                                          total number of students -- number of lines
#
#   Expected output: { Name : { Grade: value, Rank: value, Percentile: value } }
#
#   state: rank (line number) -- init val: 0
#   update state: increment 'rank' (line number) after reading each line
#
#   total number is the 'rank' in final state
#   We can calculate percentile only after we read all the lines, so apply post map.
#
#   Rank: record the rank value in state
#       - post map: rank -> (rank, percentage)
#       - to_string: (rank, percentage) -> "rank,percentage"
#
#   Output format:
#
#         Name,Grade,Rank,Percentile
#         Student1,Grade1,Rank1,Percentile1
#         Student2,Grade2,Rank2,Percentile2
#         ...
#         StudentN,GradeN,RankN,PercentileN
#
# This method is for illustration purpose. It is not the simplest approach.
#
def percentile_grade(file_name):
    sort_grade(file_name, read_grade(file_name))
    file_prefix = '.'.join(file_name.split('.')[:-1])

    def update(state):
        state.set('rank', state.get('rank') + 1)

    state = RW.State({'rank': 0}, RW.pureL(update))

    def get_percentile(state, rank):  # calculate percentage based on rank
        total = state.get('rank')
        reverse_rank = total - rank + 1
        percentile = round(float(reverse_rank - 1) / float(total) * 100, 2)
        return rank, percentile

    def print_tuple(val):
        a, b = val
        return str(a) + ',' + str(b)

    rank = RW.StateValue('rank', post_map_f=get_percentile, to_string=print_tuple)
    gradeBook2 = {
        name: [
            grade,
            rank
        ]
    }

    gradeFile = RW.DataFile(file_prefix + '_sorted.csv', line, header_lineno=0)
    grade_dict, _ = RW.HReader(gradeBook2, state).read(gradeFile, apply_post_map=True)

    outputFile = RW.OutputFile(
        file_prefix + '_percentile.csv',
        outputLine,
        header=['Name', 'Grade', 'Rank', 'Percentile']
    )

    gradeWriter = RW.HWriter(gradeBook2, [name, grade, rank])
    gradeWriter.write(outputFile, grade_dict, sort_by='Grade', reverse=True)


if __name__ == '__main__':
    percentile_grade('data/'+'example1.csv')
