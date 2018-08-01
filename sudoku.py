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

def prune_rows(grid):
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


