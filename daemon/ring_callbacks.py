import os
from telebot import *
from termcolor import colored

duration = 3000 #Config
port = 25

def start_ring():
    print(colored('🔔 [DAEMON] RING!', 'blue'))

    os.system(f'echo out > /sys/class/gpio/gpio{port}/direction')
    os.system(f'echo 1 > /sys/class/gpio/gpio{port}/value')
    os.system(f'echo {port} > /sys/class/gpio/export')
    os.system(f'echo out > /sys/class/gpio/gpio{port}/direction')
    os.system(f'echo 1 > /sys/class/gpio/gpio{port}/value')

def stop_ring():
    print(colored('🔔  [DAEMON STOP RING', 'blue'))
    os.system(f'echo {port} > /sys/class/gpio/export')
    os.system(f'echo out > /sys/class/gpio/gpio{port}/direction')
    os.system(f'echo 0 > /sys/class/gpio/gpio{port}/value')