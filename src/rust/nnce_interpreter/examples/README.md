#Examples

## Simple
The Simple program is an example of using the natural number calculation engine for arithmetic operations.

	READ
	0 $2

This reads the current value of the input tape into address 2

	COPY
	2
	8

Copy the value in address 2 (the input character), into address 8.

	INCR $7
	0 $8

Add 1 to the value stored in address 8 (the input character). Note that we need the label before INCR, since otherwise INCR would be stored in address 6, and increment address 7. The address in the cell-specifier for address 8 is technically not necessary, since the address after the previous cell-specifier is the default.

	COPY
	8
	20

Copy the value in address 8 (input + 1) into address 20.

	DECR $19
	0

Decrement the value in address 20. There is no risk of an error here, since we know the value is 1 or higher.

	COPY
	20
	40

Copy the value in address 20 (input) into address 40.

	DECR $39
	0

Decrement the value in address 40 (input). If input is 0, this will cause us to jump ahead to address 98.

	COPY
	40
	60

Copy the value in address 40 (input - 1) into address 60.

	DECR $59
	10

Decrement the value in address 60 (input - 1). Note that address 60 being initialized to 10 instead of 0 has no impact on execution -- it will be overwritten by this point anyway. If input is 1, we'll go to address 98

	GOTO
	0

Return to the beginning of the program. We will execute cells 1 to 62 again, using the next element of the input tape. We'll continue to loop until something causes us to jump ahead.

	DECR $98
	1

Decrement the value stored in address 99. The first time we execute this line, address 99 will become 0. The second time we execute this line, we'll enter an infinite loop. Each time we execute it, we'll attempt to decrement 0 and jump to address 98.

	READ $200
	0 $201

	COPY $203
	201 $204
	207 $205

	WRIT $206
	0 $207

Read the next value of the input tape and write it to the output tape.

Overall, the Simple function will iterate through the input until it encounters a character whose value is 0 or 1. Then it will write out the value after that to the output tape.

## Cat

The CAT program reads input until it encounters the end of the input tape (marked by a 0), and writes each character to the output tape. This is a simple example of an NNCE control flow loop. The lines

	DECR
	0 $7

will cause the error-handling mechanism to jump to line 98 if the value stored in address 7 is still 0 after copying the read data into it. This is how the program terminates. If the input is not 0, the lines

	GOTO
	0

cause the program to start over, allowing a new character to be read.


## Brainfuck

This is a more involved example written in NN++. The use of NN++ allows for comments that annotate the source code and named labels that make its algorithms a little easier to follow.

# TODO

## Rot13
## Integer Square root
