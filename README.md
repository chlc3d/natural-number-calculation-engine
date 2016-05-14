# Natural Number Calculation Engine (NNCE)

NNCE is a tape-based esoteric programming language. It has two data types, natural numbers and commands.
This repository contains an [interpreter](nn_interpreter/README.md), a [compiler for a meta-language with additional usability features](nnp_compiler/README.md), and a variety of [examples](examples/README.md).

## Concepts

### Tapes
The natural-number calculation engine can be modeled as a machine with three tapes. Each tape has a *tape head*, which specifies the location of execution, input, or output

The *Program Tape* stores all commands and all data that the program is operating on. The program tape consists of a series of cells, each of which can store a command or a natural number. All of the commands defined by NNCE read and/or write information from/to the program tape.  The *Tape Head* tracks the program's current location on the program tape. Excluding commands that specify otherwise, the tape head moves forward to the next cell after executing the command in the previous cell. When the tape head encounter a number in a cell rather than a command, it will do nothing and move on to the next cell.

The *Input Tape* is used to provide external data to a program. The READ command will read the next character on the input tape, write it to the program tape, and move the *Input Tape head* forward. The input tape is read-once: the input tape head cannot move backwards.

The *Output Tape* is used to write data to an external source to show the results of an NNCE computation. The WRIT command writes data from the program tape to the location of the *Output Tape Head*, and move the output tape head forward. The output tape is write-once: the output tape head cannot move backwards.

An NNCE program consists of a series of commands and numbers, separated by line breaks, which initialize the state of the program tape. Tape cells that have not been set are considered to be 0.

### Cells

The program tape consists of a series of cells. Cells are indexed from 0 and can be individually addressed by the COPY and GOTO command.

### Data types
The program tape's cells can contain two data types: natural numbers and commands.

Numbers can be treated as numeric values, characters, or addresses, depending on the context of the command that utilizes them.

Commands tell the natural number calculation engine to do something when the tape head reads them. Each command examines and/or manipulates numbers in the 1 or 2 cells following it. Commands may also manipulate other areas on the tape or move the tape head, in some cases.

### Exception Handling

The natural number calculation engine only handles natural numbers. If you attempt to decrement 0 (an operation which would create a negative number), the *exception-handling mechanism* will fire. When an exception occurs, the tape head moves to cell 98. You should place any exception-handling code at this location.

### I/O mapping

The *I/O mapping* is a function from a set of characters (the *I/O range*) to a set of natural numbers. The input tape should contain only characters on the I/O range. The I/O mapping is used to select the number to write for the READ command. The WRIT command operates on the same range to write characters to the output tape. These are defined in more detail in the descriptions of the READ and WRIT commands.

The details of the I/O mapping and I/O range are implementation-defined.

## Syntax

Each non-empty line of an NNCE program represents a cell. A line is called a *cell specifier*.

Each cell specifier contains either one of the seven NNCE commands or a number. When the NNCE program begins, the cell corresponding to the cell specifier is initialized with that value. All whitespace other than newlines is ignored by NNCE.

The first non-empty line of an NNCE program corresponds to Cell 0, and so on. Empty lines are ignored by NNCE.

Cell specifiers may also optionally contain an *address label*. The address label defines what address this cell specifier should initialize. The line after the address label will specify the next cell, and so on.

This program initalizes cells 0,7,8, and 20 to the values 1,2,3, and 4; respectively:

	1
	2 $7
	3
	4 $20

If a single address is specified multiple times in an NNCE program, such as in the example below, the behavior is undefined:

	GOTO $10
	20
	30 $11


### Comments

NNCE provides a comment functionality for documenting code. If you use a pound sign (#), everything after it on that line will be ignored.

Example

	#Read the next 6 characters of input,
	#then go to the trap address
	5 $10

	READ $20
	0

	#Decrement index and trap if it hits -1
	COPY
	10
	30

	DECR
	0 $30

	COPY
	30
	10

	#If we didn't trap, start the loop over.
	GOTO
	20

## End of execution
The NNCE program halts execution if there is no command in the current cell or any cell afterward.

## File Conventions

NNCE programs should be named *.nn. Both unix and windows-style newlines are supported.

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
### READ
Read the next character from the input tape, and write the number which corresponds to it to the next cell on the program tape.

The I/O mapping determines the number to write to the program tape.

If the READ command is executed when the input tape is exhausted, 0 will be written to the next cell on the program tape.

### WRIT
The WRIT command examines the next cell on the program tape. If it is a number in the valid I/O range, it writes the character corresponding to that number to the output tape.

The I/O mapping determines the character to write to the output tape.
The mapping of numbers to characters is implementation-defined, but must match that of the READ command.

It is undefined behavior to execute the WRIT command when it is followed by another command rather than number.
It is undefined behavior to attempt to output a number outside of the I/O range.

### WRITD
The behavior of the WRITD command is implementation-defined. Its intended use is for debugging NNCE programs.
