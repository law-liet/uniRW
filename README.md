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
```python
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
``` python
>>> name = RW.Key(name= 'Name')
>>> grade = RW.Value(name= 'Grade', map_f= RW.pureR(float))
>>> gradeReader = RW.Reader(Key= name, Values= [grade])
>>> line = RW.Line(delimiter= ',')
>>> grade_file = RW.DataFile(file_name= 'example1.csv', line= line, header_lineno= 0)
>>> grade_dict, _ = gradeReader.read(data_file= grade_file)
>>> print(grade_dict)
{'Alice': 4.0, 'Bob': 3.0}
```

##### Method 3:
`grade_file` is the same as defined at method 2 above.
``` python
>>> name = RW.Value(name= 'Name')
>>> grade = RW.Value(name= 'Grade', map_f= RW.pureR(float))
>>> gradeHReader = RW.HReader(hierarchy_spec= { name: [grade] })
>>> grade_dict, _ = gradeHReader.read(data_file= grade_file)
>>> print(grade_dict)
{'Alice': 4.0, 'Bob': 3.0}
```

Suppose we want to write `grade_dict` to a new file.

##### Method 1:
```python
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

```python
>>> outputLine = RW.OutputLine(delimiter= ',')
>>> outputFile = RW.OutputFile(
...     file_name= 'new_example.csv',
...     line= outputLine,
...     header= ['Name','Grade']
... )
>>> gradeWriter = RW.Writer(KeyValues= [name,grade])
>>> gradeWriter.write(out_file= outputFile, key_val_dict= grade_dict, sort_by= 'Grade')
```

##### Method 3: 
`name`, `grade` and `outputFile` are the same as defined at method 2 above.

```python
>>> gradeHWriter = RW.HWriter(hierarchy_spec={ name: [grade] }, value_line= [name,grade])
>>> gradeHWriter.write(out_file= outputFile, value_hierarchy= grade_dict, sort_by= 'Grade')
```

All methods will create a new file named `new_example.csv` that looks like this:
    
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
- Carry state across files
- Simple map and reduce (by key) in one file or across multiple files
- Read with evolving state (monadic?)
- Read data file in customized hierarchy
    
Write:

- Select key and values to write
- Sort by key or value
- Customize to_string methods
- Write data file in customized hierarchy
    
## To-do List
- Robust Error Messages
- Documentation
- Examples
- Break down to unit tests
- Customize comparation function for sorting
- Combine states in reading multiple files

## Future Work
- Better abstraction/structure
- Optimization
- Add type checker (Python 3.5 typing module + Mypy ?)

