import _nnce_interpreter
import _nnce_preprocessor
import argparse
import sys
### Compile and run an NN++ program.

parser = argparse.ArgumentParser(description="Compile and run an NNCE program. See interpreter.md for more details")

parser.add_argument('nnce_file', help="NNCE file to run")
parser.add_argument('--preprocessor-output', type=str, help="Where to store output file")
parser.add_argument('--debug', action='store_true', help="Enable debug features and output for interpreter")
parser.add_argument('--write-perf-info', action='store_true', help="Write interpreter performance info to stdout")
parser.add_argument('--preprocess-only', action='store_true', help="Only preprocess the file; don't run it. Use with --preprocessor-output")
parser.add_argument('--nn-input-files', default=[], type=str, nargs="+", help = "Input files to NNCE script. EOF is represented by a 0 character")
parser.add_argument('--use-extensions', action='store_true', help="Allow usage of interpreter-defined language extensions (comments and NNCE_INCLUDE calls).")
args = parser.parse_args()

processed = _nnce_preprocessor.preprocess(args.nnce_file, args.use_extensions)

if args.preprocessor_output:
	with open(args.preprocessor_output, 'w') as f:
		f.write('\n'.join(processed))

if not args.preprocess_only:
	interpreter_state = _nnce_interpreter.interpret(processed, args.nn_input_files, debug=args.debug)
	if args.write_perf_info:
		print interpreter_state
	else:
		pass
		#print interpreter_state.output