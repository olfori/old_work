'''Modbus connection with the Tech box'''
import time
import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


def b2_to_bits(b2_list):
    '''convert uint16_t list to string of bits'''
    bits_str = ''
    l = len(b2_list)
    for i in range(l):
        bits2 = bin(b2_list[i])[2:].zfill(16)
        reversed_bits = bits2[::-1]
        bits_str += reversed_bits
    return bits_str


def bits_to_b2(bits):
    '''convert string of bits to uint16_t list'''
    b1 = int('0b'+bits[:16][::-1], base=2)
    b2 = 0
    if len(bits) > 16:
        b2 = int('0b'+bits[16:32][::-1], base=2)
    return [b1, b2]


class ModbusMaster:
    '''Class for sending and receiving data to the quest with modbus'''

    def __init__(self, config):
        self.config = config
        self.master = None
        self.tech_box = 'success'
        self.bps = {
            'str': '',              # Bypasses for sending to the Tech Box
            'str_tb': '',           # Bypasses received from the Tech Box
            'count': self.config['BPS_COUNT']
        }
        self.sig = {
            'str': '',
            'count': self.config['SIG_COUNT'],
            0: 0
        }
        self.connected = 0
        self.once_at_start = 1
        self.restart = {
            'counter': 0,
            'state': 0
        }

        self.connect()

    def connect(self):
        '''set connect to the tech box by modbus'''
        try:                                    # Connect to the slave
            self.master = modbus_rtu.RtuMaster(
                serial.Serial(
                    port=self.config['PORT'],
                    baudrate=9600,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    xonxoff=0
                )
            )
            self.master.set_timeout(2.0)
            self.master.set_verbose(False)      # true if verbose needed
            time.sleep(3)                       # Time for restart arduino
            self.connected = 1

        except modbus_tk.modbus.ModbusError as exc:
            print('no connection',exc)
            self.connected = 0

    def set_players(self, players):
        '''set 3 last BPS to binary 1..6'''
        li_bin = ['000', '100', '010', '110', '001', '101', '011']
        if players != '':
            players = int(players)
            if 7 > players > 0:
                l = len(self.bps['str'])
                new_bps_str = self.bps['str'][:l-3] + li_bin[players]
                self.bps['str'] = new_bps_str
                self.set_bps()

    def check_sig_0(self):
        '''if sig 0 == 1, once return 1. Any other case - return 0'''
        if len(self.sig['str']) > 0:
            if self.once_at_start and self.sig['str'][0] == '1':
                self.once_at_start = 0
                return 1

            if not self.once_at_start and self.sig['str'][0] == '0':
                self.once_at_start = 1
        return 0

    def set_sig_0(self, state):
        '''sig 0 - started game'''
        self.sig[0] = int(state)

    def reset_all_sig(self):
        state = 0
        sig_count = self.sig['count']
        self.sig['str'] = '{0:{1}<{2}}'.format('', state, sig_count)

    def allow_restart(self):
        '''allow restarting'''
        self.restart['state'] = 1

    def check_restart(self):
        '''if quest restart - one or all bps on, wait 1 sec, all bps off'''
        if self.restart['state']:
            print(self.bps['str_tb']+' bps restart')
            if not self.restart['counter']:
                r_1 = self.config['RESET_ONE_BPS']
                if r_1:
                    self.set_one_bps(r_1)
                else:
                    self.all_bps(1)
            self.restart['counter'] += 1
            if self.restart['counter'] == 8:
                self.restart['counter'] = 0
                self.restart['state'] = 0
                self.all_bps(0)
                self.set_bps()

    def all_bps(self, state):
        '''all bps on / off, state must be 0 or 1'''
        bps_count = self.bps['count']
        self.bps['str'] = '{0:{1}<{2}}'.format('', state, bps_count)
        # print(self.bps['str']+' all_bps')

    def set_one_bps(self, bps_num):
        '''turn on choosen bps'''
        if 0 < bps_num <= self.config['BPS_COUNT']:
            num = bps_num - 1
            bstart = self.bps['str'][:num]
            bend = self.bps['str'][num+1:]
            if self.bps['str'][num] == '0':
                self.bps['str'] = bstart + '1' + bend
            else:
                self.bps['str'] = bstart + '0' + bend

    def set_bps(self):
        '''send 2 * uint16 (5, 6) to the Arduino'''
        try:
            bps_2b_list = bits_to_b2(self.bps['str'])
            self.master.execute(
                self.config['Q_NUM'],           # quest number
                cst.WRITE_MULTIPLE_REGISTERS,   # modbus command
                5,                              # data[] elem number
                output_value=bps_2b_list
            )
            self.connected = 1
        except modbus_tk.exceptions.ModbusInvalidResponseError as e_m:
            print(e_m)
            self.connected = 0

    def get_sig(self):
        '''read 5 * uint16 (0..4) from Arduino'''
        try:
            b2_li = self.master.execute(
                self.config['Q_NUM'],
                cst.READ_INPUT_REGISTERS,
                0,
                self.config['SIG_2B_COUNT']
            )
            sig_str = b2_to_bits(b2_li)
            sig_str = sig_str[:self.config['SIG_COUNT']]
            if self.sig[0]:
                sig_str = '1' + sig_str[1:]
            self.sig['str'] = sig_str
            self.connected = 1
        except modbus_tk.exceptions.ModbusInvalidResponseError as e_m:
            print(e_m)
            self.connected = 0

    def get_bps(self):
        '''read 2 * uint16 (5, 6) from Arduino'''
        try:
            b2_li = [0, 0]
            b2_li = self.master.execute(
                self.config['Q_NUM'],
                cst.READ_INPUT_REGISTERS,
                5,
                self.config['BPS_2B_COUNT']
            )
            res_str = b2_to_bits(b2_li)
            res_str = res_str[:self.config['BPS_COUNT']]
            self.bps['str_tb'] = res_str
            if self.bps['str'] == '':
                self.bps['str'] = res_str
            self.connected = 1
        except modbus_tk.exceptions.ModbusInvalidResponseError as e_m:
            print(e_m)
            self.connected = 0


if __name__ == '__main__':
    li = bits_to_b2('11000000000000001110000000000000')
    print(li)
