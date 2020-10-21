'''Main game module '''
import time
import threading

from .modbus import ModbusMaster
from .timer import Timer
from .statistics.stat import Statistics
from .sound.sound import Sound


class Game:
    '''class provides methods for control the game'''

    def __init__(self, config):
        self.play = 0
        self.allow_cycle = 1
        self.data = {}
        self.config = config.game

        self.sound = Sound(config.sound)
        self.master = ModbusMaster(config.modbus)
        self.timer = Timer(config.timer)
        self.stat = Statistics(config.stat)
        
        game_thread = threading.Thread(target=self.cycle)
        game_thread.start()

    def cycle(self):
        '''Main game cycle for modbus communication'''
        while 1:
            if self.allow_cycle:
                self.master.get_sig()
                sig = self.master.sig['str']

                if self.play:
                    self.sound.read_signals(sig)

                self.stat.processing(sig, self.timer.data)
                self.master.get_bps()
                self.master.set_bps()
                self.master.check_restart()
            time.sleep(0.3)

    def start(self):
        '''start the game'''
        print('quest start')
        self.play = 1

        self.timer.start()
        self.sound.start()
        self.stat.start()

        self.master.set_sig_0(1)

    def stop(self):
        '''stop the game'''
        print('quest stop')
        self.play = 0

        self.master.set_sig_0(0)
        self.master.reset_all_sig()

        self.sound.stop()
        self.timer.stop()
        self.stat.stop()

    def reset(self):
        '''Reset the tech box'''
        self.master.allow_restart()

    def processing(self, data):
        '''processing data from the client'''
        self.allow_cycle = 0
        # set lang: '', 'en', 'de', 'ru'
        if data['set_lang'] in ['en', 'de']:
            self.sound.lang = data['set_lang']
        # get sig str from modbus.py
        sig = self.master.sig['str']
        # get the current bypass num from Site, and send it to the Arduino
        self.master.set_one_bps(data['bps_cur'])

        if self.play:               # if game playing
            if data['start'] == 0:
                self.stop()         # stop the game
            # Set last 3 BPS in modbus
            if self.config['LAST_3BPS_PLAYERS']:
                self.master.set_players(data['players'])
            # audio_sig=-1 or audio_sig=number_of_signal
            self.sound.audio_sig(data['audio_sig'])
            # hints processing
            self.sound.play_hint(data['hint_num'])
            self.stat.get_hint(data['hint_num'])
            # saving statistics
            self.stat.get_game_id(data['game_id'])
            self.stat.get_players(data['players'])
        else:                       # if game stopped
            if data['game_reset']:
                self.reset()
            if data['start'] == 1:  # -1, 0 (stop), 1 (start)
                self.start()        # game start
                # save statistics ID, when start
                self.stat.get_game_id(data['game_id'])
                # send players count to the TechBox when start
                if self.config['LAST_3BPS_PLAYERS']:
                    self.master.set_players(data['players'])

        self.master.tech_box = 'success'

        if not self.master.connected:
            self.master.tech_box = 'danger'

        self.data = {
            'sig': sig,
            'bps': self.master.bps['str_tb'],
            'timer': self.timer.data,
            'tech_box': self.master.tech_box,
            'play': self.play,
            'lang': self.sound.lang,
            'hint_playing': self.sound.hint_playing,
            'testing': self.stat.testing,
            'sound_task': self.sound.send_task
        }
        self.allow_cycle = 1
