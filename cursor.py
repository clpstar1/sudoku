from sudoku import Sudoku


class SudokuCursor: 

    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.sudoku_size = sudoku.size()
        self.row = 0 
        self.col = 0

    def hasNext(self) -> bool:
        return self.row < self.sudoku_size and self.col < self.sudoku_size

    def hasPrev(self) -> bool:
        return self.row > 0 and self.col > 0

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