# uniRW
A universal reader & writer package for stateful data file processing with basic map & reduce functionality.

## Current Features:
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
    
## To-do List:
- Robust Error Messages
- Documentation
- Examples
- Break down to unit tests
- Customize comparation function for sorting
- Combine states in reading multiple files

## Future Work:
- Better abstraction/structure
- Hierarchical Processing
- Optimization
- Add type checker (Python 3.5 typing module + Mypy ?)

