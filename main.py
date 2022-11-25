import os
from telebot import *
from telebot import types
from daemon.daemon import Daemon
from users.user_storage import *
import privileges.validate as validator
import privileges.edit_admins as admins
from logging_features.ring_logger import *
from timetable_handling.timetable_storage import TimetableStorage
import timetable_handling.timetable_middleware as timetable

token = os.environ["BELLER_TOKEN"]
bot = TeleBot(token)

date_time = datetime.now()
refreshed_timetable, refreshed_mutetable = TimetableStorage().get_timetable(datetime(date_time.year, date_time.month, date_time.day))

daemon = Daemon(refreshed_timetable, refreshed_mutetable)

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
        daemon.instant_ring()
        # log_sucessful_ring(message.from_user.username)

    else:
        log_unsuccessful_ring(message.from_user.username)
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["resize"])
def resize(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.resize_middleware(message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["mute"])
def mute(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.mute_middleware(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["unmute"])
def unmute(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.unmute_middleware(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["shift"])
def shift(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        timetable.shift_middleware(bot, message, daemon)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

@bot.message_handler(commands=["get_timetable"])
def get_timetable(message):
    timetable.get_timetable_middleware(bot, message, daemon)

@bot.message_handler(commands=["set_timetable"])
def set_timetable(message):
    if (validator.check(message, UserStorage('admins').append_user('ncinsli'))):
        bot.reply_to(message,
        """Отправьте файл расписания в формате JSON по одному из шаблонов
        1. Сдвиговой формат(https://docs.github.com/......)
        2. Абсолютный формат(https://docs.github.com/.....)
        """)
        bot.register_next_step_handler(message, get_new_timetable)
    else:
        bot.reply_to(message, '❌ Недостаточно прав')

def get_new_timetable(message):
    returnedMessage = timetable.set_timetable_middleware(bot, message, daemon)
    bot.reply_to(message, returnedMessage)


@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "BrigeBell146 - экземпляр системы BellBrige для МАОУ СОШ №146 с углублённым изучением физики, математики, информатики г. Перми")

print(f"Starting {colored('[DAEMON]', 'blue')} and BOT")
daemon.start()
bot.infinity_polling()
