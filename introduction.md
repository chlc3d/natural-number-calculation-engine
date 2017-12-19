# An Introduction to the  Natural Number Calculation Engine
# Written by its creator, Dr. Cornelius Vandergraff

The natural number calculation engine is a powerful tool for performing arithmetic calculations automatically 
## Concepts

### Tapes
The engine must be fed two tapes which provide information on calculations, and has an additional output tape. Each tape has a *tape head*, which specifies the location of execution, input, or output

The *Procedure Tape* stores all commands and all data that the procedure is operating on. The procedure tape consists of a series of cells, each of which can store a command or a natural number. Many of the commands defined by the engine read or write information from or to the procedure tape.  The *Tape Head* tracks the procedure's current location on the procedure tape. Excluding commands that specify otherwise, the tape head moves forward to the next cell after executing the command in the previous cell. When the tape head encounter a number in a cell rather than a command, it will do nothing and move on to the next cell.

The Procedure Tape is the only tape which can be used for both reading and writing - as such it is useful for storing intermediate calculations.

The *Input Tape* is used to provide external data to a procedure. It is made of a sequence of natural numbers of arbitrary length. The READ command will read the next number on the input tape, write it to the procedure tape, and move the *Input Tape head* forward. The input tape is read-once: the input tape head cannot move backwards. If the input tape has been exhausted (or if no input tape was provided), the READ command will return a 0.

The *Output Tape* is used to write data to an external source to show the results of a computation. The WRIT command writes data from the procedure tape to the location of the *Output Tape Head*, and move the output tape head forward. The output tape is write-once: the output tape head cannot move backwards.

A *procedure* consists of a series of commands and numbers, each on a separate line, which initialize the state of the procedure tape. Tape cells that have not been set are considered to be 0.

### Procedure Tape features
The procedure tape's cells can contain one of two different types of features: natural numbers and commands.

Numbers can be treated as numeric values, characters, or addresses,depending on the context of the command that utilizes them.

Commands tell the natural number calculation engine to do something when the tape head reads them. Each command examines and/or manipulates numbers in the 1 or 2 cells following it. Commands may also manipulate other areas on the tape or move the tape head, in some cases.

### Illegal Decrement Correction Subprocedure

The natural number calculation engine only handles natural numbers. If you attempt to decrement 0 (an operation which would create a negative number), the *Illegal Decrement Correction Subprocedure* will fire. This subprocedure moves the tape head moves to cell 98. You should place any processes which clean up after an illegal decrement at this location. I have found this feature very useful for solving flaws in my students' procedures.

## Syntax

Each non-empty line of a Natural Number Calculation Engine procedure represents a cell on the Procedure Tape. A line is called a *cell specifier*.

Each cell specifier contains either one of the seven commands or a number. 

The first non-empty line of an NNCE procedure corresponds to Cell 0, and so on. Empty lines are ignored by NNCE.


### Address Labels

Cell specifiers may also optionally contain an *address label*. The address label defines what address this cell specifier should initialize. The line after the address label will specify the next cell, and so on.

This procedure initalizes cells 0,7,8, and 20 to the values 1,2,3, and 4; respectively:

	1
	2 $7
	3
	4 $20

All addresses that are skipped over (in the previous example: 1-6 and 9-19) are initialized to 0, as are all cells after the last address.

If a single address is specified multiple times in an NNCE procedure, such as in the example below, the behavior is undefined:

	GOTO $10
	20
	30 $11

The cell "20" gets the implicit address $11 because it is one after $10. Then, the next cell tries to use the address $11, which creates undefined behavior.

The behavior is also undefined if an address would cause the procedure's order to be nonlinear. For example

	100 $100
	500 $50



### Named Labels

The engine also allows you to place a name instead of a number in the label field of a cell descriptor. This functions completely differently from numeric labels.

The named label itself has no impact on the procedure's semantics in that location. The engine will only make a note of the label and its location in the procedure.

However, using a named label allows you to refer to that line in other places in your procedure.  The engine will translate other uses of that label into a numeric literal equal to the named address.

Example:
	GOTO
	^my_location

	INCR $my_location
	^my_location

is equivalent to
	GOTO
	2
	INCR $2
	2

Named labels make it easier to write useful GOTO statements, since you don't have to do manual bookkeeping if you relocate a procedure.

Implementations should support using labels before their point of declaration (Such as in the example above).


### Comments

There is a comment functionality for documenting code. If you use a pound sign (#), everything after it on that line will be ignored.

Example



## End of execution
The procedure halts execution if there are no commands in the instruction pointer's current cell, and all future cells are numbers rather than commands.


## Commands

### INCR
Increment the number stored in the next cell by 1.

Undefined behavior results if the INCR command is executed when another command rather than a number is stored in the cell after it.

### DECR
Decrement the number stored in the next cell by 1.

Undefined behavior results if the DECR command is executed when another command rather than a number is stored in the cell after it.

It is an error to attempt to decrement 0. The natural number calculation engine can only handle natural numbers. If you attempt to decrement 0, the  Illegal Decrement Correction Subprocedure will fire (described above.)

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

### READ
Read the next number from the input tape and write it to the next cell on the procedure tape.

If the READ command is executed when the input tape is exhausted, 0 will be written to the next cell on the procedure tape.

### WRIT
The WRIT command examines the next cell on the procedure tape. If it is a number, it writes that number to the output tape.

It is undefined behavior to execute the WRIT command when it is followed by another command rather than number.

## A note on cell numbering

The cells that make up the procedure tape can be referenced by the COPY and GOTO commands described above. These cells are numbered starting from 0 rather than 1, as this avoids a potential error condition:

	GOTO
	0

If cells were numbered from 1, this command would not be executable.

