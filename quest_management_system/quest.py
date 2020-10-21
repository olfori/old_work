'''start whole app'''
import sys

from app import app
from config import GameConfig
from quest_modules.game import Game


app.game = Game(GameConfig())

if __name__ == "__main__":
    arg = sys.argv          # get the command line arguments
    if len(arg) > 1:        # if ip written in the command line
        app.run(host=str(sys.argv[1]), debug=True)  # '192.168.31.174' - home
    else:
        app.run()
