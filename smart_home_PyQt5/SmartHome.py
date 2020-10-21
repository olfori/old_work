import sys
from SmartHomePages import *

if GPO_ON:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SIG_OUT, GPIO.OUT)
    GPIO.output(SIG_OUT, GPIO.LOW)
    GPIO.setup(SIG_OUT_CAMERA_1 , GPIO.OUT)
    GPIO.output(SIG_OUT_CAMERA_1 , GPIO.LOW)
    GPIO.setup(SIG_OUT_CAMERA_2 , GPIO.OUT)
    GPIO.output(SIG_OUT_CAMERA_2 , GPIO.LOW)
    GPIO.setup(BYPASS_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BYPASS_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        

class SmartHome(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Чтобы пропуск хода срабатывал только 1 раз
        self.bypass_1 = False
        self.bypass_2 = False
        
        # CURSOR OFF
        if not CURSOR_ON:
            self.setCursor(Qt.BlankCursor)
            
        self.off_ok = False
        self.off_ = False
        
        # MAIN WINDOW size
        self.setFixedSize(800,480)
        
        self.fire_ok = False
        
        # LAYOUT CONTAINER FOR WIDGETS Показыв только 1 виджет одномоментно
        self.widget_layout = QStackedLayout()
        
        # WIDGETS
        self.hellow = PageHellow()
        self.home_password = PageHomePassword()
        self.mng_page = ManagementPage()
        self.fire_pass = PageHomePassword()
        self.all_open_page = AllOpen()
        self.cam = VideoPage()
        self.off = OFF()
        
        self.widget_layout.addWidget(self.hellow)
        self.widget_layout.addWidget(self.home_password)
        self.widget_layout.addWidget(self.mng_page)
        self.widget_layout.addWidget(self.fire_pass)
        self.widget_layout.addWidget(self.all_open_page)
        self.widget_layout.addWidget(self.cam)
        self.widget_layout.addWidget(self.off)
        
        # PASSWORD SETTINGS
        self.home_password.pswd = '2004'
        self.fire_pass.pswd = '0612'
        
        # BUTTONS SIGNAL AND CONNECTIONS
        self.hellow.btn_ru.okClicked.connect(self.lang_ru)
        self.hellow.btn_en.okClicked.connect(self.lang_en)
        self.home_password.back_btn.okClicked.connect(self.back_from_passw_page)
        self.home_password.okPswd.connect(self.show_mng_page)
        
        self.mng_page.small_btn_pages[2].btns[2].bon.okClicked.connect(self.show_fire_pass)
        
        self.fire_pass.back_btn.okClicked.connect(self.back_from_fire_pass)
        self.fire_pass.okPswd.connect(self.show_fire_ok)
        
        self.mng_page.small_btn_pages[4].btns[2].bon.okClicked.connect(self.show_cam)
        
        self.cam.back_btn.okClicked.connect(self.back_from_cam)
        
        # Запускаю таймер проверки входных сигналов
        self.timerGPIO = QTimer()
        self.timerGPIO.setInterval(100)
        self.timerGPIO.timeout.connect(self.checkInputs)
        self.timerGPIO.start()

        # CENTRAL WIDGET
        self.bg = BgWidget()
        self.bg.setLayout(self.widget_layout)
        self.setCentralWidget(self.bg)
        
        # SHOW CENTRAL WIDGET
        self.showFullScreen()
        self.setGeometry(0, 0, 800, 480)
    
    # Смена языка    
    def lang_ru(self):
        # Меняю текст на странице ввода пароля
        self.home_password.set_lang('ru')
        # Меняю текст на  MNG_PAGE
        self.mng_page.mng_btn_names = BIG_BTNS_NAME_RU
        self.mng_page.set_mng_btn_names()
        # Меняю названия кнопок и комнат на MNG_PAGE
        self.mng_page.set_all_sm_btn_pages('ru')
        # Меняю текст на странице ввода пароля к камину
        self.fire_pass.set_lang('ru')
        self.fire_pass.l_welcome.setText('Пароль к Разделочн.')
        # Меняю текст кн "Назад" на стр с видео
        self.cam.back_btn.setText('Назад')
        
        self.all_open_page.lang('ru')
        
        self.show_home_passw_page()
        
    def lang_en(self):
        # Меняю текст на странице ввода пароля
        self.home_password.set_lang('en')
        # Меняю текст на  MNG_PAGE
        self.mng_page.mng_btn_names = BIG_BTNS_NAME_EN
        self.mng_page.set_mng_btn_names()
        # Меняю названия кнопок и комнат на MNG_PAGE
        self.mng_page.set_all_sm_btn_pages('en')
        # Меняю текст на странице ввода пароля к камину
        self.fire_pass.set_lang('en')
        self.fire_pass.l_welcome.setText(' Cutting pass')
        # Меняю текст кн "Назад" на стр с видео
        self.cam.back_btn.setText('Back')
        
        self.all_open_page.lang('en')
        
        self.show_home_passw_page()
    
    # Методы показа страниц 
    #   Страница основного пароля   
    def show_home_passw_page(self):
        self.hellow.hide()
        self.home_password.show()
        
    def back_from_passw_page(self):
        self.home_password.hide()
        self.hellow.show()
    
    #   Страница больших и маленьких кнопок    
    def show_mng_page(self):
        self.bypass_1 = True
        self.home_password.hide()
        self.mng_page.show()
    
    #   Страница ввода пароля от камина  
    def show_fire_pass(self):
        if not self.fire_ok:
            self.mng_page.hide()
            self.fire_pass.show()
        
    def back_from_fire_pass(self):
        self.mng_page.show()
        self.fire_pass.hide()
        self.mng_page.small_btn_pages[2].btns[2].set_off()
    
    # Если введен правильный пароль камина    
    def show_fire_ok(self):
        self.fire_ok = True
        self.fire_pass.hide()
        self.all_open_page.show()
        
        if GPO_ON:
            GPIO.output(SIG_OUT, GPIO.HIGH)
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.back_fire_ok)
        self.timer.start(4000)
        
    def back_fire_ok(self):
        self.all_open_page.hide()
        self.off.show()
        
    def hideAllPages(self):
        self.hellow.hide()
        self.home_password.hide()
        self.mng_page.hide()
        self.fire_pass.hide()
        self.all_open_page.hide()
        self.cam.hide()
        self.off.hide()
    
    # Показываю видео с камеры
    def show_cam(self):
        if GPO_ON:
            GPIO.output(SIG_OUT_CAMERA_1 , GPIO.HIGH)
            GPIO.output(SIG_OUT_CAMERA_2 , GPIO.HIGH)
        self.mng_page.hide()
        self.cam.show()
        
    def back_from_cam(self):
        if GPO_ON:
            GPIO.output(SIG_OUT_CAMERA_1 , GPIO.LOW)
            GPIO.output(SIG_OUT_CAMERA_2 , GPIO.LOW)
        self.mng_page.show()
        self.cam.hide()
        self.mng_page.small_btn_pages[4].btns[2].set_off()
    
    # Жду сигналов пропуска ходов     
    def checkInputs(self):
        if GPO_ON:
            # Если Bypass_1 еще не сработал и пришел Bypass_1
            if not self.bypass_1 and not GPIO.input(BYPASS_1):
                self.hideAllPages()
                self.show_mng_page()
                self.bypass_1 = True
            # Если Bypass_1 сработал, а Bypass_2 нет и пришел Bypass_2
            if self.bypass_1 and not self.bypass_2 and not GPIO.input(BYPASS_2):
                self.hideAllPages()
                self.show_fire_ok()
                self.bypass_2 = True

    #Смотрю координаты нажатия для выхода из приложения и отладки
    def mousePressEvent(self, event):
        if self.fire_ok:
            if self.mng_page.active_mng_btn == 5:
                if event.pos().x()>760 and event.pos().y()>460:
                    self.off_ok = True
                    self.tmr = QTimer()
                    self.tmr.setSingleShot(True)
                    self.tmr.timeout.connect(self.off)
                    self.tmr.start(2000)
        if DEBUG:
            print(event.pos())
    
    # For getting out from the application
    def mouseReleaseEvent(self, event):
        if self.fire_ok and self.off_ok:
            if self.mng_page.active_mng_btn == 5:
                if event.pos().x()<20 and event.pos().y()<20:
                    self.close()
                    
    def off(self):
        self.off_ok = False
                
    # When close window
    def closeEvent(self, e):
        print("closed")
        if GPO_ON:
            GPIO.output(SIG_OUT, GPIO.LOW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartHome()
    sys.exit(app.exec_())