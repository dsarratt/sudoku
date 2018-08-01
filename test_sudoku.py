"""Test cases for sudoku"""

import unittest

import sudoku

TESTGRID = """
24   8   
    147  
91  73  2
16   75  
 2 145 8 
  43   71
8  72  13
  183    
   4   67
"""

class InitialiseTest(unittest.TestCase):
    def test_init(self):
        grid = sudoku.initialise(TESTGRID)
        expected = list()
        for rowstring in TESTGRID.strip('\n').split('\n'):
            row = []
            expected.append(row)
            for cell in rowstring:
                if cell.isdigit():
                    row.append(set([int(cell)]))
                else:
                    row.append(set((1,2,3,4,5,6,7,8,9)))
        
        self.assertEqual(grid, expected)
        self.assertEqual(sudoku.to_string(grid).strip('\n'), TESTGRID.strip('\n'))

class PruneTest(unittest.TestCase):
    def test_row_prune(self):
        testgrid = '\n'.join((
            "12345678 ",
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            ))
        grid = sudoku.initialise(testgrid)
        self.assertEqual(grid[0],
            [set([1]), set([2]), set([3]), set([4]), set([5]), set([6]), set([7]), set([8]), set([1,2,3,4,5,6,7,8,9])])
        self.assertTrue(sudoku.prune_rows(grid))
        self.assertEqual(grid[0],
            [set([1]), set([2]), set([3]), set([4]), set([5]), set([6]), set([7]), set([8]), set([9])])
        
    def test_row_2(self):
        testgrid = '\n'.join((
            "1        ",
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            " "*9,
            ))
        grid = sudoku.initialise(testgrid)
        firstrow = [set([1])]
        for _ in range(8):
            firstrow.append(set([1,2,3,4,5,6,7,8,9]))
        self.assertEqual(grid[0], firstrow)
        
        self.assertTrue(sudoku.prune_rows(grid))
        firstrow = [set([1])]
        for _ in range(8):
            firstrow.append(set([2,3,4,5,6,7,8,9]))
        self.assertEqual(grid[0], firstrow)
        
        # Repeat prunings should be harmless
        self.assertFalse(sudoku.prune_rows(grid))
        sudoku.prune_rows(grid)
        sudoku.prune_rows(grid)
        self.assertEqual(grid[0], firstrow)
