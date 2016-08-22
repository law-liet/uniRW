# Version Number Spec
vX.Y.Z

- X: Big changes. (API-breaking)
- Y: Add more features. (API-non-breaking)
- Z: Debug or minor fix. (API-non-breaking)

Do not record debug and minor fixes currently.

## v0.5.0:
A clean version passing all tests.

New features:

- Generalize hierarchy from reader and writer
- Dictionary-like access for state and line

## v0.4.0:
New features:

- Key abstraction not needed anymore
- Read and write data file in customized hierarchy

## v0.3.0
New features: 

- Object-oriented abstraction of key, value, line, file, reader and writer

## v0.2.0
New features: 

- Filter lines of a file
- Split by regular expression
- Read with evolving states (monadic?) 
- Sort by key or value
- Customize to_string methods
    
## v0.1.0
Features:

- Select key and values to read
- Read multiple files
- Simple map and reduce (by key) in one file or across multiple files
- Select key and values to write