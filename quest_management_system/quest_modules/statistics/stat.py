'''statistics game module'''
import csv

from datetime import datetime
from os import path
from .csv_worker import CsvWorker

DIR_NAME = path.join(path.dirname(__file__), 'csv')


class Statistics:
    '''Class provides methods for collecting game statistics'''

    def __init__(self, config):
        self.dir_name = DIR_NAME
        self.config = config

        self.c_w = CsvWorker(config['COLUMNS'], DIR_NAME)

        self.game_stat = {}
        self.el_time = {}

        self.testing = 0
        self.started = ''  # 'run', 'stopped', '':full_stop

    def get_global_stat(self):
        '''read last csv from static/stat/ and return list '''
        return self.c_w.last_csv_read()

    def game_stat_create(self):
        '''Create game statistics dictionary'''
        self.game_stat = dict.fromkeys(self.config['COLUMNS'], 0)
        self.el_time = dict.fromkeys(self.config['START_END_SIG'], [0, 0])

    def csv_save_current_stat(self):
        '''append row in last csv from static/stat/'''
        f_name = self.c_w.last_csv_path()
        with open(f_name, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.config['COLUMNS'])
            writer.writerow(self.game_stat)

    def start(self):
        '''Create statistics when the game started'''
        self.testing = 1
        self.started = 'run'
        self.game_stat_create()

        dt_str = datetime.now().strftime("%d.%m.%Y")
        tm_str = datetime.now().strftime("%H:%M:%S")
        self.game_stat['Game date'] = dt_str
        self.game_stat['Start time'] = tm_str

    def stop(self):
        '''Saving statistics when the game is stopped'''
        self.started = 'stopped'
        print('stat stopped')

    def processing(self, sig, timer_data):
        '''Collect statistics while the game on'''

        if self.started in ['run', 'stopped']:

            for el_num, sig_range in self.config['START_END_SIG'].items():
                column_name = 'El {} time'.format(el_num)

                sig_activate = sig_range[0] - \
                    self.config['SIG_START_FROM_1']
                sig_solved = sig_range[1] - self.config['SIG_START_FROM_1']

                if sig[sig_activate] == '1' and not self.el_time[el_num][0]:
                    # remember the element activation time
                    self.el_time[el_num] = [timer_data['time'], 0]
                #print(sig_solved)
                if sig[sig_solved] == '1' and not self.el_time[el_num][1]:
                    active_time = self.el_time[el_num][0]
                    solved_time = timer_data['time']
                    self.el_time[el_num] = [active_time, solved_time]
                    riddle_solved_time = active_time - solved_time
                    if riddle_solved_time > 0:
                        self.game_stat[column_name] = riddle_solved_time

            if self.started == 'stopped':
                if not self.testing:
                    print('stat ending saved')
                    self.game_stat['Play time'] = timer_data['total'] - \
                        timer_data['time']
                    self.csv_save_current_stat()
                if self.started == 'stopped':
                    self.started = ''
                    self.testing = 0

    def get_hint(self, hint):
        '''get the hint number, count it and write it to the statistics file'''
        if hint != '':
            print('I get hint!')
            hint_num = int(hint.split('_')[0])
            if hint_num and hint_num < 100:
                column_name = 'El {} hints'.format(hint_num)
                if column_name in self.game_stat:
                    self.game_stat[column_name] += 1

    def get_game_id(self, game_id):
        '''If the game_id has been set, then statistics will be saved'''
        if game_id != '':
            self.game_stat['Game id'] = game_id
            self.testing = 0

    def get_players(self, players):
        '''get players from client and set them in game_stat dictionary'''
        if players != '':
            self.game_stat['Players'] = players
