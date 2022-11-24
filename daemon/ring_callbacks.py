from telebot import *
from termcolor import colored

duration = 3000 #Config

def start_ring():
    print(colored('RING!', 'green'))

def stop_ring():
    print(colored('STOP RING', 'red'))