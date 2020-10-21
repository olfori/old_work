'''Testing all modules and app'''
import time

from config import GameConfig
from quest_modules.game import Game

g = Game(GameConfig())


def mb_test():
    print(g.master.sig['count'])
    for i in range(10):
        g.master.get_sig()
        print(g.master.sig['str'])
        time.sleep(1)
    g.master.get_bps()
    print(g.master.bps['str'])


def csv_create():
    g.stat.c_w.create_csv()


def test_set_bps():
    for i in range(26):
        g.master.set_one_bps(i)
        g.master.get_bps()
        bps = g.master.bps['str']
        print(bps)
        time.sleep(1)


if __name__ == '__main__':
    csv_create()
