import nn_interpreter
import nnp_compiler

def print_state(st):
	print st.output

	print ""
	print "executed instructions: %s" % st.executed_instructions
	print "total instructions: %s" % st.num_instructions_executed()
	print "head moves: %s" % st.head_moves
	print "final pc: %s" % st.pc
	print ""

bfi_compiled = nnp_compiler.compile_file('brainfuck/bfi.nnp')

print "bfi.nnp hello.bf:"
print_state(nn_interpreter.interpret(False, bfi_compiled, ['brainfuck/test/hello/hello.bf']))

print "bfi.nnp cat.bf catinput.txt:"
print_state(nn_interpreter.interpret(False, bfi_compiled, ['brainfuck/test/cat/cat.bf',
								'brainfuck/test/cat/catinput.txt']))

print "bfi.nnp rot13.bf rot13input.txt:"
print_state(nn_interpreter.interpret(False, bfi_compiled, ['brainfuck/test/cristofd/rot13.bf', 'brainfuck/test/cristofd/rot13input.txt']))

print "bfi.nnp stress1.bf:"
print_state(nn_interpreter.interpret(False, bfi_compiled, ['brainfuck/test/cristofd/stress1.bf']))

print "cat.nn catinput.txt:"
print_state(nn_interpreter.interpret_file(False, 'examples/cat.nn', ['brainfuck/test/cat/catinput.txt']))

print "simple.nn catinput.txt:"
print_state(nn_interpreter.interpret_file(False, 'examples/simple.nn', ['brainfuck/test/cat/catinput.txt']))


