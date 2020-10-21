'''Timer work with threading'''
import threading


class Timer:
    '''Class for timer'''

    def __init__(self, config):
        self.data = {
            'started': 0,
            'time': config['TIME'],
            'str': '',
            'total': config['TIME']
        }
        self.run()          # run timer at start

    def set_str(self):
        '''set the timer string'''
        sec = self.data['time']
        m = int(abs(sec/60))
        s = sec % 60
        p = ' '
        if not s % 2:
            p = ':'
        self.data['str'] = '{0:0=2}{1}{2:0=2}'.format(m, p, s)

    def run(self):
        '''if timer started, timer count -1 sec'''

        if self.data['started'] and self.data['time'] > 0:
            self.data['time'] -= 1

        self.set_str()

        threading.Timer(1.0, self.run).start()

    def start(self):
        '''start timer and reset time'''
        self.data['started'] = 1
        self.data['time'] = self.data['total']

    def stop(self):
        '''stop timer, no reset'''
        self.data['started'] = 0
