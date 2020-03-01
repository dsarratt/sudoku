# Sudoku solver

## Usage

Call sudoku.solve(), pass it a string consisting of nine lines
with nine digits each line. Unknown cells can be any non-numeric character, e.g.

    python sudoku.py <<EOF
    24...8...
    ....147..
    91..73..2
    16...75..
    .2.145.8.
    ..43...71
    8..72..13
    ..183....
    ...4...67
    EOF

## Code layout

1. Load the sudoku grid as a 2D array of sets, each set represents a single cell and contains the possible candidates that could fill the given cell
2. For any cells where the number is already known (i.e. a set of 1), replace the set with an integer
3. For each known integer, remove the integer from every other candidate set in the same row, column, and square
4. If steps 2 or 3 have pruned the number of candidates, go back to step 2
5. Else (steps 2 and 3 are no longer making progress), make a clone of the sudoku grid and guess one of the unknowns. Recurse back to step 2 using this cloned grid.
6. If the guess made the grid unsolvable, go back to step 5 and make a different guess
