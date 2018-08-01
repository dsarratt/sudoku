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

class CanonicaliseTest(unittest.TestCase):
    def test_canonicalise(self):
        grid = [[1, 2, 3, set((4,5)), set((4,5)), set((6,7,8)), set((6,7,8)), set((6,7,8)), set((9,))]]
        sudoku.canonicalise(grid)
        self.assertEqual(grid,
            [[1, 2, 3, set((4,5)), set((4,5)), set((6,7,8)), set((6,7,8)), set((6,7,8)), 9]])

class InitialiseTest(unittest.TestCase):
    def test_init(self):
        grid = sudoku.initialise(TESTGRID)
        expected = list()
        for rowstring in TESTGRID.strip('\n').split('\n'):
            row = []
            expected.append(row)
            for cell in rowstring:
                if cell.isdigit():
                    row.append(int(cell))
                else:
                    row.append(set((1,2,3,4,5,6,7,8,9)))
        
        self.assertEqual(grid, expected)
        self.assertEqual(sudoku.to_string(grid).strip('\n'), TESTGRID.strip('\n'))
    
    def test_init_full(self):
        gridstring = "123456789\n"*9
        grid = sudoku.initialise(gridstring)
        for row in grid:
            self.assertEqual(row, [1,2,3,4,5,6,7,8,9])

class ValidateTest(unittest.TestCase):
    """Test validation"""
    def test_no_candidates(self):
        """If a cell has no candidates, the puzzle is malformed"""
        grid = [[1, 2, 3, set((4,5)), set((4,5)), set((6,7,8)), set((6,7,8)), set((6,7,8)), set((9,))]]
        self.assertIsNone(sudoku.validate(grid))
        
        grid[0][-1] = set()
        with self.assertRaises(ValueError):
            sudoku.validate(grid)
    
    def test_ok(self):
        """Test a grid with conflicting cells"""
        grid = [[1, 2, 3, set((4,5)), set((4,5)), set((6,7,8)), set((6,7,8)), set((6,7,8)), set((8, 9))]]
        self.assertIsNone(sudoku.validate(grid))
        
        grid[0][-1] = 9
        self.assertIsNone(sudoku.validate(grid))
        
        grid[0][-1] = 1
        with self.assertRaises(ValueError):
            sudoku.validate(grid)

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
        self.assertEqual(grid[0], [1,2,3,4,5,6,7,8, set([1,2,3,4,5,6,7,8,9])])
        self.assertTrue(sudoku.prune_cells(grid))
        # Note that the grid hasn't been canonicalised yet
        self.assertEqual(grid[0], [1,2,3,4,5,6,7,8, set([9])])
    
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
        firstrow = [1]
        for _ in range(8):
            firstrow.append(set([1,2,3,4,5,6,7,8,9]))
        self.assertEqual(grid[0], firstrow)
        
        self.assertTrue(sudoku.prune_cells(grid))
        firstrow = [1]
        for _ in range(8):
            firstrow.append(set([2,3,4,5,6,7,8,9]))
        self.assertEqual(grid[0], firstrow)
        
        # Repeat prunings should be harmless
        self.assertFalse(sudoku.prune_cells(grid))
        sudoku.prune_cells(grid)
        sudoku.prune_cells(grid)
        self.assertEqual(grid[0], firstrow)

class TransformTests(unittest.TestCase):
    """Test the transformations to columns or squares"""
    def test_columns(self):
        testgrid = '\n'.join((
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            ))
        grid = sudoku.initialise(testgrid)
        cols = sudoku.to_columns(grid)
        self.assertEqual(cols[0], [1]*9)
        self.assertEqual(cols[4], [5]*9)
        self.assertEqual(cols[8], [9]*9)
    
    def test_squares(self):
        testgrid = '\n'.join((
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            ))
        grid = sudoku.initialise(testgrid)
        squares = sudoku.to_squares(grid)
        self.assertEqual(squares[0], [1,2,3,1,2,3,1,2,3])
        self.assertEqual(squares[8], [7,8,9,7,8,9,7,8,9])
        
        testgrid = '\n'.join((
            "111222333",
            "111222333",
            "111222333",
            "444555666",
            "444555666",
            "444555666",
            "777888999",
            "777888999",
            "777888999",
            ))
        grid = sudoku.initialise(testgrid)
        squares = sudoku.to_squares(grid)
        self.assertEqual(squares[0], [1]*9)
        self.assertEqual(squares[5], [6]*9)
        self.assertEqual(squares[8], [9]*9)

class SolverTest(unittest.TestCase):
    """Tricky puzzles to prove recursive solving works"""
    def test_1611984609(self):
        """http://www.websudoku.com/?level=4&set_id=1611984609"""
        testgrid = '\n'.join((
            "5   4 8  ",
            "   7     ",
            "63  82 1 ",
            "  1   2 9",
            "  6   5  ",
            "9 7   3  ",
            " 4 15  27",
            "     7   ",
            "  5 9   4",
            ))
        grid = sudoku.initialise(testgrid)
        self.assertTrue(sudoku.solve(grid))
        self.assertEqual(grid, [
            [5,7,2,6,4,1,8,9,3],
            [1,9,8,7,3,5,4,6,2],
            [6,3,4,9,8,2,7,1,5],
            [3,5,1,8,7,6,2,4,9],
            [4,8,6,3,2,9,5,7,1],
            [9,2,7,5,1,4,3,8,6],
            [8,4,9,1,5,3,6,2,7],
            [2,1,3,4,6,7,9,5,8],
            [7,6,5,2,9,8,1,3,4],
            ])
    
    def test_escargot(self):
        """https://www.kristanix.com/sudokuepic/worlds-hardest-sudoku.php"""
        testgrid = '\n'.join((
            "1    7 9 ",
            " 3  2   8",
            "  96  5  ",
            "  53  9  ",
            " 1  8   2",
            "6    4   ",
            "3      1 ",
            " 4      7",
            "  7   3  ",
            ))
        grid = sudoku.initialise(testgrid)
        self.assertTrue(sudoku.solve(grid))
        self.assertEqual(grid, [
            [1,6,2,8,5,7,4,9,3],
            [5,3,4,1,2,9,6,7,8],
            [7,8,9,6,4,3,5,2,1],
            [4,7,5,3,1,2,9,8,6],
            [9,1,3,5,8,6,7,4,2],
            [6,2,8,7,9,4,1,3,5],
            [3,5,6,4,7,8,2,1,9],
            [2,4,1,9,3,5,8,6,7],
            [8,9,7,2,6,1,3,5,4],
            ])
    
    def test_inkala(self):
        """https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html"""
        testgrid = '\n'.join((
            "8        ",
            "  36     ",
            " 7  9 2  ",
            " 5   7   ",
            "    457  ",
            "   1   3 ",
            "  1    68",
            "  85   1 ",
            " 9    4  ",
            ))
        grid = sudoku.initialise(testgrid)
        self.assertTrue(sudoku.solve(grid))
        self.assertEqual(grid, [
            [8,2,5,7,1,3,6,9,4],
            [9,4,3,6,5,2,8,7,1],
            [1,7,6,4,9,8,2,5,3],
            [3,5,2,9,8,7,1,4,6],
            [6,1,9,3,4,5,7,8,2],
            [7,8,4,1,2,6,9,3,5],
            [4,3,1,2,7,9,5,6,8],
            [2,6,8,5,7,4,3,1,9],
            [5,9,6,8,3,1,4,2,7],
            ])
