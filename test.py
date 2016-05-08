import nn_interpreter.nn_interpreter as nn_interpreter
import nnp_compiler.nnp_compiler as nnp_compiler
import os

def print_state(st):
	print st.output

	print ""
	print "executed instructions: %s" % st.executed_instructions
	print "total instructions: %s" % st.num_instructions_executed()
	print "head moves: %s" % st.head_moves
	print "final pc: %s" % st.pc
	print ""


bf_dir = 'examples/brainfuck'
bf_test_dir = 'examples/brainfuck/test'

bfi_compiled = nnp_compiler.compile_file(os.path.join(bf_dir, 'bfi.nnp'))

print "bfi.nnp hello.bf:"
print_state(nn_interpreter.interpret(False, bfi_compiled, [os.path.join(bf_test_dir, 'hello/hello.bf')]))

print "bfi.nnp cat.bf catinput.txt:"
print_state(nn_interpreter.interpret(False, bfi_compiled,
	[os.path.join(bf_test_dir, 'cat/cat.bf'),
	os.path.join(bf_test_dir, 'cat/catinput.txt')]))

print "bfi.nnp rot13.bf rot13input.txt:"
print_state(nn_interpreter.interpret(False, bfi_compiled,
	[os.path.join(bf_test_dir, 'cristofd/rot13.bf'),
	os.path.join(bf_test_dir, 'cristofd/rot13input.txt')]))

print "bfi.nnp stress1.bf:"
print_state(nn_interpreter.interpret(False, bfi_compiled,
	[os.path.join(bf_test_dir, 'cristofd/stress1.bf')]))

print "cat.nn catinput.txt:"
print_state(nn_interpreter.interpret_file(False, 'examples/cat.nn',
	[os.path.join(bf_test_dir, 'cat/catinput.txt')]))

print "simple.nn catinput.txt:"
print_state(nn_interpreter.interpret_file(False, 'examples/simple.nn',
	[os.path.join(bf_test_dir, 'cat/catinput.txt')]))


