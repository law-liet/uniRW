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
# Suppose we have a varied number of exams and grades of a varied number of students for a varied number of courses,
# which are recorded in a varied number of files named example2*.csv
# We want to compute the average grade of each course for each student.
#


def average(num_list):
    return round(sum(num_list) / len(num_list), 2)

name = RW.Value('Name')
course = RW.Value('Course')
grade = RW.Value(  # record a list of grades
    name='Grade',
    map_f=RW.pureR(lambda x: [float(x)]),  # convert a grade to a list
    reduce_f=add,  # append the lists
    post_map_f=RW.pureR(average)  # compute the average of the list of grades after reading all data
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
    comma_line = RW.Line(',')

    def grade_file(file_name):
        return RW.DataFile(file_name, comma_line, header_lineno=0)

    grade_files = map(grade_file, file_names)  # create the list of DataFile objects we want.
    grade_dict = RW.HReader(grade_book).read_all(grade_files)
    return grade_dict


def write_grade(file_name, grade_dict):
    output_file = RW.OutputFile(
        file_name,
        RW.OutputLine(','),
        foreword=['# Average Grade of Exams for Each Subject']
    )
    RW.HWriter(grade_book, [name, course, grade]).write(output_file, grade_dict)


if __name__ == "__main__":
    raw_grade_files = glob("data/example2*.csv")
    print("Input files: " + ' & '.join(raw_grade_files))
    write_grade("data/average_example2.csv", read_grade(raw_grade_files))
    print('Done. Take a look at data/average_example.csv')
