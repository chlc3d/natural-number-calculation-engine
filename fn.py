import sys
import re

def match(itr, sym):
	n = next(itr)
	assert n in sym, "Expected %s while parsing at %s" % (sym, [n] + list(itr)[:9])

def consume_until(itr, end):
	return consume_list(itr,end)

def consume_list(itr, end, list_sep=None, toks_between_seps=1):
	toks = []
	while True:
		saw = next(itr)
		for i in range(toks_between_seps):
			if saw != end:
				toks.append(saw)
			else:
				return toks
		if list_sep is not None:
			poss_sep = next(itr)
			if poss_sep in end:
				return toks
			assert poss_sep in list_sep


def parse_block(itr):
	match(itr, '{')
	return consume_until(itr, '}')

def parse_ftn(itr):
	name = next(itr)
	match(itr, '(')
	args = consume_list(itr, ')', ',')
	body = parse_block(itr)
	return Function(name,args,body)


class Token:
	pass

class Literal(Token):
	def __init__(self, text):
		self._text = text

class Call(Token):
	def __init__(self, ftn, arg_values):
		self._ftn = ftn
		self._params = arg_values

class Function:
	def __init__(self, name, args, body):
		self.name = name
		self.args = args
		self.body = body
		self.begin_idx = 0

	def __repr__(self):
		return "%s (%s)" % (self.name, ", ".join(self.args))


class BlockTable:
	def __init__(self):
		self._functions = dict()
		self._globals = None
		self._constants = None
		self._epilogue = None


	def add(self, block, name):
		try:
			lookup = {
				'constants': self._constants,
				'globals': self._globals,
				'epilogue': self._epilogue
			}

			assert lookup[name] is None, "Found two blocks with type %s, which must be unique" % name
			lookup[name] = block
		except KeyError:
			assert False, "Invalid block type %s" % name

	def add_ftn(self, ftn):
		assert ftn.name not in self._functions, "Found two functions with name %s!" % ftn.name
		self._functions[ftn.name] = ftn


	def parse_call(self, tok_iter):
		#function_name ( arg1 = val1, arg2 = val2 )
		name = next(tok_iter)

		match(tok_iter, '(')
		elems = consume_list(tok_iter, ')', ',', toks_between_seps=3)
		args, eqs, vals = elems[::3], elems[1::3], elems[2::3]
		assert all(x == '=' for x in eqs), "Invalid call syntax"

		called_ftn = self._functions[name]
		assert called_ftn.args == args

		return Call(called_ftn, vals)


	def process_functions(self):
		special_names = set(['BEFORE', 'BEGIN', 'CALL'])

		for ftn in self._functions.values():

			itr = iter(ftn.body)
			expanded_body = []
			has_before = False
			first_tok = True
			while True:
				try:
					tok = next(itr)
				except StopIteration:
					print "finished parsing function %s" % ftn.name
					break
				if tok not in special_names:
					expanded_body.append(Literal(tok))
				elif tok == 'BEFORE':
					assert first_tok, "BEFORE must be at beginning of block"
					has_before = True
				elif tok == 'BEGIN':
					assert has_before, "Can't have BEGIN without BEFORE"
					ftn.begin_idx = len(expanded_body) - 1
				elif tok == 'CALL':
					expanded_body.append(self.parse_call(itr))

				first_tok = False
			ftn.body = expanded_body

	def __repr__(self):
		return "Function table"


def preprocess_token(tok):
	return tok.strip()

def important_token(tok):
	return tok.strip() != ''

def tokenize_prgm(lines):
	tokenstream = []

	for line in lines:
		line_tokens = [preprocess_token(tok) 
						for tok in re.split(r'(\d+|\W+?|\s+)', line) 
						if important_token(tok)]

		for tok in line_tokens:
			if tok.startswith('#'):
				break
			else:
				tokenstream.append(tok)
	return tokenstream



def build_function_table(path):
	with open(path) as f:
		tokens = tokenize_prgm(f.readlines())

	tok_itr = iter(tokens)
	table = BlockTable()
	
	while True:
		try:
			block_type = next(tok_itr)
		except StopIteration:
			print "finished iteration"
			break

		if block_type == 'function':
			table.add_ftn(parse_ftn(tok_itr))
		else:
			table.add(parse_block(tok_itr), block_type)




	table.process_functions()
	print table._functions.values()

	return table


class CallStrategyInterface:
	def __init__(self, inlined_function_set, expanded_function_list, inlined_constant_set):
		self._inlined = inlined_function_set
		self._ftns = expanded_function_list
		self._inlined_constants = inlined_constant_set

	def place_noninlined_constants(self):
		raise NotImplementedError()

	def place_globals(self):
		raise NotImplementedError()

class MassInlineCallStrategy(CallStrategyInterface):
	def __init__(self, table):
		expanded_function_list = [table._functions['main']]
		inlined = set(table._functions.values())
		inlined.remove('main')
		inlined_constants = set(table._constants)
		
		CallStrategyInterface.__init__(inlined, expanded_function_list, inlined_constants)

if __name__ == '__main__':
	context = build_function_table(sys.argv[1])

	#print context