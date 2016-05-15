import nn_interpreter.nn_interpreter as nn_interpreter
import nnp_compiler.nnp_compiler as nnp_compiler
import argparse
import sys
### Compile and run an NN++ program.

parser = argparse.ArgumentParser(description="Compile and run an NN++ program")

parser.add_argument('nnp_file', help="NN++ file to run")
parser.add_argument('--compile-output', type=str, help="Where to store output file")
parser.add_argument('--debug', action='store_true', help="Enable debug features and output for interpreter")
parser.add_argument('--write-perf-info', action='store_true', help="Write interpreter performance info to stdout")
parser.add_argument('--compile-only', action='store_true', help="Only compile the file; don't run it. Use with --compile-output")
parser.add_argument('--nn-input-files', default=[], type=str, nargs="+", help = "Input files to NNCE script")
args = parser.parse_args()

compiled = nnp_compiler.compile_file(args.nnp_file)

if args.compile_output:
	with open(args.compile_output, 'w') as f:
		f.write('\n'.join(compiled))

if not args.compile_only:
	interpreter_state = nn_interpreter.interpret(compiled, args.nn_input_files, debug=args.debug)
	if args.write_perf_info:
		print interpreter_state
	else:
		pass
		#print interpreter_state.output