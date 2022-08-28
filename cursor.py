from sudoku import Sudoku


class SudokuCursor: 

    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.sudoku_size = sudoku.size()
        self.row = 0 
        self.col = 0

    def hasNext(self) -> bool:
        if self.row == self.sudoku_size-1: return self.col < self.sudoku_size-1
        if self.col == self.sudoku_size-1: return self.row < self.sudoku_size-1
        return True 

    def hasPrev(self) -> bool:
        if self.row == 0: return self.col > 0
        if self.col == 0: return self.row > 0
        return True

    def next(self) -> None:
        # end reached 
        if (
            self.row == self.sudoku_size and 
            self.col == self.sudoku_size
        ): raise Exception("Error: next: no next element")
        # new row 
        if self.col == self.sudoku_size-1:
            self.row += 1
            self.col = 0
        else: 
            self.col += 1
    
    def prev(self) -> None: 
        if (
            self.row == 0 and 
            self.col == 0
        ): raise Exception("Error: prev: no previous element")

        if self.col == 0: 
            self.row -= 1
            self.col = self.sudoku_size-1
        else: 
            self.col -= 1

    def up(self) -> None:
        self.row = (self.row - 1) % self.sudoku_size

    def down(self) -> None:
        self.row = (self.row + 1) % self.sudoku_size
    
    def left(self) -> None:
        self.col = (self.col - 1) % self.sudoku_size

    def right(self) -> None:
        self.col = (self.col + 1) % self.sudoku_size