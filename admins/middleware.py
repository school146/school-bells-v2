import sqlite3
import admins.edit, admins.storage, admins.validator 
from telebot import *
from logging_features.previledge_logger import *

def add(bot: TeleBot, message, connection: sqlite3.Connection):
    admins.edit.append(connection, 'ncinsli')

    if ' ' not in message.text:
        bot.reply_to(message, 'Если Вы хотите добавить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    target = message.text.split()[1].replace('@', '')

    if (admins.validator.check(message, connection) and not admins.storage.contains(target, connection)):
        admins.edit.append(connection, target)
        log_admin_adding(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь администратор')

    elif not admins.storage.contains(target, connection):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_adding(message.from_user.username, target, 'ACCESS_DENIED')
        
    else:
        bot.reply_to(message, f'❌ @{target} уже администратор')
        log_rejected_admin_adding(message.from_user.username, target, 'NO_SUCH_ADMIN')

def remove(bot: TeleBot, message, connection: sqlite3.Connection):
    admins.edit.append(connection, 'ncinsli')
    
    target = message.text.replace(' ', '')[len('/rm_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите удалить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (admins.validator.check(message, connection) and admins.storage.contains(target, connection)):
        admins.edit.delete(connection, target)
        log_admin_removing(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь не администратор')

    elif admins.storage.contains(target, connection):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_removing(message.from_user.username, target, 'ACCESS_DENIED')

    else:
        bot.reply_to(message, f'❌ @{target} не был администратором')
        log_rejected_admin_removing(message.from_user.username, target, 'NO_SUCH_ADMIN')
