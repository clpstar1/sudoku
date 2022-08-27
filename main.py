from generator import generate_sudoku, add_holes
from printer import print_sudoku
from argparse import ArgumentParser

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("size")

    args = parser.parse_args()

    size = int(args.size)

    sudoku = generate_sudoku(size or 9)
    sudoku = add_holes(sudoku, 0.5)

    print_sudoku(sudoku)