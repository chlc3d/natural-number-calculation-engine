import nat

def print_state(st):
	print st.output

	print ""
	print "executed instructions: %s" % st.executed_instructions
	print "total instructions: %s" % st.num_instructions_executed()
	print "head moves: %s" % st.head_moves
	print "final pc: %s" % st.pc
	print ""

print "bfi.txt hello.bf:"
print_state(nat.interpret(False, 'bfi.txt', ['brainfuck/test/hello/hello.bf']))

print "bfi.txt cat.bf catinput.txt:"
print_state(nat.interpret(False, 'bfi.txt', ['brainfuck/test/cat/cat.bf',
								'brainfuck/test/cat/catinput.txt']))

print "bfi.txt rot13.bf rot13input.txt:"
print_state(nat.interpret(False, 'bfi.txt', ['brainfuck/test/cristofd/rot13.bf', 'brainfuck/test/cristofd/rot13input.txt']))

print "bfi.txt stress1.bf:"
print_state(nat.interpret(False, 'bfi.txt', ['brainfuck/test/cristofd/stress1.bf']))

print "cat.nn catinput.txt:"
print_state(nat.interpret(False, 'examples/cat.nn', ['brainfuck/test/cat/catinput.txt']))

print "simple.nn catinput.txt:"
print_state(nat.interpret(False, 'simple.nn', ['brainfuck/test/cat/catinput.txt']))


