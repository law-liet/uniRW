# simple data processing for one file
# install uniRW by running: pip install uniRW
# cd into examples/ directory, run: python example1.py

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

#
# Suppose we want to read the grade file example1.csv and only record
# the highest grade for each student.
# Idea:
#   Expected output: { Name : { Grade: Grade value } }
#   Key: Name - column 0
#   Value: Grade - column 1
#   Ignore: line start with #
#   has header (column label): Name, Grade
#   Split: ','
#   Map: Grade - to float type
#   Reduce: Grade - keep the maximum
#
def read_grade():
    grade_dict,_ = RW.read(
        file_name= './data/example1.csv',
        mode= 'r',
        key_col= 0,
        val_cols= [1],
        has_header= True,
        ignore_chars= ['#'],
        split_re= ',',
        map_fs= {1: lambda dummy,x: float(x)},
        reduce_fs= {1: max}
    )

    return grade_dict

#
# Suppose we want to create a file to sort the students by their grades.
# Idea:
#   Expected input: { Name : { Grade: value } }
#   Output format:
#
#         Name,Grade
#         Student1,Grade1
#         Student2,Grade2
#         ...
#         StudentN,GradeN
#
#   Split: ','
#   Header (Column Label): Name, Grade
#   Column: Name (key), Grade
#   Sort By: Grade
#
def sort_grade():
    grade_dict = read_grade()

    RW.write(
        file_name= './data/sorted_example1.csv',
        mode= 'w',
        key_val_dict= grade_dict,
        split_char= ',',
        header= ['Name','Grade'],
        col_names= ['key', 'Grade'],
        sort_by= 'Grade'
    )

#
# Suppose we want to create a file with each student's grade, rank and percentile.
# Idea:
#   Input: sorted by grade
#   To calculate percentile, need to know: rank - line number
#                                          total number of students - number of lines
#
#   Expected output: { Name : { Grade: value, Rank: value, Percentile: value } }
#
#   Key: Name - column 0
#   Value: Grade - column 1, Rank - line number (state)
#   Split: ','
#   has header: Name, Grade
#   state: rank (line number) - init val: 0
#   update state: increment 'rank' (line number) after reading each line
#
#   total number is the 'rank' in final state
#
#   Output format:
#
#         Name,Grade,Rank,Percentile
#         Student1,Grade1,Rank1,Percentile1
#         Student2,Grade2,Rank2,Percentile2
#         ...
#         StudentN,GradeN,RankN,PercentileN
#
def percentile_grade():
    sort_grade()

    def update(state, dummy):
        state['rank'] += 1

    grade_dict, state = RW.read(
        file_name= './data/sorted_example1.csv',
        mode= 'r',
        key_col= 0,
        val_cols= ['rank',1],
        has_header= True,
        split_re= ',',
        state= {'rank': 0},
        update_state= update
    )

    total = state.get('rank')

    def add_per_and_rev_rank(dict):
        rank = dict['rank']
        dict['rank'] = total-rank+1
        dict['percentile'] = round(float(rank-1)/float(total)*100, 2)
        return dict

    percentile_dict = {k: add_per_and_rev_rank(v_dict) for k, v_dict in grade_dict.items()}

    RW.write(
        file_name= './data/percentile_example1.csv',
        mode= 'w',
        key_val_dict= percentile_dict,
        split_char= ',',
        header= ['Name', 'Rank', 'Grade', 'Percentile'],
        col_names= ['key', 'rank', 'Grade', 'percentile'],
        sort_by= 'percentile'
    )



if __name__ == '__main__':
    percentile_grade()