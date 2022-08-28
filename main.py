from generator import fill, holes
from printer import print_sudoku
from argparse import ArgumentParser
from sudoku import Sudoku

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("size")

    args = parser.parse_args()

    size = int(args.size or 9)

    sudoku = Sudoku(size)

    sudoku = fill(sudoku)
    sudoku = holes(sudoku, 0.5)

    print_sudoku(sudoku)