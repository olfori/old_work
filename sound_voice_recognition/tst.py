import time

import RPi.GPIO as GPIO
#import GPIOEmu as GPIO


def GPIO_tst():
    '''test GPIO'''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for pin in range(1, 28):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(pin, GPIO.input(pin))
        time.sleep(0.5)


if __name__ == '__main__':
    GPIO_tst()
