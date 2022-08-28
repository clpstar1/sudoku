from argparse import ArgumentParser
from generator import fill, holes
from sudoku import Sudoku
import curses as cu
from interval import Interval
from game import CursorDirection, Game

options = "Controls:\t(n)ew; (q)uit; (c)lear;\n\t\t[0-9]: set cell; [arrows]: move; [+/-]: adjust difficulty"

def new_game(size, difficulty):
    sudoku = Sudoku(size)
    sudoku = fill(sudoku)
    sudoku = holes(sudoku, difficulty)
    game = Game(sudoku, difficulty)
    return game

def available_string(avail):
    return f"Available:\t{avail} \n"

def difficulty_string(diff):
    return f"Difficulty: \t{float(diff) * 100}% holes \n"

def render(game: Game, stdscr: cu.window, cursor = None):
    stdscr.erase()
    stdscr.addstr(game.sudoku_string(cursor))
    stdscr.addstr(available_string(game.available()))
    stdscr.addstr(difficulty_string(str(game.difficulty)))
    stdscr.addstr(options)

def main(stdscr: cu.window):

    size = 9
    difficulty = 0.5

    game = new_game(size, difficulty)

    cu.curs_set(0)
    
    stdscr.nodelay(1)
    render(game, stdscr, " ")

    def wc():
        render(game, stdscr, " ")

    def nc():
        render(game, stdscr)


    iv = Interval(0.25, wc, nc)
    iv.start()

    while True:
        try:
            key = stdscr.getkey()

            if (key == "KEY_UP"):
                game.move(CursorDirection.UP)
            
            elif (key == "KEY_DOWN"):
                game.move(CursorDirection.DOWN)

            elif (key == "KEY_LEFT"):
                game.move(CursorDirection.LEFT)
            
            elif (key == "KEY_RIGHT"):
                game.move(CursorDirection.RIGHT)

            elif (key.lower() == "q"):
                break

            elif (key.lower() == "n"):
                game = new_game(size, game.difficulty)
            
            elif (key.lower() == "c"):
                game.unset()

            elif (key == "+"):
                new_difficulty = (game.difficulty * 10) + 1
                if (new_difficulty >= 10.0): continue
                game = new_game(size, new_difficulty / 10)

            elif (key == "-"):
                new_difficulty = (game.difficulty * 10) - 1
                if (new_difficulty == 0.0): continue
                game = new_game(size, new_difficulty/10)

            elif (key in game.NUMBER_KEYS):
                game.set(key)
                if game.check_win() == True:
                    break

        except:
            pass
    
    iv.stop()
    cu.endwin()


if __name__ == "__main__":
    cu.wrapper(main)
    
    