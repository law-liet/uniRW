### v0.2.0
New features: 

- Filter lines of a file
- Split by regular expression
- Read with evolving states (monadic?) 
- Sort by key or value
- Customize to_string methods
 
API Changes:

- switch order of arguments of functions in post_map_fs:
    - Before: f(val, lineno)
    - Now: f(lineno, val)
    
### v0.1.0
Features:

- Select key and values to read
- Read multiple files
- Simple map and reduce (by key) in one file or across multiple files
- Select key and values to write