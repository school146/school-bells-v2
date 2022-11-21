import os
from users.user_storage import * 
from logging_features.ring_logger import *
import ring_commands.ring_commands as rings
import previleges.validate as validator
import previleges.edit_admins as admins
from telebot import *

token = os.environ["BELLER_TOKEN"]

bot = TeleBot(token)

@bot.message_handler(commands=["add_admin"])
def admin_add(message):
    admins.add(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["rm_admin"])
def admin_rm(message):
    admins.remove(bot, message)
    target = message.text.replace(' ', '')[len('/add_admin'):].replace('@', '')


@bot.message_handler(commands=["ring"])
def ring(message):
    if validator.check(message, UserStorage('admins.txt').append_user('ncinsli')):
        rings.ring()
        log_sucessful_ring(message.from_user.username)

    else:
        log_unsuccessful_ring(message.from_user.username)

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "Про меня? Что ты хочешь блин про меня узнать? Пиши на @ncinsli!")

bot.infinity_polling()