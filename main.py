import curses as cu
from threading import Thread
from game import CursorDirection, Game, Screen

options = "Controls:\t(n)ew; (q)uit; (c)lear;\n\t\t[0-9]: set cell; [arrows]: move; [+/-]: adjust difficulty"

def main(stdscr: cu.window):

    size = 9
    difficulty = 0.5

    


    game = Game.new(size, difficulty)
    screen = Screen(stdscr)

  

    game.addListener(screen)
    game.notify()

    cu.curs_set(0)
    
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
                game.reset()

            elif (key.lower() == "c"):
                game.unset()

            elif (key.lower() == "r"):
                game.reveal()

            elif (key == "+"):
                game.raise_difficulty_by(1)

            elif (key == "-"):
                game.raise_difficulty_by(-1)

            elif (key in game.NUMBER_KEYS):
                game.set(key)
                if game.check_win() == True:
                    break

        except:
            pass
    
    screen.stop()
    cu.endwin()


if __name__ == "__main__":
    cu.wrapper(main)
    
    