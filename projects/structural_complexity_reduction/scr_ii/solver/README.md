# Exact solver

The baseline solver exhaustively traverses the binary decision tree and applies only the independent downstream solution predicate.

The SCR solver is the same solver with the frozen structural filter inserted before a node is expanded.

The solution-checking code must be identical in both arms.
