import os
import sys

class NNCEPreprocessorException(Exception):
	pass

def preprocess(filename, use_extensions):
	return _preprocess_lines(open(filename).readlines(), filename, use_extensions)


def _include_recursive(program_lines, current_file_dir):
	for idx, line in enumerate(program_lines):
		line = line.strip()
		if line.startswith('NNP_INCLUDE'):
			#Pull in include file
			#(Use relative path from this NNP file)
			path = line.split(' ')[1]
			with open(os.path.join(current_file_dir, path)) as f:
				new_lines = f.readlines()
				
				# Call recursively with the new file
				new_lines = _include_recursive(new_lines, os.path.dirname(path))

				# Add new_lines to program_lines
				program_lines = program_lines[:idx] + new_lines + program_lines[idx+1:]

				# Call _include_recursive again to reset the loop
				# TODO(tstamper): we should do this in a more efficent way
				return _include_recursive(program_lines, current_file_dir)
	return program_lines

def _preprocess_lines(program_lines, path, use_extensions):
	curr_addr = 0

	name_to_loc = dict()

	newlines = []

	# Resolve includes
	if use_extensions:
		program_lines = _include_recursive(program_lines, os.path.dirname(path))

	#first pass:
	#Find symbolic addresses
	for idx, line in enumerate(program_lines):

		#remove braces, they're used for the meta-assembler!
		line = filter(lambda x: x != '{' and x != '}', line)
		line = line.strip()

		if use_extensions:
			line = ''.join(line.split('#')[0].split())

		line_segs = line.split("$")
		if line != '':
			curr_addr += 1

		if len(line_segs) == 2:
			addr = line_segs[1]
			if not addr.isdigit():
				addr = addr.lower()
				addr = addr.strip()
				assert addr != '', "Empty address (line %i)" % (idx + 1)
				assert addr not in name_to_loc, "Multiple definitions of %s (line %i)" % (addr, idx+1)
				name_to_loc[addr] = str(curr_addr)
			else:
				if curr_addr > int(addr):
					raise NNCEPreprocessorException(
						"Could not satisfy address %s. Current address = %s. Line %i"
						% (line, curr_addr, idx + 1))
				curr_addr = int(addr)
		else:
			assert len(line_segs) == 1, "too many sections in %s" % line
		newlines.append(line)

	program_lines = newlines
	result_lines = []

	#Second pass:
	#Convert usages of symbolic addresses
	for idx, line in enumerate(program_lines):
		segs = line.split('$')
		cell = segs[0]
		if len(cell) > 0 and cell[0] == '^':
			cell_value = cell.lower()[1:]
			assert cell_value in name_to_loc, \
						"Undefined address %s (used on line %i)" % (cell, idx)
			cell = name_to_loc[cell.lower()[1:]]
		assert cell.isdigit() or cell.lower()  \
					in ['', 'writd', 'incr', 'decr', 'copy', 'read', 'writ', 'goto'], \
					"unknown segment %s on line %i" % (cell, idx)

		if len(segs) > 1:
			assert len(segs) == 2, "Extra segment %s on line %i" % (seg[2], idx)
			addr = segs[1]
			addr = name_to_loc.get(addr.lower(), addr)
			assert addr.isdigit()
		if len(segs) == 1:
			result_lines.append(cell)
		else:
			result_lines.append('$'.join([cell,addr]))
	return result_lines


if __name__ == "__main__":
	print '\n'.join(preprocess(sys.argv[1], False))
