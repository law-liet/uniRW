# uniRW
A universal reader & writer package for stateful data file processing with basic map & reduce functionality.

## Installation
```
pip install uniRW
```

## Quick Start
First, import the package.
```Python
>>> import uniRW as RW
```

Suppose we want read a file named *example.csv* that looks like this:

    Name,Grade
    Alice,4.0
    Bob,3.0

##### Method 1:
```Python
>>> grade_dict, _ = RW.read(
...     file_name= 'example.csv',
...     mode= 'r',
...     key_col= 0,
...     val_cols= [1],
...     has_header= True,
...     map_fs= {1: RW.pureR(float)}
...     split_by= ','
... )
>>> print(grade_dict)
{'Alice': 4.0, 'Bob': 3.0}
```

##### Method 2:
``` Python
>>> name = RW.Key(name= 'Name')
>>> grade = RW.Value(name= 'Grade', map_f= RW.pureR(float))
>>> gradeReader = RW.Reader(Key= 'Name', Values= [Grade])
>>> line = RW.Line(delimiter= ',')
>>> grade_file = RW.DataFile(file_name= 'example1.csv', line= line, header_lineno= 0)
>>> grade_dict, _ = gradeReader.read(data_file= grade_file)
>>> print(grade_dict)
{'Alice': 4.0, 'Bob': 3.0}
```

Suppose we want to write `grade_dict` to a new file.

##### Method 1:
```Python
>>> RW.write(
...     file_name= 'new_example.csv',
...     mode= 'w',
...     key_val_dict= grade_dict,
...     split_char= ',',
...     header= ['Name','Grade']
...     col_names= ['key','Grade'],
...     sort_by= 'Grade'
... )
```

##### Method 2: 
`name` and `grade` are the same as defined at method 2 above.

```Python
>>> outputLine = RW.OutputLine(delimiter= ',')
>>> outputFile = RW.OutputFile(
...     file_name= 'new_example.csv',
...     line= outputLine,
...     header= ['Name','Grade']
... )
>>> gradeWriter = RW.Writer(KeyValues= [name,grade])
>>> gradeWriter.write(out_file= outputFile, key_val_dict= grade_dict, sort_by= 'Grade')
```
Both methods will create a new file named `new_example.csv` that looks like this:
    
    Name,Grade
    Bob,3.0
    Alice,4.0
    
See [examples](https://github.com/law-liet/uniRW/tree/master/examples) for more examples.
See [wiki](https://github.com/law-liet/uniRW/wiki) for documentation.

## Current Features
Read:

- Select key and values to read
- Filter lines of a file
- Split by regular expression
- Read multiple files
- Simple map and reduce (by key) in one file or across multiple files
- Read with evolving state (monadic?)
    
Write:

- Select key and values to write
- Sort by key or value
- Customize to_string methods
    
## To-do List
- Robust Error Messages
- Documentation
- Examples
- Break down to unit tests
- Customize comparation function for sorting
- Combine states in reading multiple files

## Future Work
- Better abstraction/structure
- Hierarchical Processing
- Optimization
- Add type checker (Python 3.5 typing module + Mypy ?)

