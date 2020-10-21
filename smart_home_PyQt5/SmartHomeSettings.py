DEBUG = False
CV2_ON = True
CURSOR_ON = False
GPO_ON = True

SIG_OUT = 25        # Выход 
BYPASS_1 = 12       # Вход
BYPASS_2 = 16       # Вход
SIG_OUT_CAMERA_1 = 26 # pin 37 
SIG_OUT_CAMERA_2 = 6  # pin 31

LIGHT_ROOM_STATE = [0,0,1,1,0,0,0]
VENT_ROOM_STATE =  [1,0,0,0,0,0,0]
ELEC_ROOM_STATE =  [-1,-1,0,-1,0,0,0]  # переименовано в Доступ
DOOR_ROOM_STATE =  [0,0,1,0,0,0,1]
SIGN_ROOM_STATE =  [-1,-1,0,-1,0,0,0]  # переименовано в Видеонаблюдение
TEMP_ROOM_STATE = [21,22,20,20,22,21,16]

# StyleSheet для мал. кнопок вкл. выкл. и назад
BTN_MID_SS = 'background-color: transparent; background-image: url(btnMid.png); font: 16pt;'
BTN_ON_SS = 'background-color: transparent; background-image: url(btnWhite.png); font: 16pt;'
BTN_OFF_SS = 'background-color: transparent; background-image: url(btnRed.png); font: 16pt;'


BIG_BTNS_NAME_RU = ['Свет',             #0
                    'Вентиляция',       #1
                    'Доступ',           #2
                    'Двери',            #3
                    'Видеонаблюд.',     #4
                    'Температура']      #5

BIG_BTNS_NAME_EN = ['Light', 
                    'Ventilation', 
                    'Access', 
                    'Doors', 
                    'CCTV', 
                    'Temperature']
                    
BIG_BTNS_ACTIVE =   [ 0, 0, 1, 0, 1, 0]

LINE_ROOMS_NAME_RU = [  'Кладовая', 
                        'Чердак', 
                        'Разделочная', 
                        'Подвал']
                    
LINE_ROOMS_NAME_EN = [  'Pantry', 
                        'Attic', 
                        'Cutting', 
                        'Basement']