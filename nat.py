from collections import OrderedDict
import sys

EOF = 0

class State:
	def __init__(self, **kwargs):
		self.memory = kwargs['memory']
		self.pc = kwargs['pc']
		self.tape = kwargs['tape']

def get(mem, pc):
	return mem.get(pc, 0)

def get_int(mem, pc):
	val = get(mem, pc)
	assert(type(val) is int)
	return val

def _incr(state):
	val = get_int(state.memory, state.pc+1)
	state.memory[state.pc+1] = val + 1
	state.pc += 1

def _decr(state):
	#print '---'

	#print state.pc+1
	#print state.memory[state.pc+1]
	val = get_int(state.memory, state.pc+1)
	if val <= 0:
		#go to trap
		state.pc = 98
	else:
		state.memory[state.pc+1] = val - 1
		state.pc += 1

def _goto(state):
	val = get_int(state.memory, state.pc+1)
	state.pc = val

def _copy(state):
	src_addr = get_int(state.memory, state.pc+1)
	dest_addr = get_int(state.memory, state.pc+2)
	state.memory[dest_addr] = get(state.memory, src_addr)

	#if dest_addr > max_state.pc:
		#max_state.pc = dest_addr

	state.pc += 1

def _user_input(state):
	if state.tape == "":
		state.memory[state.pc+1] = EOF
	else:
		state.memory[state.pc+1] = ord(state.tape[0])
		state.tape = state.tape[1:]

	state.pc += 1

def _output(state):
	sys.stdout.write(chr(get(state.memory, state.pc + 1)))
	state.pc += 1

def _debug_output(state):
	print "%s: %s" % (state.pc, get(state.memory, state.pc+1))
	state.pc += 1

def interpret(debug, program_path, input_files):

	program = open(program_path).readlines()

	user_input = ''
	for f in input_files:
		user_input += open(f, 'rb').read()
		user_input += chr(0)

	print ':'.join(x.encode('hex') for x in user_input)

	state = State(memory=dict(), tape=user_input, pc=0)

	for line in program:
		line = ''.join(line.split())
		if line == '':
			continue

		line_sections = line.split(':')
		if len(line_sections) == 1:
			state.pc += 1
			line_idx = state.pc
			content = line_sections[0]
		else:
			line_idx = int(line_sections[0])
			state.pc = line_idx
			content = line_sections[1]

		if content.isdigit():
			state.memory[line_idx] = int(content)
		else:
			state.memory[line_idx] = content

	max_pc = state.pc
	state.pc = 1

	while state.pc <= max_pc:

		instr = get(state.memory, state.pc)

		#print "%s: %s (next: %s)" % (state.pc, instr, get(state.memory,state.pc+1))
		#print state.pc
		#print instr
		if type(instr) is int:
			state.pc += 1
			continue

		{
			"incr": _incr,
			"decr": _decr,
			"goto": _goto,
			"copy": _copy,
			"inpt": _user_input,
			"outp": _output,
			"outpd": _debug_output
		}[get(state.memory, state.pc).lower()](state)

	print ""
	print "final state.pc: %s" % state.pc
	if debug:
		print "final state.memory: %s" % sorted(state.memory.items())

if __name__ == '__main__':
	interpret(False, sys.argv[1], sys.argv[2:])