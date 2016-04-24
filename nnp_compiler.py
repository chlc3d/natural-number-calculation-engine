import sys

def compile_file(filename):
	return compile(open(filename).readlines())


def compile(program_lines):
	curr_addr = 0

	name_to_loc = dict()

	newlines = []

	#first pass:
	#Find symbolic addresses
	for idx, line in enumerate(program_lines):

		#remove braces, they're used for the meta-assembler!
		line = filter(lambda x: x != '{' and x != '}', line)
		line = line.strip()
		line = ''.join(line.split('#')[0].split())
		line_segs = line.split(":")
		if line != '':
			curr_addr += 1

		if len(line_segs) == 2:
			addr = line_segs[0]
			if not addr.isdigit():
				addr = addr.lower()
				assert addr not in name_to_loc, "Multiple definitions of %s (line %i)" % (addr, idx+1)

				name_to_loc[addr] = str(curr_addr)
			else:
				assert curr_addr <= int(addr), "Could not satisfy current address in %s" % line
				curr_addr = int(addr)
		else:
			assert len(line_segs) == 1, "too many sections in %s" % line
		newlines.append(line)

	program_lines = newlines
	result_lines = []
	#Second pass:
	#Convert usages of symbolic addresses
	for idx, line in enumerate(program_lines):
		segs = line.split(':')

		segs = [name_to_loc.get(s.lower(), s) for s in segs]
		for seg in segs:
			assert seg.isdigit() or seg.lower() in ['', 'outpd', 'incr', 'decr', 'copy', 'inpt', 'outp', 'goto'], "unknown segment %s on line %i" % (seg, idx)
		result_lines.append(':'.join(segs))
	return result_lines


if __name__ == "__main__":
	print '\n'.join(compile_file(sys.argv[1]))
