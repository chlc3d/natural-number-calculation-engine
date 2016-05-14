# Natural Number++ (NN++)

NN++ is a set of extensions for NNCE that make writing NNCE programs easier.

These are language extensions instead of core language pieces to make writing NNCE interpreters easier.

This package includes an NN++ compiler (nnp_compiler.py), which can be used to translate an NN++ program into an NNCE program.
eter
NN++ also provides features for indicating relationships between pieces of your code. These currently have no effect on the compilation process, but could be used as hints for optimization techniques.

## Named labels
NN++ allows you to place a name instead of a number in the label field of a cell descriptor. This functions completely differently from numeric labels.

The named label itself has no impact on the program's semantics in that location. The NN++ compiler will translate this into a label that simply refers to the cell this cell-descriptor would already describe.

However, using a named label allows you to refer to that line in other places in your program.  The NN++ compiler will translate other uses of that label into a numeric literal equal to the line.

Example:
	GOTO
	my_location

	INCR $my_location
	my_location

Will become
	GOTO
	2
	INCR $2
	2

Named labels make it easier to write useful GOTO statements, since you don't have to do manual bookkeeping if you relocate a procedure.

Example:

## Code Sections

You can put curly braces ("{" and "}") around any number of cell-descriptors. These define those cell-descriptions as a *code section*. Code sections cannot be nested.

Currently code sections have no semantic meaning. In the future they will serve as a note to the optimizer that the relative order of these cell-descriptions must be observed, and nothing else can be inserted between them.

## Future Directions

### Optimization
Complex NNCE programs may have many procedures and a variety of data segments. Determining the optimal order of these segments to minimize tape head movements is a difficult, tedious process. An optimization technique such as simulated annealing could be used to find an effective order of data and procedures to minimize tape head movements.

This feature would use code sections to determine what should be considered an independent segment.