from typing import List, Tuple
sudoku_grid = []


# Maybe do a global variable for the solutions


sudoku_board = [
    [5, 3, ".", ".", 7, ".", ".", ".", "."],
    [6, ".", ".", 1, 9, 5, ".", ".", "."],
    [".", 9, 8, ".", ".", ".", ".", 6, "."],
    [8, ".", ".", ".", 6, ".", ".", ".", 3],
    [4, ".", ".", 8, ".", 3, ".", ".", 1],
    [7, ".", ".", ".", 2, ".", ".", ".", 6],
    [".", 6, ".", ".", ".", ".", 2, 8, "."],
    [".", ".", ".", 4, 1, 9, ".", ".", 5],
    [".", ".", ".", ".", 8, ".", ".", 7, 9]
]


sudoku_multiple_solutions = [
    [4, 1, 3, 6, 7, 8, ".", ".", 9],
    [6, 8, 2, 9, 3, 5, 7, 4, 1],
    [7, 5, 9, 4, 2, 1, 6, 3, 8],

    [3, 9, 4, ".", 1, 6, 8, ".", "."],
    [1, 7, 5, 8, 9, 2, 4, 6, 3],
    [8, 2, 6, ".", 4, ".", 9, 1, "."],

    [9, 3, 7, 1, 6, 4, ".", 8, "."],
    [5, 6, 1, 2, 8, ".", 3, ".", 4],
    [2, 4, 8, ".", 5, ".", 1, ".", 6]
]

sudoku_jane_street = [
    [".", ".", ".",  ".", "2", ".",  ".", ".", "5"],
    [".", ".", ".",  ".", ".", ".",  ".", "2", "."],
    [".", "2", ".",  ".", ".", ".",  ".", ".", "."],

    [".", ".", "0",  ".", ".", ".",  ".", ".", "."],
    [".", ".", ".",  ".", ".", ".",  ".", ".", "."],
    [".", ".", ".",  "2", ".", ".",  ".", ".", "."],

    [".", ".", ".",  ".", "0", ".",  ".", ".", "."],
    [".", ".", ".",  ".", ".", "2",  ".", ".", "."],
    [".", ".", ".",  ".", ".", ".",  "5", ".", "."],
]


def print_grid(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            print(val, end=" ")
            if c % 3 == 2 and c != 8:
                print("|", end=" ")
        if r % 3 == 2 and r != 8:
            print("\n" + "-" * 21)
        else:
            print()

def find_empty_cell(grid) -> tuple[int, int]:
    """
        Find the first empty cell in the grid.
        Going up to down, left to right
        (row by row, left to right.)
    """
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == ".":
                return r, c
    return None


def is_valid(grid, r, c, num, biggest_gcd) -> bool:
    """
        Check if we can place num at grid[r][c]
    """
    # First, check if num is in the row
    for cc in range(9):
        if grid[r][cc] == num: return False
    # Check if num is in the column
    for rr in range(9): 
        if grid[rr][c] == num: return False
    # Check the 3x3 subgrids.
    start_r, start_c = (r // 3) * 3, (c // 3) * 3
    # Loop over every value in the subgrid 
    # and check if it is equal to the 
    # element we want to add to it.
    for rr in range(start_r, start_r + 3):
        for cc in range(start_c, start_c + 3):
            if grid[rr][cc] == num: return False
    
    if c == 8:
        # Compute the gcd of the grid of the 
        # full rows so far
        grid[r][c] = num
        gcd = grid_gcd(grid, r)
        grid[r][c] = "."
        if gcd <= biggest_gcd or gcd < 1000:
            return False
    
    return True 


def find_solution(grid):
    """
        Find a single solution to the sudoku
    """
    # Check if there is an empty cell.
    # If not, we have solved the sudoku
    if find_empty_cell(grid) is None:
        print_grid(grid)
        return True
    # We need to find the first empty cell
    empty_r, empty_c = find_empty_cell(grid)
    # Try out all the possible numbers
    for num in range(1, 10):
        # Check if the number is valid at 
        # this position
        if not is_valid(grid, empty_r, empty_c, num): continue
        # Try it out
        # Fill in the number
        grid[empty_r][empty_c] = num
        if find_solution(grid):
            return True
        # If we reach this point, it means that
        # the number we tried out is not valid
        # so we need to backtrack
        grid[empty_r][empty_c] = "."



def find_gcd(x, y):
    while(y):
        x, y = y, x % y
    return x
     
     
def grid_gcd(grid, rowmax):
    l = []
    for r, row in enumerate(grid):
        if r > rowmax:
            break
        val = int("".join(row))
        l.append(val)
    gcd = l[0]
    for i in range(1,rowmax + 1):
        gcd=find_gcd(gcd,l[i])
    return gcd


def find_solutions(grid, numbers: str, biggest_gcd) -> List[List[List[int]]]:
    """
        Find all possible solutions to the sudoku.
    """
    # Check if there is an empty cell.
    # If not, we have solved the sudoku
    if find_empty_cell(grid) is None:
        gcd = grid_gcd(grid, 8)
        print_grid(grid)
        print(f"Found a solution with gcd: {gcd}")
        return 
    # We need to find the first empty cell
    empty_r, empty_c = find_empty_cell(grid)
    # Try out all the possible numbers
    for num in numbers:
        # Check if the number is valid at 
        # this position
        if not is_valid(grid, empty_r, empty_c, num, biggest_gcd): continue
        # Fill in the number
        grid[empty_r][empty_c] = num
        find_solutions(grid, numbers, biggest_gcd)
        # If we reach this point, it means that
        # the number we tried out is not valid
        # so we need to backtrack
        grid[empty_r][empty_c] = "."


"""
    A hack is to cutoff after the current gcd is smaller than the current highest.

    Unfortunately, this is not fast enough to find the solution.

    Biggest hack: just hack that the answer is > 1000, then basically
    we prune always after the first two rows are filled in.
"""


if __name__ == "__main__":
    # find_solution(sudoku_board)
    # print("Multiple solutions")
    all_numbers = "0123456789"
    # Check for all the possibilities of the sudoku, with 9 numbers.
    # We can choose all except 0, 2, 5
    remove = "1346789"
    for i in remove:
        print(f"\n\nRemoving {i}")
        numbers = all_numbers.replace(i, "")
        assert len(numbers) == 9
        find_solutions(sudoku_jane_street, numbers=numbers, biggest_gcd=float('-inf'))

