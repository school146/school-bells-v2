from telebot import *
from termcolor import colored

duration = 3000 #Config

def start_ring():
    print(colored('🔔 [DAEMON] RING!', 'blue'))

def stop_ring():
    print(colored('🔔  [DAEMON STOP RING', 'blue'))