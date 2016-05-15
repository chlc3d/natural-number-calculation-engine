from collections import OrderedDict
import sys
import argparse

EOF = 0

class State:
	def __init__(self, **kwargs):
		self.memory = kwargs['memory']
		self.pc = 0
		self.tape = kwargs['tape']
		self.output = ''
		self.head_moves = 0

		self.executed_instructions = {
			"incr": 0,
			"decr": 0,
			"goto": 0,
			"copy": 0,
			"read": 0,
			"writ": 0,
			"writd": 0,
			"number": 0
		}

		self.executeds = {}

	def mark_line_executed(self):
		self.executeds[self.pc] = self.executeds.get(self.pc, 0) + 1


	def num_instructions_executed(self):
		sm = 0
		for name,count in self.executed_instructions.items():
			if name != 'number':
				sm += count
		return sm
	def get(self):
		return self.memory.get(self.pc, 0)

	def get_int(self):
		val = self.get()
		assert(type(val) is int)
		return val

	def set(self, val):
		self.memory[self.pc] = val

	def next(self):
		self.pc += 1
		self.head_moves +=1

	def jump(self, pc):
		self.head_moves += abs(self.pc - pc)
		self.pc = pc

	def __str__(self):
		result = self.output

		result += "\n"
		result += "executed instructions: %s" % self.executed_instructions
		result += '\n'
		result += "total instructions: %s" % self.num_instructions_executed()
		result += '\n'
		result += "head moves: %s" % self.head_moves
		result += '\n'
		result += "hot lines: %s" % (
			sorted(self.executeds.items(), key=lambda x:x[1], reverse=True)
			[:50])
		result += '\n'
		result += "final pc: %s" % self.pc
		return result

#def get(mem, pc):
	#return mem.get(pc, 0)
#
#def get_int(mem, pc):
	#val = get(mem, pc)
	#assert(type(val) is int)
	#return val

def _incr(state):
	state.next()
	state.set(state.get_int() + 1)

def _decr(state):
	#print '---'

	#print state.pc+1
	#print state.memory[state.pc+1]
	state.next()
	val = state.get_int()
	if val <= 0:
		#go to trap
		state.jump(98)
	else:
		state.set(val -1)

def _goto(state):
	state.next()
	state.jump(state.get_int())

def _copy(state):
	orig_addr = state.pc

	state.next()
	src_addr = state.get_int()
	state.next()
	dest_addr = state.get_int()

	state.jump(src_addr)
	value = state.get()

	state.jump(dest_addr)
	state.set(value)

	state.jump(orig_addr + 3)

def _user_input(state):
	state.next()
	if state.tape == "":
		state.set(EOF)
	else:
		state.set(ord(state.tape[0]))
		state.tape = state.tape[1:]


def _output(state):
	state.next()
	state.output += chr(state.get())

def _debug_output(state):
	state.next()
	state.output += "%s: %s\n" % (state.pc, state.get())
	print "%s: %s\n" % (state.pc, state.get())

def interpret(program, input_files, debug=False):

	try:
		program_lines = open(program).readlines()
	except TypeError:
		program_lines = program


	user_input = ''
	for f in input_files:
		user_input += open(f, 'rb').read()
		user_input += chr(0)

	if debug:
		print ':'.join(x.encode('hex') for x in user_input)

	state = State(memory=dict(), tape=user_input)

	for line in program_lines:
		#remove whitespace
		line = ''.join(line.split())

		#remove segment of line after comment marker
		line = ''.join(line.split('#')[0].split())
		if line == '':
			continue

		line_sections = line.split('$')
		content = line_sections[0]
		if len(line_sections) == 1:
			state.pc += 1
		else:
			state.pc = int(line_sections[1])
		line_idx = state.pc
			

		if content.isdigit():
			state.memory[line_idx] = int(content)
		else:
			state.memory[line_idx] = content

	max_pc = state.pc
	state.pc = 1

	while state.pc <= max_pc:

		instr = state.get()

		#print "%s: %s (next: %s)" % (state.pc, instr, get(state.memory,state.pc+1))
		#print state.pc
		#print instr
		if type(instr) is int:
			state.next()
			state.executed_instructions['number'] += 1
			continue

		instr = instr.lower()

		state.mark_line_executed()
		state.executed_instructions[instr] += 1
		{
			"incr": _incr,
			"decr": _decr,
			"goto": _goto,
			"copy": _copy,
			"read": _user_input,
			"writ": _output,
			"writd": _debug_output
		}[instr](state)


	if debug:
		print "final state.memory: %s" % sorted(state.memory.items())
	return state

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Compile and run an NN++ program")

	parser.add_argument('nn_file', help="NNCE file to run")
	parser.add_argument('--debug', action='store_true', help="Enable debug features and output for interpreter")
	parser.add_argument('--write-perf-info', action='store_true', help="Write interpreter performance info to stdout")
	parser.add_argument('--nn-input-files', default=[], type=str, nargs="+", help = "Input files to NNCE script")
	
	args = parser.parse_args()
	state = interpret(args.nn_file, args.nn_input_files, debug=args.debug)

	if args.write_perf_info:
		print state
	else:
		print state.output

	if args.debug:
		print ""
		print state.executed_instructions
		print "head moves: %s" % state.head_moves
		print "final pc: %s" % state.pc
		