# install uniRW by running: pip install uniRW
# slightly more complex data processing for multiple files
# run this file: python example2H.py

from glob import glob
from operator import add

import uniRW as RW


# example2*.csv format:
#
#       Name,Course,Exam,Grade
#       Student1,Course1,Exam1,Grade1
#       Student1,Course1,Exam2,Grade2
#       ...
#       Student1,Course1,ExamN,GradeN
#       Student2,Course1,Exam1,Grade1
#       ...
#       StudentM,CourseM,ExamM,GradeM
#

#
# Suppose we a varied number of exams and grades of a varied number of students for varied number of courses,
# which are recorded in a varied number of files named example2*.csv
# We want to compute the average grade of each course for each student.
#

# helper
def average(num_list):
    return round(sum(num_list) / len(num_list), 2)
# end helper

name   = RW.Value(name= 'Name')
course = RW.Value(name= 'Course')
grade  = RW.Value(  # record a list grades
    name      = 'Grade',
    map_f     = RW.pureR(lambda x: [float(x)]),  # convert a grade to a list
    reduce_f  = add,  # append the lists
    post_map_f= RW.pureR(average)  # compute the average of the list of grades after reading all data
)

# We want the mapping (name => (course => grade)), like {'Alice': {'Math': {'grade': 4.0}}}
grade_book = {
    name: {
        course: [
            grade
        ]
    }
}


def read_grade(file_names):
    comma_line = RW.Line(delimiter=',')

    def grade_file(file_name):
        return RW.DataFile(file_name, comma_line, header_lineno= 0)

    grade_files = map(grade_file, file_names)  # create the list of DataFile objects we want.
    grade_reader = RW.HReader(grade_book)
    grade_dict = grade_reader.readAll(grade_files)
    return grade_dict


def write_grade(file_name, grade_dict):
    comma_output_line = RW.OutputLine(delimiter=',')
    output_file = RW.OutputFile(
        file_name,
        comma_output_line,
        foreword= ['# Average Grade of Exams for Each Subject']
    )

    value_line = [name, course, grade]
    grade_writer = RW.HWriter(grade_book, value_line)
    grade_writer.write(output_file, grade_dict)


if __name__ == "__main__":
    raw_grade_files = glob("data/example2*.csv")
    write_grade("data/average_example2.csv", read_grade(raw_grade_files))
