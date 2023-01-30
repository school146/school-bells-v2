import logging
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
        logging.getLogger().error(f'Operation {message.text} cancelled for user @{str(message.from_user.username).lower()}: invalid format')
        bot.reply_to(message, 'Если Вы хотите добавить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    target = message.text.split()[1].replace('@', '')

    if (not admins.storage.contains(target)):
        admins.edit.append(target)
        logging.info(f'@{message.from_user.username} added admin: {message.text.split()[1]}')
        bot.reply_to(message, f'✅ @{target} теперь администратор')

    else:
        logging.getLogger().info(f'@{message.from_user.username} tried to add admin: {message.text.split()[1]}, but there\'s already such')
        bot.reply_to(message, f'❌ @{target} уже администратор')

def remove(bot: TeleBot, message):    
    target = message.text.replace(' ', '')[len('/rm_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите удалить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (admins.storage.contains(target)):
        admins.edit.delete(target)
        logging.getLogger().info(f'@{message.from_user.username} removed admin: {message.text.split()[1]}')
        bot.reply_to(message, f'✅ @{target} теперь не администратор')
    else:
        logging.getLogger().info(f'@{message.from_user.username} tried to remove admin: {message.text.split()[1]}, but there\'s no such')
        bot.reply_to(message, f'❌ @{target} не был администратором')
