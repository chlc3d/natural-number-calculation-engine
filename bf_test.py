import nat

def print_state(st):
	print st.output

	print ""
	print "executed instructions: %s" % st.executed_instructions
	print "total instructions: %s" % st.num_instructions_executed()
	print "head moves: %s" % st.head_moves
	print "final pc: %s" % st.pc


print "compare cat.nn to brainfuck cat interpret!"
print_state(nat.interpret(False, 'bfi.txt', ['brainfuck/test/cat/cat.bf',
								'brainfuck/test/cat/catinput.txt']))

print_state(nat.interpret(False, 'examples/cat.nn', ['brainfuck/test/cat/catinput.txt']))



