from __future__ import print_function

def initialise(gridstring):
    """Take a string-format grid and return a 2D array of sets
    
    Coords are Y,X (row, then col)
    """
    # Validate the string
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
