''' Sound  '''
import time
import threading
from os import path
import pygame

DIR_MP3 = path.join(path.dirname(__file__), 'mp3')


class Sound:
    '''Sound control'''

    def __init__(self, config):
        pygame.mixer.init()
        self.mus = pygame.mixer.music
        self.mus.set_volume(1.0)

        self.config = config

        self.sig_last = ''      # last sig_str. For new sig_num detect
        self.sig_count = config['SIG_COUNT']     # constant

        self.thread_run = 1     # always 1 - allow run play_song thread

        self.new_sig = 0        # 0 or 1=new sig hes been detected

        self.sound_stop = 0     # 0 or 1=can't play sound

        self.lang = 'de'        # 'en', 'de'

        self.task = ['', '']    # 0='song', 1='bg'
        self.send_task = ['', '']  # [0]-sig num, [1]-bg num, while playing

        self.hint_num = ''       # number of playing hint, >0 once
        self.hint_playing = ''   # number of playing hint, >0 while hint playing

        self.bg = {
            'prev_f_name': ''    # имя предыдущего файла
        }

        self.snd = None

        # флаги в словаре - ключ(номер сигнала):значение(этот сиг приходил?)
        self.flag = self.config['FLAGS'].copy()

        threading.Thread(target=self.thread_cycle).start()

    def reset(self):
        '''if reset needed'''
        print('sound reset all')
        self.flag = self.config['FLAGS'].copy()    # reset flags
        self.stop()

    def thread_cycle(self):
        '''Thread cycle, start on init'''
        while self.thread_run:

            if self.new_sig:
                self.play_task()

            if self.hint_num != '':           # if hint needed
                self.play_wav_hint()

            time.sleep(0.05)

    def play_task(self):
        '''play task: 1 track, 1 background'''
        self.new_sig = 0            # reset new_sig for next new_sig reaction

        tr = self.task[0]
        bg = self.task[1]

        if tr != '':                # if task have track
            self.play_track(tr)
            self.task[0] = ''
            self.send_task[0] = ''

        if bg != '':                # if task have background
            if self.sound_stop:
                self.send_task[1] = ''
                return
            if '.' in bg:
                self.send_task[1] = bg.split('.')[0]
                self.play_bg(bg)
        else:                       # если у таска нет bg
            self.mus.stop()
            self.send_task[1] = ''

    def play_track(self, f_name):
        '''Playing track (file name)'''
        if not self.sound_stop:
            dir_lang = path.join(DIR_MP3, self.lang)
            f_name = path.join(dir_lang, f_name)
            print('play_track = ', f_name)
            if self.mus.get_busy():
                self.mus.pause()
            self.snd = pygame.mixer.Sound(f_name)
            snd_len = self.snd.get_length()
            snd_cycles = int(snd_len/0.1)
            self.snd.play()

            for i in range(snd_cycles):
                if self.new_sig:        # if new sig received when playing
                    self.snd.stop()
                    self.play_task()
                if self.hint_num != '':
                    self.snd.stop()
                    self.play_wav_hint()
                time.sleep(0.1)

    def play_bg(self, f_name):
        '''Playing background (file name)'''
        if not self.sound_stop:
            if self.bg['prev_f_name'] != f_name:
                self.bg['prev_f_name'] = f_name
                f_name = path.join(DIR_MP3, f_name)
                print('play_bg = ', f_name)
                self.mus.stop()
                self.mus.load(f_name)
                self.mus.play(-1)
            else:
                print('play_prev_bg = ', f_name)
                self.mus.unpause()

            while self.mus.get_busy():
                if self.new_sig:        # if new sig received when playing
                    self.play_task()
                if self.hint_num != '':
                    self.play_wav_hint()
                continue

    def play_wav_hint(self):
        '''Play sound over the current (only .wav), the current sound is paused'''

        # get the file name in order with hint number
        if self.hint_num in self.config['HINTS']:
            self.task[0] = ''
            self.send_task[0] = ''
            f_name = self.config['HINTS'][self.hint_num]
            self.hint_playing = self.hint_num
            self.hint_num = ''
            dir_lang = path.join(DIR_MP3, self.lang)
            f_name = path.join(dir_lang, f_name)

            print(f_name)

            self.mus.pause()
            self.snd = pygame.mixer.Sound(f_name)
            snd_len = self.snd.get_length()
            self.snd.play(fade_ms=1000)
            time.sleep(snd_len)
            self.mus.unpause()
            self.hint_playing = ''

    def stop(self):
        '''stop playing any sound, reset flags, allow play after 3 sec'''
        
        self.task = ['', '']
        self.send_task = ['', '']
        self.new_sig = 0
        self.sound_stop = 1
        self.sig_last = '0' * self.sig_count
        self.bg['prev_f_name'] = ''

        if self.snd is not None:
            self.snd.stop()
        self.mus.stop()

    def start(self):
        '''start sound, allow playing, play SIG_TASK[0]'''
        self.reset()
        self.sound_stop = 0
        # start playing first song
        self.set_task(self.config['START_SIG'])

    def read_signals(self, sig_str):
        '''What to do, when the current signal is recieved'''
        if not self.sound_stop:
            l = len(sig_str)
            ll = len(self.sig_last)

            if l == ll and l == self.sig_count:

                for i, s in enumerate(sig_str):
                    if s != self.sig_last[i]:           # if this is a new signal
                        sig = i + self.config['START_SIG']
                        if sig in self.flag:            # if sig have sound
                            if self.flag[sig] == 0:     # if sig did not playing yet
                                self.flag[sig] = 1
                                self.set_task(sig)

            self.sig_last = sig_str

    def set_task(self, sig_num):
        '''set task to play. Set send_task variable for send it to the client'''
        if sig_num in self.config['SIG_TASK']:
            self.task = self.config['SIG_TASK'][sig_num].copy()
            self.new_sig = 1
            if self.task[0] != '':
                self.send_task = ['a' + str(sig_num), '']
            else:
                self.send_task = ['', '']

    def audio_sig(self, sig_num):
        '''if sig number > -1, playing one task from SIG_TASK'''
        if sig_num != -1:
            self.set_task(sig_num)

    def play_hint(self, hint_num):
        '''if hint number != 0 pause all and playing current hint'''
        if hint_num != '':
            self.hint_num = hint_num

    def check_sound_files(self):
        '''check existing of all sound files in SIG_TASK and HINT'''
        for sig in self.config['SIG_TASK']:
            for name in self.config['SIG_TASK'][sig]:
                if name != '':
                    f_name = path.join(DIR_MP3, name)
                    if path.exists(f_name):
                        print('file ' + name + ' exist')
                    else:
                        print('ERROR!!!! file ' + name + " doesn't exist")

        for lang in ['en', 'de', 'ru']:
            for hint in self.config['HINTS']:
                name = self.config['HINTS'][hint]
                if name != '':
                    f_name = path.join(DIR_MP3, lang)
                    f_name = path.join(f_name, name)
                    if path.exists(f_name):
                        print('file ' + name + ' exist')
                    else:
                        print('ERROR!!!! file ' + name + " doesn't exist")
