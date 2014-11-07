import sys
program = open(sys.argv[1]).readlines()

curr_addr = 0

name_to_loc = dict()

newlines = []

#first pass:
#Find symbolic addresses
for idx, line in enumerate(program):
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

program = newlines
newlines = []
#Second pass:
#Convert usages of symbolic addresses
for idx, line in enumerate(program):
	segs = line.split(':')

	segs = [name_to_loc.get(s.lower(), s) for s in segs]
	for seg in segs:
		assert seg.isdigit() or seg.lower() in ['', 'outpd', 'incr', 'decr', 'copy', 'inpt', 'outp', 'goto'], "unknown segment %s on line %i" % (seg, idx)
	print ':'.join(segs)


