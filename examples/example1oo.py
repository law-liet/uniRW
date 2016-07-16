# install uniRW by running: pip install uniRW
# simple data processing for one file
# run this file: python example1.py

import uniRW as RW

data_dir = './data/'

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
Line  = RW.Line(delimiter= ',')
OutputLine = RW.OuputLine(delimiter= ',')

def read_grade(file_name):

    def skip_first_line(line):
        return not line.get_by_index(0)[0] == '#'

    GradeFile     = RW.DataFile(file_name= file_name, line= Line, header_lineno= 1)
    GradeReader   = RW.Reader(Key= Name, Values= [Grade], filter_f= RW.pureR(skip_first_line))
    grade_dict, _ = GradeReader.read(data_file= GradeFile)
    return grade_dict

def sort_grade(file_name):
    grade_dict = read_grade(file_name)

    OutputFile = RW.OutputFile(
        file_name= '.'.join(file_name.split('.')[:-1]) + '_sorted.csv',
        line= OutputLine,
        header= ['Name','Grade']
    )
    GradeWriter = RW.Writer(KeyValues= [Name,Grade])
    GradeWriter.write(out_file= OutputFile, key_val_dict= grade_dict, sort_by= 'Grade', reverse= True)

def percentile_grade(file_name):
    sort_grade(file_name)
    file_prefix = '.'.join(file_name.split('.')[:-1])

    def update(state):
        state.set('rank', state.get('rank') + 1)
        
    state = RW.State(init_state= {'rank': 0}, update_func= RW.pureL(update))

    def get_percentile(state, rank):
        total = state.get('rank')
        reverse_rank = total-rank+1
        percentile = round(float(reverse_rank-1)/float(total)*100, 2)
        return rank, percentile

    def print_tuple(val):
        a,b = val
        return str(a) + ',' + str(b)

    Rank        = RW.StateValue(name= 'rank', post_map_f= get_percentile, to_string= print_tuple)
    GradeReader = RW.Reader(Key= Name, Values= [Rank,Grade], State= state)
    GradeFile   = RW.DataFile(
        file_name= file_prefix + '_sorted.csv',
        line= Line,
        header_lineno= 0
    )
    grade_dict, _ = GradeReader.read(data_file= GradeFile, apply_post_map= True)

    OutputFile = RW.OutputFile(
        file_name= file_prefix + '_percentile.csv',
        line= OutputLine,
        header= ['Name','Grade','Rank','Percentile']
    )
    GradeWriter = RW.Writer(KeyValues= [Name,Grade,Rank])
    GradeWriter.write(out_file= OutputFile, key_val_dict= grade_dict, sort_by= 'Grade', reverse= True)



if __name__ == '__main__':
    percentile_grade(data_dir + 'example1.csv')