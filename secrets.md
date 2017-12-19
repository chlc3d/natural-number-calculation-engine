
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