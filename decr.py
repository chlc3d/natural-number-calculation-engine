from collections import OrderedDict
import sys

debug = False
pc = 0
EOF = 0
program = open(sys.argv[1]).readlines()

user_input = ''
for f in sys.argv[2:]:
	user_input += open(f, 'rb').read()
	user_input += chr(0)

print ':'.join(x.encode('hex') for x in user_input)


memory = dict()

for line in program:
	line = ''.join(line.split())
	if line == '':
		continue

	line_sections = line.split(':')
	if len(line_sections) == 1:
		pc += 1
		line_idx = pc
		content = line_sections[0]
	else:
		line_idx = int(line_sections[0])
		pc = line_idx
		content = line_sections[1]

	if content.isdigit():
		memory[line_idx] = int(content)
	else:
		memory[line_idx] = content

max_pc = pc

def get(mem, id):
	return mem.get(id, 0)

def get_int(mem, id):
	val = get(memory, id)
	assert(type(val) is int)
	return val

pc = 1
while pc <= max_pc:
	instr = get(memory, pc)
	if type(instr) is int:
		pc += 1
		continue

	def _incr():
		global pc
		val = get_int(memory, pc+1)
		memory[pc+1] = val + 1
		pc += 1
		if debug:
			print "%s: incr %s" % (pc, val)

	def _decr():
		global pc
		#print '---'

		#print pc+1
		#print memory[pc+1]
		val = get_int(memory, pc+1)
		if debug:
			print "%s: decr %s" % (pc, val)
		if val <= 0:
			if debug:
				print "%s:  Trap = %s" % (pc, memory.get(99))
			pc = 98
		else:
			memory[pc+1] = val - 1
			pc += 1

	def _goto():
		global pc
		val = get_int(memory, pc+1)
		if debug:
			print "%s: goto %s" % (pc, val)
		pc = val

	def _copy():
		global pc
		global max_pc
		src_addr = get_int(memory, pc+1)
		dest_addr = get_int(memory, pc+2)
		memory[dest_addr] = get(memory, src_addr)
		if debug:
			print "%s: copy %s to %s" % (pc, src_addr, dest_addr)
			print "  Value= %s" % get(memory, src_addr)

		if dest_addr > max_pc:
			max_pc = dest_addr

		pc += 1

	def _user_input():
		global pc
		global user_input
		if user_input == "":
			memory[pc+1] = EOF
		else:
			memory[pc+1] = ord(user_input[0])
			user_input = user_input[1:]
		if debug:
			print "%s: user_input < %s" % (pc, memory[pc+1])
		pc += 1

	def _output():
		global pc
		sys.stdout.write(chr(get(memory, pc + 1)))
		pc += 1

	def _debug_output():
		global pc
		print "%s: %s" % (pc, get(memory, pc+1))
		pc += 1

	{
		"incr": _incr,
		"decr": _decr,
		"goto": _goto,
		"copy": _copy,
		"inpt": _user_input,
		"outp": _output,
		"outpd": _debug_output
	}[get(memory, pc).lower()]()

print ""
print "final PC: %s" % pc
if debug:
	print "final memory: %s" % sorted(memory.items())