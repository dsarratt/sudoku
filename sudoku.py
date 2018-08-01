from __future__ import print_function

from copy import deepcopy
import logging

def canonicalise(grid):
    """Convert any sets of 1 into ints"""
    for row in grid:
        for colnum, cell in enumerate(row):
            if isinstance(cell, set) and len(cell) == 1:
                row[colnum] = cell.pop()

def initialise(gridstring):
    """Take a string-format grid and return a 2D array of sets
    
    Coords are Y,X (row, then col)
    """
    # Validate the string
    gridstring = gridstring.strip('\n')
    if gridstring.count('\n') < 8:
        raise ValueError('gridstring should be 9 lines long')
    
    # Initialise an empty grid
    grid = []
    for _ in range(9):
        grid.append([None] * 9)
    
    # Set numbers
    for rownum, row in enumerate(gridstring.split('\n')):
        if rownum > 8:
            # Ignore extra lines
            break
        elif len(row) != 9:
            raise ValueError("row {0} is not 9 chars".format(rownum))
        
        for colnum, cell in enumerate(row):
            try:
                grid[rownum][colnum] = int(cell)
            except ValueError:
                grid[rownum][colnum] = set(range(1, 10))
    
    return grid

def is_solved(grid):
    """Return whether a grid is solved"""
    for row in grid:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True

def validate(grid):
    """Raise an error if any cells have no candidates, or if there
    are conflicting singletons.
    """
    # Check for any cells which have no candidates
    for row in grid:
        for cell in row:
            if isinstance(cell, set) and len(cell) == 0:
                raise ValueError("Cell has no candidates!")
    
    # Check for any rows which have the same singleton repeatedly
    for row in grid:
        digits = set((1,2,3,4,5,6,7,8,9))
        singletons = [cell for cell in row if isinstance(cell, int)]
        for cell in singletons:
            try:
                digits.remove(cell)
            except KeyError:
                raise ValueError("Digit {0} seen more than once".format(cell))

def to_columns(grid):
    """Return a list of columns for the grid"""
    cols = []
    for _ in range(9):
        cols.append([])
    for row in grid:
        for colnum, cell in enumerate(row):
            cols[colnum].append(cell)
    return cols

def to_squares(grid):
    """Return a list of squares for the grid"""
    squares = []
    for _ in range(9):
        squares.append([])
    for rownum, row in enumerate(grid):
        for colnum, cell in enumerate(row):
            squareno = colnum // 3 + (rownum // 3) * 3
            squares[squareno].append(cell)
    return squares

def to_string(grid):
    """Given a grid, return a string with the known chars"""
    chars = []
    for row in grid:
        for cell in row:
            if isinstance(cell, int):
                chars.append(str(cell))
            else:
                chars.append(' ')
        chars.append('\n')
    return ''.join(chars)

def prune_cells(grid):
    """Given a grid, scan each row for solved cells, and remove those
    numbers from every other cell in the row.
    
    Note that 'grid' can be an iterable of rows, columns, or 3x3 squares.
    Since the component cells (sets) are modified in-place it still works
    if you rearrange things.
    
    Return True or False depending on whether any pruning was done.
    """
    changes = False
    for row in grid:
        singletons = [cell for cell in row if isinstance(cell, int)]
        for key in singletons:
            prunable = [cell for cell in row if isinstance(cell, set) and key in cell]
            for cell in prunable:
                cell.remove(key)
                changes = True
    return changes

def repeat_prunes(grid):
    """
    Repeatedly prune candidates from unknown cells using the known cells.
    """
    while True:
        changes = prune_cells(grid)
        changes |= prune_cells(to_columns(grid))
        changes |= prune_cells(to_squares(grid))
        canonicalise(grid)
        validate(grid)
        validate(to_columns(grid))
        validate(to_squares(grid))
        if changes:
            logging.debug("Pruning...")
        elif is_solved(grid):
            logging.info("Solved!")
            logging.info(to_string(grid))
            return True
        else:
            logging.debug("I'm out of ideas. Grid is:")
            logging.debug(to_string(grid))
            return False

def solve(grid):
    """Call repeat_prunes(), then if the grid isn't solved
    guess a cell and recurse.
    
    Note that solving is done in-place on the grid. A return
    value of True indicates success, False indicates an
    unsolveable grid.
    """
    if isinstance(grid, basestring):
        grid = initialise(grid)
    
    try:
        solved = repeat_prunes(grid)
    except ValueError:
        # Well, this was an impossible solution
        return False
    if solved:
        # Trivially solveable, hooray
        return True
    
    # If not trivially solvable, iterate over some possibilities
    logging.debug("Guessing a cell...")
    best_candidate = '9'*10
    x, y = None, None
    for rownum, row in enumerate(grid):
        for colnum, cell in enumerate(row):
            if isinstance(cell, set) and len(cell) < len(best_candidate):
                best_candidate = cell
                x, y = rownum, colnum
    logging.debug("Best cell is ({0},{1})".format(x, y), best_candidate)
    for candidate in best_candidate:
        logging.debug("Guessing", candidate)
        subgrid = deepcopy(grid)
        subgrid[x][y] = candidate
        if solve(subgrid):
            # Hooray, we've solved it!
            # Update the primary grid in-place
            for rownum, row in enumerate(subgrid):
                for colnum, cell in enumerate(row):
                    grid[rownum][colnum] = cell
            return True
        else:
            logging.debug("Bad guess, will try something else")
    
    # Oh god how did we end up here??
    logging.debug("All my guesses were unsolveable")
    return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import fileinput
    GRID = "".join(fileinput.input())
    solve(GRID)
