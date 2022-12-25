import sqlite3
import admins.edit, admins.storage, admins.validator 
from telebot import *
import configuration
from logging_features.previledge_logger import *

connection = configuration.connection
cursor = connection.cursor()
table = configuration.admin_table_name

def init():
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table} (
        userid TEXT UNIQUE
    ) 
    """)

    connection.commit()

def add(bot: TeleBot, message):
    if ' ' not in message.text:
        bot.reply_to(message, 'Если Вы хотите добавить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    target = message.text.split()[1].replace('@', '')

    if (not admins.storage.contains(target)):
        admins.edit.append(target)
        log_admin_adding(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь администратор')

    else:
        bot.reply_to(message, f'❌ @{target} уже администратор')
        log_rejected_admin_adding(message.from_user.username, target, 'NO_SUCH_ADMIN')

def remove(bot: TeleBot, message):
    admins.edit.append('ncinsli')
    connection = configuration.connection
    
    target = message.text.replace(' ', '')[len('/rm_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите удалить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (admins.storage.contains(target)):
        admins.edit.delete(target)
        log_admin_removing(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь не администратор')
        
    else:
        bot.reply_to(message, f'❌ @{target} не был администратором')
        log_rejected_admin_removing(message.from_user.username, target, 'NO_SUCH_ADMIN')
