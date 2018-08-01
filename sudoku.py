from __future__ import print_function

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
        grid.append([set() for _ in range(9)])
    
    # Set numbers
    for rownum, row in enumerate(gridstring.split('\n')):
        if rownum > 8:
            # Ignore extra lines
            break
        elif len(row) != 9:
            raise ValueError("row {0} is not 9 chars".format(rownum))
        
        for colnum, cell in enumerate(row):
            try:
                grid[rownum][colnum] = set([int(cell)])
            except ValueError:
                grid[rownum][colnum] = set(range(1, 10))
    
    return grid

def to_string(grid):
    """Given a grid, return a string with the known chars"""
    chars = []
    for row in grid:
        for cell in row:
            if len(cell) == 1:
                chars.append(str(next(iter(cell))))
            else:
                chars.append(' ')
        chars.append('\n')
    return ''.join(chars)

def prune_rows(grid):
    """Given a grid, scan each row for solved cells, and remove those
    numbers from every other set in the row.
    """
    for row in grid:
        for cell in row:
            if len(cell) == 1:
                known = cell.pop()
                [c2.discard(known) for c2 in row]
                cell.add(known)
