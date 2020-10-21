'''Quest management system config file'''

from os import path
import json

BASE_DIR = path.abspath(path.dirname(__file__)) # Корневая директория квеста

CONTENT_NAME = path.join(BASE_DIR, 'content.json')
with open(CONTENT_NAME) as json_file:
    S_CONTENT = json.load(json_file)            # read json file with the content

# if true => last 3 BPS is number of Players (bps_count += 3)
LAST_3BPS_PLAYERS = 0

SIG_COUNT = 48                                  # число сигналов в квесте
BPS_COUNT = 13 + int(LAST_3BPS_PLAYERS) * 3     # число байпасов
TIME_TOTAL = 3600                               # время одной игры
SIG_START_FROM_1 = 0                            # отсчет сигналов с 0 или 1


class GameConfig:
    '''Game configuration'''
    game = {
        'LAST_SIGNAL': SIG_COUNT - 1,           # номер последнего синала
        'LAST_3BPS_PLAYERS': LAST_3BPS_PLAYERS  # 1 => последн 3 сигн = число игроков
    }

    timer = {
        'TIME': TIME_TOTAL      # game time 1 hour = 3600 seconds
    }

    modbus = {
        'PORT': '/dev/ttyUSB0', # ttyACM0 ! имя порта, подключенного к ТЯ
        'Q_NUM': 1,             # quest number = modbus slave num (1)

        # signals uint16_t count in data[] 0..4 (count = 5)
        'SIG_2B_COUNT': 5,
        # bypasses uint16_t count in data[] 5, 6 (count = 2)
        'BPS_2B_COUNT': 2,

        'SIG_COUNT': SIG_COUNT,  # signals count in this quest
        'BPS_COUNT': BPS_COUNT,  # bypasses count in this quest

        'RESET_ONE_BPS': 0      # if 0 - reset all BPS, if > 0 reset only one BPS
    }

    stat = {                    # columns for statistics .csv file
        'SIG_START_FROM_1': SIG_START_FROM_1,

        'COLUMNS': [            # назв колонок для записи в файл статистики
            'Game id', 'Game date', 'Start time',
            'Players', 'Play time',
            'El 1 time', 'El 1 hints',
            'El 2 time', 'El 2 hints',
            'El 4 time', 'El 4 hints',
            'El 5 time', 'El 5 hints',
            'El 8 time', 'El 8 hints',
            'El 9 time', 'El 9 hints',
            'El 11 time', 'El 11 hints',
            'El 12 time', 'El 12 hints',
            'El 14 time', 'El 14 hints',
            'El 15 time', 'El 15 hints',
            'El 17 time', 'El 17 hints',
            'El 18 time', 'El 18 hints'
        ],

        'START_END_SIG': {      # statistics calculation
            1: [0, 1],          # 1_Boxes. element_num: [sig_start, sig_stop]
            2: [1, 5],          # 2(3)_Circles
            4: [5, 11],         # 4(5)_Eyes
            5: [11, 14],        # 5(6)_Cat
            8: [14, 20],        # 8(9)_Equalizer
            9: [20, 27],        # 9(11)_Buttons
            11: [27, 28],       # 11(12)_Scull
            12: [28, 32],       # 12(13)_Man_Door
            14: [32, 47],       # 14_Light
            15: [47, 36],       # 15(16)_Bugs
            17: [36, 43],       # 17_Candles
            18: [43, 45]        # 18_Stick
        }
    }

    sound = {
        'START_SIG': SIG_START_FROM_1,       # start signal number

        'SIG_COUNT': SIG_COUNT,

        'FLAGS': {           # signal number: state
            0: 1,            # always 1,
            1: 0,
            5: 0,
            11: 0,
            14: 0,
            20: 0,
            27: 0,
            28: 0,
            32: 0,
            47: 0,
            36: 0,
            43: 0,
            45: 0
        },

        'SIG_TASK': {                   # signal number: sound, background
            # Sig_0 = “Start” btn pressed, quest run
            0: ['tr0.wav', 'bg1.mp3'],      # Start sound
            1: ['tr1.wav', 'bg1.mp3'],      # after 1_Boxes
            5: ['tr2.wav', 'bg2.mp3'],      # after 2(3)_Circles,  D1

            11: ['tr4.wav', 'bg2.mp3'],     # after 4(5)_Eyes
            14: ['tr5.wav', 'bg3.mp3'],     # after 5(6)_Cat,      D2

            20: ['tr8.wav', 'bg3.mp3'],     # after 8(9)_Equalizer
            27: ['tr9.wav', 'bg3.mp3'],     # after 9(11)_Buttons, D3
            28: ['tr11.wav', 'bg3.mp3'],    # after 11(12)_Scull
            32: ['tr12.wav', 'bg4.mp3'],    # after 12(13)_Man_Door,D4

            47: ['tr14.wav', 'bg4.mp3'],    # after 14_Light
            36: ['tr15.wav', 'bg5.mp3'],    # after 15(16)_Bugs,    D5

            43: ['tr17.wav', 'bg6.mp3'],    # after 17_Candles
            45: ['tr18.wav', 'quiet.mp3']   # after 18_Stick,   D6
        },

        'HINTS': {   # element number: hint file name
            '1_1': 'h1_1.wav', '1_2': 'h1_2.wav', '1_3': 'h1_3.wav',    # 1_Boxes
            '2_1': 'h2_1.wav', '2_2': 'h2_2.wav', '2_3': 'h2_3.wav',    # 2(3)_Circles
            '4_1': 'h4_1.wav', '4_2': 'h4_2.wav', '4_3': 'h4_3.wav',    # 4(5)_Eyes
            '5_1': 'h5_1.wav', '5_2': 'h5_2.wav', '5_3': 'h5_3.wav',    # 5(6)_Cat
            '8_1': 'h8_1.wav', '8_2': 'h8_2.wav', '8_3': 'h8_3.wav',    # 8(9)_Equalizer
            '9_1': 'h9_1.wav', '9_2': 'h9_2.wav', '9_3': 'h9_3.wav',    # 9(11)_Buttons
            '11_1': 'h11_1.wav', '11_2': 'h11_2.wav', '11_3': 'h11_3.wav',  # 11(12)_Scull
            '12_1': 'h12_1.wav', '12_2': 'h12_2.wav', '12_3': 'h12_3.wav',  # 12(13)_Man_Door
            '14_1': 'h14_1.wav', '14_2': 'h14_2.wav', '14_3': 'h14_3.wav',  # 14_Light
            '15_1': 'h15_1.wav', '15_2': 'h15_2.wav', '15_3': 'h15_3.wav',  # 15(16)_Bugs
            '17_1': 'h17_1.wav', '17_2': 'h17_2.wav', '17_3': 'h17_3.wav',  # 17_Candles
            '18_1': 'h18_1.wav', '18_2': 'h18_2.wav', '18_3': 'h18_3.wav',  # 18_Stick

            '101_0': 'h101.wav',  # global hint "no force"
            '102_0': 'h102.wav',  # global hint "be careful"
            '103_0': 'h103.wav',  # global hint "no contact"
            '104_0': 'h104.wav',  # global hint "stop"
            '105_0': 'h105.wav'   # global hint "answe"
        }
    }


class AppConfig:
    '''Application configuration'''

    CONTENT = S_CONTENT

    SECRET_KEY = 'foppeopp4657'

    JS_SETTINGS = {     # Данные для отправки в JS (передаются в браузер)
        'SIG_COUNT': SIG_COUNT,
        'BPS_COUNT': BPS_COUNT,
        'TIME_TOTAL': TIME_TOTAL,
        'SIG_START_FROM_1': SIG_START_FROM_1,
        'PB_SIG': '1,5,11,14,20,27,28,32,47,36,43,45'
                                            # сигналы для прогресс бара
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        path.join(BASE_DIR, 'db.sqlite')    # где лежит файл БД sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # откл систему уведомлений о событиях
