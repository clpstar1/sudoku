from sudoku import Sudoku

def print_sudoku(sudoku: Sudoku):
    sudoku_size = sudoku.size()
    cell_size = sudoku.cell_size

    print_horizontal_border(sudoku)

    for row in range(0, sudoku_size):
        for col in range(0, sudoku_size):
            cell = str(sudoku.get(row, col).value)

            if col == 0:
                print("| " + cell, end=" ")
            
            elif (col+1) % cell_size == 0:
                print(cell + " |", end=" ")
            
            else: print(cell + "", end=" ")
        
        print("")
        if (row+1) % cell_size == 0:
            print_horizontal_border(sudoku)

def print_horizontal_border(sudoku):
    sudoku_size = sudoku.size()
    cell_size = sudoku.cell_size
    print("- " * (sudoku_size + cell_size + 1))
