# uniRW
A universal reader and writer package for stateful data file processing with basic map/filter/reduce functionality.

## Current Features:
- Reading:
    - Select key and values to read
    - Read multiple files
    - Simple map and reduce (by key) in one file or across multiple files
    - Split by regular expression
    - Read with evolving states (monadic?)
    
- Writing:
    - Select key and values to write
    - Sort by key or value
    - Customize to_string methods
    
## To-do List:
- Robust Error Message
- Examples
- Break down to unit tests
- Customize comparation function for sorting
- Add type checker (Python 3.5 typing module + Mypy ?)

## Future Work:
- Better Abstraction/Structure (OO style?)
- Optimization