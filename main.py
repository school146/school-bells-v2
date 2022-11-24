import os
from telebot import *
from telebot import types
from users.user_storage import * 
from logging_features.ring_logger import *
import ring_commands.ring_commands as rings
import privileges.validate as validator
import privileges.edit_admins as admins
import timetable_handling.timetable_middleware as timetable

token = os.environ["BELLER_TOKEN"]
bot = TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Д')

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
    if validator.check(message, UserStorage('admins').append_user('ncinsli')):
        rings.ring()
        log_sucessful_ring(message.from_user.username)

    else:
        log_unsuccessful_ring(message.from_user.username)
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["resize"])
def add_unique(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.resize_middleware(message)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["mute"])
def mute(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.mute_middleware(bot, message)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["unmute"])
def unmute(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.unmute_middleware(bot, message)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["shift"])
def shift(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.shift_middleware(bot, message)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["get_timetable"])
def get_timetable(message):
    timetable.get_timetable_middleware(bot, message)

@bot.message_handler(commands=["set_timetable"])
def set_timetable(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        bot.reply_to(message, """Отправьте файл расписания в формате
        HH:MM - HH:MM
        HH:MM - HH:MM
        """)
        bot.register_next_step_handler(message, get_new_timetable)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

def get_new_timetable(message):
    timetable.set_timetable_middleware(bot, message)
    bot.reply_to(message, "Расписание изменено")


@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "BrigeBell146 - экземпляр системы BellBrige для МАОУ СОШ №146 с углублённым изучением физики, математики, информатики г. Перми")

bot.infinity_polling()