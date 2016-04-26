# Natural Number Calculation Engine (NNCE)

NNCE is a tape-based esoteric programming language. It has two data types, natural numbers and commands.

## Concepts

### Tapes
The natural-number calculation engine can be modeled as a machine with three tapes. Each tape has a *tape head*, which specifies the location of execution, input, or output

The *Program Tape* stores all commands and all data that the program is operating on. The program tape consists of a series of cells, each of which can store a command or a natural number. All of the commands defined by NNCE read and/or write information from/to the program tape.  The *Tape Head* tracks the program's current location on the program tape. Excluding commands that specify otherwise, the tape head moves forward to the next cell after executing the command in the previous cell. When the tape head encounter a number in a cell rather than a command, it will do nothing and move on to the next cell.

The *Input Tape* is used to provide external data to a program. The INPT command will read the next character on the input tape, write it to the program tape, and move the *Input Tape head* forward. The input tape is read-once: the input tape head cannot move backwards.

The *Output Tape* is used to write data to an external source to show the results of an NNCE computation. The OUTP command writes data from the program tape to the location of the *Output Tape Head*, and move the output tape head forward. The output tape is write-once: the output tape head cannot move backwards.

An NNCE program consists of a series of commands and numbers, separated by line breaks, which initialize the state of the program tape. Tape cells that have not been set are considered to be 0.

### Exception Handling

## File Conventions

NNCE programs should be named *.nn

## Syntax

Multiple new lines in a row are ignored by the interpreter.

## Commands

### INCR
Increment the number stored in the next cell by 1.

Undefined behavior results if the INCR command is executed when another command rather than a number is stored in the cell after it.
### DECR
Decrement the number stored in the next cell by 1.

Undefined behavior results if the DECR command is executed when another command rather than a number is stored in the cell after it.

It is an error to attempt to decrement 0. The natural number calculation engine can only handle natural numbers. If you attempt to decrement 0, the tape head will move to the error-handling address (defined below.)

### GOTO
Read the number stored in the cell after the GOTO command, and move the tape head to that address.

Undefined behavior results if the GOTO command is executed when another command is stored in the cell after it.

### COPY
Read the numbers stored in the two cells after the COPY command. These numbers are treated as cell addresses. The value (a number or a command) stored in the first addressed cell is copied into the second addressed cell. Then the tape head continues to execute from the cell after the copy command.

Undefined behavior results if the COPY command is executed when either of the two cells after it is another command rather than a number.

### Numbers
Numbers aren't commands. When the tape head sees a number, it will simply move past it to the next line.

## I/O Commands
The natural number calculation engine has some basic character-based I/O facilities.
### INPT
Read the next character from the input tape, and write a numeric value which corresponds to it to the next line on the program tape.

The mapping of numbers to characters is implementation-defined, but must match that of the OUTP command.

It is an error to attempt to read if the input tape has been exhausted. If the INPT command is executed when the input tape is exhausted, the tape head will move to the error-handling address (defined below.) 
### OUTP
The OUTP command examines the next cell on the program tape. If it is a number in the valid output range, it writes a character corresponding to that number to the output tape.

The mapping of numbers to characters is implementation-defined, but must match that of the INPT command.

It is undefined behavior to execute the OUTP command when it is followed by another command rather than number.
It is undefined behavior to attempt to output a number outside of the valid output range.

### OUTPD
The behavior of the OUTPD command is implementation-defined. Its inteded use is for debugging NNCE programs.

## Additional features

### Labels

### Error-Handling Address

### Valid Output Ranges

# NNCE Interpreter

## Using the interpreter
## Implementation Details
### Valid Ouput ranges
### Outpd behavior

## Known Issues

### Copy Bug
# Natural Number++ (NN++)

NN++ is a set of extensions for NNCE that make writing NNCE programs easier

## Named labels
## Comments
## Control loops
