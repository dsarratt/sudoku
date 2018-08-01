from __future__ import print_function

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

def prune_columns(grid):
    """Given a grid, scan each column for solved cells, and remove those
    numbers from every other cell in the column.
    
    Return True or False depending on whether any pruning was done.
    """
    cols = to_cols(grid)
    return prune_cells(cols)

def prune_cells(grid):
    """Given a grid, scan each row for solved cells, and remove those
    numbers from every other cell in the row.
    
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


def solve(grid):
    """Naive solver, won't make guesses"""
    while True:
        changes = prune_cells(grid)
        changes |= prune_cells(to_columns(grid))
        changes |= prune_cells(to_squares(grid))
        canonicalise(grid)
        validate(grid)
        if changes:
            print("Pruning...")
        elif is_solved(grid):
            print("Solved!")
            print(to_string(grid))
            return True
        else:
            print("I'm out of ideas. Grid is:")
            print(to_string(grid))
            return False
