# install uniRW by running: pip install uniRW
# simple data processing for one file
# run this file: python example1.py

import uniRW as RW

# Suppose we want to read the grade file example1.csv and only record
# the highest grade for each student.
def read_grade():
    grade_dict,_ = RW.read(file_name= './data/example1.csv',
                           mode= 'r',
                           key_col= 0,
                           val_cols= [1],
                           has_header= True,
                           ignore_chars= ['#'],
                           split_re= ',',
                           map_fs= {1: lambda dummy,x: float(x)},
                           reduce_fs= {1: max})

    return grade_dict

# Suppose we want to create a file to sort the students by their grades.
def sort_grade():
    grade_dict = read_grade()

    RW.write(file_name= './data/sorted_example1.csv',
             mode= 'w',
             key_val_dict= grade_dict,
             split_char= ',',
             header= ['Name','Grade'],
             col_names= ['key', 'Grade'],
             sort_by= 'Grade')

# Suppose we want to create a file with each student's grade, rank and percentile.
def percentile_grade():
    sort_grade()

    def update(state, dummy):
        state['rank'] += 1

    grade_dict, state = RW.read(file_name= './data/sorted_example1.csv',
                                mode= 'r',
                                key_col= 0,
                                val_cols= ['rank',1],
                                has_header= True,
                                split_re= ',',
                                state= {'rank': 0},
                                update_state= update)

    total = state.get('rank')

    def add_per_and_rev_rank(dict):
        rank = dict['rank']
        dict['rank'] = total-rank+1
        dict['percentile'] = round(float(rank-1)/float(total)*100, 2)
        return dict

    percentile_dict = {k: add_per_and_rev_rank(v_dict) for k, v_dict in grade_dict.items()}

    RW.write(file_name='./data/percentile_example1.csv',
             mode='w',
             key_val_dict=percentile_dict,
             split_char=',',
             header=['Name', 'Rank', 'Grade', 'Percentile'],
             col_names=['key', 'rank', 'Grade', 'percentile'],
             sort_by='percentile')

percentile_grade()