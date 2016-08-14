# uniRW
An expressive universal reader & writer package for stateful data file processing.

## Installation
```
pip install uniRW
```

## Quick Start
First, import the package:
```Python
>>> import uniRW as RW
```

Suppose we want read a file named *example.csv* that looks like this:

    Name,Grade
    Alice,4.0
    Bob,3.0

Define the value structures and hierarchy:

``` python
>>> name = RW.Value(name= 'Name')
>>> grade = RW.Value(name= 'Grade', map_f= RW.pureR(float))
>>> hierarchy = { name : [ grade ] }
```

Define the input file:

```python
>>> line = RW.Line(delimiter= ',')
>>> grade_file = RW.DataFile(file_name= 'example1.csv', line= line, header_lineno= 0)
```

Create the reader and read the file:

```python
>>> grade_reader = RW.HReader(hierarchy_spec= hierarchy)
>>> grade_dict, _ = grade_reader.read(data_file= grade_file)
>>> print(grade_dict)
{'Alice': 4.0, 'Bob': 3.0}
```

Suppose we want to write `grade_dict` to a new file *new_example.csv* that looks like this:

    Name    Grade
    Bob     3.0
    Alice   4.0

Define the value line:

```python
>>> value_line= [name,grade]
```

Define the output file:

```python
>>> outputLine = RW.OutputLine(delimiter= '\t')
>>> outputFile = RW.OutputFile(file_name= 'new_example.csv', line= outputLine)
```

Create the writer and write the file:

```python
>>> grade_writer = RW.HWriter(hierarchy_spec= hierarchy, value_line= value_line)
>>> grade_writer.write(out_file= outputFile, value_hierarchy= grade_dict, sort_by= 'grade')
```

## Examples
See [examples](https://github.com/law-liet/uniRW/tree/master/examples) for more examples.

## Documentation
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
- Combine states in reading multiple files

## Future Work
- Better abstraction/structure
- Generalize hierarchy
- Optimization
- Add type checker (Python 3.5 typing module + Mypy ?)

