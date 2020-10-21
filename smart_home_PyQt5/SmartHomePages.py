from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial

from SmartHomeSettings import *

if CV2_ON:
    import cv2

from datetime import datetime
from os import path

BIG_BTN_SS = 'background-color: transparent; background-image: url(btn.png); font: 20pt;'
BIG_BTN_SS_OFF = 'background-color: transparent; background-image: url(btnNA.png); font: 20pt;'

# Большие кнопки
class ButtonBig(QPushButton):
    okClicked = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.btn_off = False
        
        self.btn_active = False
        self.setStyleSheet(BIG_BTN_SS)
        self.resize(250,80)
        self.shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=-4, yOffset=4, color=QColor(200, 0, 0, 250))
        
    def mousePressEvent(self, event):
        if not self.btn_off:
            self.show_shaddow()
        
    def mouseReleaseEvent(self, event):
        if not self.btn_off:
            self.hide_shaddow()
            self.okClicked.emit()
        
    def show_shaddow(self):
        self.shadow.setEnabled(True)
        self.setGraphicsEffect(self.shadow)
        
    def hide_shaddow(self):
        self.shadow.setEnabled(False)
        
    def off(self):
        self.btn_off = True


# Кнопки среднего размера 
class ButtonMid(ButtonBig):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(BTN_MID_SS)
        self.resize(122,42)
        
# Кнопка вкл
class ButtonOn(ButtonMid):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(BTN_ON_SS)
        

# Кнопка выкл
class ButtonOff(ButtonMid):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(BTN_OFF_SS)
        

# Страница размером 800*480 и красное пятно по фону
class PageBig(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Выставил размер
        self.resize(800,480)
        
        # Красное пятно по фону
        self.spot = QLabel(self)
        self.spot.setPixmap(QPixmap(path.abspath("red_spot.png")))
        self.spot.resize(800,480)
        self.spot.hide()


# labels для фонового виджета(температ, время, дата)
class BgLabels(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('color: red; font: 12pt;')
                
        
# Виджет "Задний фон": черн фон, выпуклая полоса сверху, температ, время, дата 
class BgWidget(PageBig):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        labels_y_coord = 0
        
        self.colon_show = False
        
        # MAIN BACKGROUND
        bg_label = QLabel(self)     
        bg_pixmap = QPixmap(path.abspath("background.png"))
        bg_label.setPixmap(bg_pixmap)
        bg_label.resize(800,480)
        
        # TEMPERATURE, TIME, DATE label
        bg_temp = BgLabels(self)
        bg_temp.move(556, labels_y_coord)
        bg_temp.setText('+22C')
        
        self.bg_h = BgLabels(self)
        self.bg_h.move(638, labels_y_coord)
        self.bg_h.setText('18')
        
        self.bg_c = BgLabels(self)
        self.bg_c.move(656, labels_y_coord)
        self.bg_c.setText(':')
        
        self.bg_m = BgLabels(self)
        self.bg_m.move(663, labels_y_coord)
        self.bg_m.setText('11')
        
        self.bg_date = BgLabels(self)
        self.bg_date.move(712, labels_y_coord)
        self.bg_date.setText(datetime.today().strftime('%d.%m.%Y'))
        
        # Показ времени
        timer = QTimer(self)
        timer.timeout.connect(self.show_time_day)
        timer.start(1000)
        
    # Время на BG    
    def show_time_day(self):
        tm = datetime.today()
        
        self.colon_show = not self.colon_show
        colon = ''
        if self.colon_show: colon = ':'
        else: colon = ''
        
        self.bg_h.setText(tm.strftime('%H'))
        self.bg_c.setText(colon)
        self.bg_m.setText(tm.strftime('%M'))
        
        self.bg_date.setText(tm.strftime('%d.%m.%Y'))

# Страница приветствия
class PageHellow(PageBig):
    def __init__(self):
        super().__init__()
        
        self.spot.show()
        
        label_hellow = QLabel(self)
        label_hellow.setStyleSheet('color: red; font: 40pt;')
        label_hellow.move(100, 70)
        label_hellow.setText('Приветствую / Welcome')
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=-4, yOffset=4, color=QColor(0, 0, 0, 250))
        label_hellow.setGraphicsEffect(shadow)
        
        l_bg_smart_home = QLabel(self)
        l_bg_smart_home.setPixmap(QPixmap(path.abspath("bg_smart_home.png")))
        l_bg_smart_home.resize(800,94)
        l_bg_smart_home.move(0, 180)
        
        l_smart_home = QLabel(self)
        l_smart_home.setStyleSheet('color: white; font: 20pt;')
        l_smart_home.move(270, 190)
        l_smart_home.setText('Система Умный дом')
        
        l_smart_home1 = QLabel(self)
        l_smart_home1.setStyleSheet('color: white; font: 14pt;')
        l_smart_home1.move(305, 230)
        l_smart_home1.setText('Smart Home System')
        
        l_choose_lang = QLabel(self)
        l_choose_lang.setStyleSheet('color: white; font: 16pt;')
        l_choose_lang.move(220, 300)
        l_choose_lang.setText('Выберите язык / Choose the language')
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=-2, yOffset=2, color=QColor(0, 0, 0, 250))
        l_choose_lang.setGraphicsEffect(shadow)
        
        self.btn_ru = ButtonBig(self)
        self.btn_ru.move(110, 370)
        self.btn_ru.setText('Русский')
        
        self.btn_en = ButtonBig(self)
        self.btn_en.move(450, 370)
        self.btn_en.setText('English')
        
# Страница ввода пароля        
class PageHomePassword(PageBig):
    okPswd = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.pswd = '3334'
        
        # Кнопка Назад
        self.back_btn = ButtonMid(self)
        self.back_btn.setText('Назад')
        self.back_btn.move(30,50)
        
        # Надпись "Пароль от сист умн дом"
        self.l_welcome = QLabel(self)
        self.l_welcome.setStyleSheet('color: red; font: 26pt;')
        self.l_welcome.resize(400,100)
        self.l_welcome.move(240, 50)
        self.l_welcome.setText('Пароль от системы \n      Умный дом')
        
        # 4 сегмента индикатора пароля
        self.ind_position = 0
        self.indic_segment = []
        for num_seg in range(4):
            self.indic_segment.append( BgLabels(self) )
            self.indic_segment[num_seg].setStyleSheet('color: #a9292a; font: 40pt;')
            self.indic_segment[num_seg].setText('*')
            self.indic_segment[num_seg].resize(70, 70)
            self.indic_segment[num_seg].move(280+num_seg*70, 140)
        
        # Кнопки ввода пароля
        self.keypad = QGroupBox(self)
        grid = QGridLayout()
        self.keypad.setLayout(grid)

        names = ['7', '8', '9',
                 '4', '5', '6',
                 '1', '2', '3',
                 'Del', '0', 'Ok']

        positions = [(i,j) for i in range(4) for j in range(3)]
        
        self.buttons = {}
        for position, name in zip(positions, names):
            btn = QPushButton(name)
            grid.addWidget(btn, *position)
            self.buttons[name] = btn
            btn.clicked.connect(partial(self.on_clicked, name))
            
        self.keypad.resize(300,250)
        self.keypad.move(250,210)
        self.keypad.setStyleSheet('background: #230608; border: 2px solid black; font: 30pt; color: #FF0000; ')
        
    def on_clicked(self, txt):
        # Если нажата цифра 0-9
        if txt in  map(str, range(0, 10)):
            if self.ind_position < 4:
                self.indic_segment[self.ind_position].setText(txt)
            if self.ind_position == 4:
                self.reset_ind()
            self.ind_position += 1
            if self.ind_position > 4:
                self.ind_position = 0
        if txt=='Del':
            self.reset_indicator()
        if txt=='Ok':
            ind_txt = self.get_ind_text()
            self.reset_indicator()
            if ind_txt == self.pswd:
                self.okPswd.emit()
            
    def reset_ind(self):
        for num_seg in range(4):
            self.indic_segment[num_seg].setText('*')
            
    def reset_indicator(self):
        self.reset_ind()
        self.ind_position = 0
        
    def get_ind_text(self):
        txt = ''
        for num_seg in range(4):
            txt += self.indic_segment[num_seg].text()
        return txt
        
    def set_lang(self, lang='ru'):
        if lang=='ru':
            self.back_btn.setText('Назад')
            self.l_welcome.setText('Пароль от системы \n      Умный дом')
            self.l_welcome.move(240, 50)
        else:
            self.back_btn.setText('Back')
            self.l_welcome.setText('Smart Home\n  password')
            self.l_welcome.move(300, 50)

# Большие кнопки для страницы управления комнатами
class ButtonBigMng(ButtonBig):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.btn_off = False
        
    def mousePressEvent(self, event):
        if not self.btn_off:
            self.btn_active = True
            self.okClicked.emit()
            self.btn_active = False
        
    def mouseReleaseEvent(self, event):
        pass
        
    def off(self):
        self.btn_off = True
        self.setStyleSheet(BIG_BTN_SS_OFF)
                
# Страница управления комнатами и приборами        
class ManagementPage(PageBig):
    def __init__(self):
        super().__init__()
        
        # вкл показ красного пятна по фону
        self.spot.show()
        
        self.sm_btns_light = LINE_ROOMS_NAME_RU
                                
        self.sm_btns_el = LINE_ROOMS_NAME_RU 
            
        # Кнопки переключения глобальные
        self.mng_btn_names = BIG_BTNS_NAME_RU   # Список имен управляющих кнопок
                                
        self.mng_btn_count = len(self.mng_btn_names)    # Длина списка имен
        self.active_mng_btn = 2     # Какая кнопка первая будет активна при вкл
        
        # Создание и инициализация страниц. Заполняю названия + названия кнопок
        #                       Данные для страницы маленьких кнопок(назв линии, кн вкл. выкл.)
        #                           массив названий линий       назв кн ON
        #                                               назв кн OFF        состояние кнопок
        self.pages_setup_data_ru = [[LINE_ROOMS_NAME_RU,   'выкл', 'вкл',  LIGHT_ROOM_STATE],
                                    [LINE_ROOMS_NAME_RU,   'выкл', 'вкл',  VENT_ROOM_STATE],
                                    [LINE_ROOMS_NAME_RU, 'выкл', 'вкл',  ELEC_ROOM_STATE],
                                    [LINE_ROOMS_NAME_RU, 'закр', 'откр', DOOR_ROOM_STATE],
                                    [LINE_ROOMS_NAME_RU,   'выкл', 'вкл',  SIGN_ROOM_STATE],
                                    [LINE_ROOMS_NAME_RU,   '-',    '+',    TEMP_ROOM_STATE]]
                                
        self.pages_setup_data_en = [[LINE_ROOMS_NAME_EN,   'off', 'on',   LIGHT_ROOM_STATE],
                                    [LINE_ROOMS_NAME_EN,   'off', 'on',   VENT_ROOM_STATE],
                                    [LINE_ROOMS_NAME_EN, 'off', 'on',   ELEC_ROOM_STATE],
                                    [LINE_ROOMS_NAME_EN, 'lock','open', DOOR_ROOM_STATE],
                                    [LINE_ROOMS_NAME_EN,   'off', 'on',   SIGN_ROOM_STATE],
                                    [LINE_ROOMS_NAME_EN,   '-',   '+',    TEMP_ROOM_STATE]]
        self.mng_btn = []
        self.small_btn_pages = []
        for cc in range(self.mng_btn_count):
            self.mng_btn.append(ButtonBigMng(self))
            if not BIG_BTNS_ACTIVE[cc]:
                self.mng_btn[cc].off()
            self.mng_btn[cc].move(15, 35+cc*72)
            self.mng_btn[cc].okClicked.connect(self.find_active_btn) #Подключает подсветку больш кнопки при нажатии
            self.small_btn_pages.append(RoomPage(self)) # Загружаю стр с мал. кнопками, привязанную к больш кнопке
            self.set_sm_btn_page(self.pages_setup_data_ru[cc], cc) # Делаю установки страницы с мал кнопками
            
            
            
        self.set_mng_btn_names()
        self.activate_mng_btn()
        
        # Вертикальн черта
        l_vert = QLabel(self)
        l_vert.setPixmap(QPixmap(path.abspath("vert_line.png")))
        l_vert.resize(7,447)
        l_vert.move(270, 34)
        
        # Коннекшн больших кнопок
        #self.mng_btn[0].okClicked.connect(self.light)
        #self.mng_btn[1].okClicked.connect(self.vent)
        self.mng_btn[2].okClicked.connect(self.electro)
        #self.mng_btn[3].okClicked.connect(self.doors)
        self.mng_btn[4].okClicked.connect(self.signal)
        #self.mng_btn[5].okClicked.connect(self.temp)
        
    # Вписываю названия больших кнопок
    def set_mng_btn_names(self):
        for cc in range(self.mng_btn_count):
            self.mng_btn[cc].setText(self.mng_btn_names[cc])
    
    # Нахожу и запоминаю активную большую кнопку
    def find_active_btn(self):
        for cc in range(self.mng_btn_count):
            if self.mng_btn[cc].btn_active:
                self.active_mng_btn = cc
        self.activate_mng_btn()
        
    # Показываю активную большую кнопку, остальные делаю неактивными
    def activate_mng_btn(self):
        for cc in range(self.mng_btn_count):
            if cc == self.active_mng_btn:
                self.mng_btn[cc].show_shaddow()
                self.hide_all_but_one(cc)
            else:
                self.mng_btn[cc].hide_shaddow()
                
    # Ф-ции больших кнопок
    #                    номер кнопки
    def light(self):
        self.hide_all_but_one(0)
        
    def vent(self):
        self.hide_all_but_one(1)
        
    def electro(self):
        self.hide_all_but_one(2)
        
    def doors(self):
        self.hide_all_but_one(3)
        
    def signal(self):
        self.hide_all_but_one(4)
        
    def temp(self):
        self.hide_all_but_one(5)
    
    # Задаю параметры маленьких кнопок на странице    
    def set_sm_btn_page(self, data, page_num):
        names_array, txt_off, txt_on, btn_state = data[0], data[1], data[2], data[3]
        self.small_btn_pages[page_num].btns_name = names_array
        self.small_btn_pages[page_num].set_btn_name()
        self.small_btn_pages[page_num].set_txt_offon_btn(txt_off, txt_on)
        self.small_btn_pages[page_num].set_state_offon_btn(btn_state)
    
    # прячет все страницы с маленькими кнопками, кроме заданной
    def hide_all_but_one(self, num_page):
        for cc in range(self.mng_btn_count):
            if cc==num_page:
                self.small_btn_pages[cc].show()
            else:
                self.small_btn_pages[cc].hide()
    
    # Делаю все настройки на всех страницах( для смены языка)
    def set_all_sm_btn_pages(self, lang='ru'):
        for cc in range(self.mng_btn_count):
            if lang == 'ru':
                self.set_sm_btn_page(self.pages_setup_data_ru[cc], cc)
            else:
                self.set_sm_btn_page(self.pages_setup_data_en[cc], cc)

        
# Кнопки, которые непосредственно вкл и выкл приборы и комнаты        
class RoomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(520,450)
        self.move(270, 40)
        
        self.btns_name = LINE_ROOMS_NAME_RU
                        
        self.btn_count = len(self.btns_name)
        self.btns = []
        for cc in range(self.btn_count):
            self.btns.append(RPLine(self))
            self.btns[cc].move(10, 50+cc*50)
        self.set_btn_name()    
    
    # Уст название комнаты в линии
    def set_btn_name(self):
        for cc in range(self.btn_count):
            self.btns[cc].lb.setText(self.btns_name[cc])
    
    # Уст имя кнопок вкл/выкл 
    def set_txt_offon_btn(self, text_off, text_on):
        for cc in range(self.btn_count):
            self.btns[cc].boff.setText(text_off)
            self.btns[cc].bon.setText(text_on)
    
    # Устанавливаю состояние кнопок вкл/выкл на странице
    def set_state_offon_btn(self, state):
        for cc in range(self.btn_count):
            self.btns[cc].state = state[cc]
            if state[cc] == 1:
                self.btns[cc].set_on()
            elif state[cc] == 0:
                self.btns[cc].set_off()
            elif state[cc] == -1:
                self.btns[cc].set_undef()
            elif state[cc] > 1:
                self.btns[cc].set_temp(state[cc])

# Линия исполнительных кнопок с фоном, ромбиком, именем, кнопками вкл. и выкл.
class RPLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.resize(520,43)
        
        # Состояние линии (вкл/выкл), если =-1, то нельзя изменить
        self.state = 0
        
        # фоновый label
        self.lbg = QLabel(self)
        self.lbg.resize(520,43)
        self.lbg.setPixmap(QPixmap(path.abspath("lbg.png")))
        
        # label ромба
        self.rmb = QLabel(self)
        self.rmb.resize(16,22)
        self.rmb.setPixmap(QPixmap(path.abspath("rmb.png")))
        self.rmb.move(10,11)
        
        # Название комнаты
        self.lb = QLabel(self)
        self.lb.setStyleSheet('color: white; font: 16pt;')
        self.lb.resize(170,25)
        self.lb.setText('Комната')
        self.lb.move(40,10)
        
        # Кнопка Вкл (неактивна по умолчанию)
        self.boff = ButtonMid(self)
        self.boff.setText('off')
        self.boff.move(220,0)
        self.boff.okClicked.connect(self.set_off)
        
        # Кнопка Выкл (неактивна по умолчанию)
        self.bon = ButtonMid(self)
        self.bon.setText('on')
        self.bon.move(360,0)
        self.bon.okClicked.connect(self.set_on)
        
        # Показатель температуры
        self.tl = QLabel(self)
        self.tl.setStyleSheet('color: red; font: 16pt; background: black; border: 1px solid white;')
        self.tl.resize(70,35)
        self.tl.setText('+17C')
        self.tl.move(360,5)
        self.tl.hide()
    
    # Ф-ции вкл и выкл кнопок    
    def set_on(self):
        if self.state>-1 and self.state<2:
            self.state = 1
            self.bon.setStyleSheet(BTN_ON_SS)
            self.boff.setStyleSheet(BTN_MID_SS)
        
    def set_off(self):
        if self.state>-1 and self.state<2:
            self.state = 0
            self.bon.setStyleSheet(BTN_ON_SS)
            self.boff.setStyleSheet(BTN_OFF_SS)
            
    def set_undef(self):
        if self.state == -1:
            self.state = -1
            self.bon.setStyleSheet(BTN_MID_SS)
            self.bon.off()
            self.boff.setStyleSheet(BTN_MID_SS)
            self.boff.off()
            
    def set_temp(self, t=17):
        if self.state > -1:
            self.state = t
            self.bon.hide()
            self.boff.hide()
            self.tl.setText('+'+str(t)+'C')
            self.tl.show()

# Страница показывается, когда введен пароль к камину 
class AllOpen(PageBig):
    def __init__(self):
        super().__init__()
        
        self.spot.show()
        
        l_bg_smart_home = QLabel(self)
        l_bg_smart_home.setPixmap(QPixmap(path.abspath("bg_smart_home.png")))
        l_bg_smart_home.resize(800,94)
        l_bg_smart_home.move(0, 180)
        
        self.tx = QLabel(self)
        self.tx.setStyleSheet('color: white; font: 20pt;')
        
        self.lang('ru')
        
    def lang(self, lng):
        if lng == 'en':
            self.tx.move(240, 210)
            self.tx.setText('Access to cutting obtained')
        else:
            self.tx.move(210, 210)
            self.tx.setText('Доступ к Разделочной получен')


# Черный экран - откл умн дом
class OFF(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,480)
        
        lb = QLabel(self)
        lb.resize(800,480)
        lb.move(0, 0)
        lb.setStyleSheet('background-color: black;')

                
class VideoPage(PageBig):
    def __init__(self):
        super().__init__()
        if CV2_ON:
            self.cap = cv2.VideoCapture(0)
        
        # Кнопка Назад
        self.back_btn = ButtonMid(self)
        self.back_btn.setText('Назад')
        self.back_btn.move(15,50)
        
        # create a video label
        self.label = QLabel(self)
        self.label.move(160, 35)
        self.label.resize(640, 480)
        
        self.timer = QTimer()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.setImage)
        self.timer.start()
        
    def setImage(self):
        if CV2_ON:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),1)
                
                convertToQtFormat = QImage( rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                pict = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                
                self.label.setPixmap(QPixmap.fromImage(pict))