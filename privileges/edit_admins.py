import privileges.admins as admins
from . import validate
from telebot import *
from logging_features.previledge_logger import *

def add(bot: TeleBot, message):
    admins.append_admin('ncinsli')

    if ' ' not in message.text:
        bot.reply_to(message, 'Если Вы хотите добавить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    target = message.text.split()[1].replace('@', '')

    if (validate.check(message) and not admins.contains(target)):
        admins.append_admin(target)
        log_admin_adding(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь администратор')

    elif not admins.contains(target):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_adding(message.from_user.username, target, 'ACCESS_DENIED')
        
    else:
        bot.reply_to(message, f'❌ @{target} уже администратор')
        log_rejected_admin_adding(message.from_user.username, target, 'NO_SUCH_ADMIN')

def remove(bot: TeleBot, message):
    admins.append_admin('ncinsli')
    
    target = message.text.replace(' ', '')[len('/rm_admin'):].replace('@', '')

    if target == '':
        bot.reply_to(message, 'Если Вы хотите удалить администратора, Вы должны указать его имя пользователя или Telegram ID')
        return
    
    if (validate.check(message) and admins.contains(target)):
        admins.delete_admin(target)
        log_admin_removing(message.from_user.username, target)
        bot.reply_to(message, f'✅ @{target} теперь не администратор')

    elif admins.contains(target):
        bot.reply_to(message, '❌ У Вас нет прав администратора')
        log_rejected_admin_removing(message.from_user.username, target, 'ACCESS_DENIED')

    else:
        bot.reply_to(message, f'❌ @{target} не был администратором')
        log_rejected_admin_removing(message.from_user.username, target, 'NO_SUCH_ADMIN')
