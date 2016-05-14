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

def validate(nn_program, args, expected):
	state = nn_interpreter.interpret(False, nn_program, args)
	print "expected: \n%s." % expected
	print "output: \n%s." % state.output

	assert state.output == expected

bf_dir = 'examples/brainfuck'
bf_test_dir = 'examples/brainfuck/test'

bfi_compiled = nnp_compiler.compile_file(os.path.join(bf_dir, 'bfi.nnp'))

catinput = os.path.join(bf_test_dir, 'cat/catinput.txt')
with open(catinput, 'r') as f:
	catinput_text = f.read()

print "cat.nn catinput.txt:"
validate('examples/cat.nn',
	[catinput],
	catinput_text)

print "bfi.nnp cat.bf catinput.txt:"
validate(bfi_compiled,
	[os.path.join(bf_test_dir, 'cat/cat.bf'), catinput],
	catinput_text)

print "bfi.nnp numwarp.bf:"
with open(os.path.join(bf_test_dir, 'cristofd/numwarp_example_output.txt')) as f:
	numwarp_example_output = f.read()
validate(bfi_compiled, [os.path.join(bf_test_dir, 'cristofd/numwarp.b'),
	os.path.join(bf_test_dir, 'cristofd/numwarp_example.txt')],
	numwarp_example_output)

print "bfi.nnp stress1.bf:"
validate(bfi_compiled, [os.path.join(bf_test_dir, 'cristofd/stress1.bf')],
	'H\n')

print "bfi.nnp hello.bf:"
validate(bfi_compiled, [os.path.join(bf_test_dir, 'hello/hello.bf')],
	'Hello World!')

print "bfi.nnp rot13.bf rot13input.txt:"
validate(bfi_compiled,
	[os.path.join(bf_test_dir, 'cristofd/rot13.bf'),
	os.path.join(bf_test_dir, 'cristofd/rot13input.txt')],
	"~ zyx mlk ~")




