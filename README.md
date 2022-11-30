Команда: Гидроплазменный анигилятор

Проект: Служба Звонков (ru) и BridgeBell (en)

Роли: Василий Гайсен - программист, Федор Жаков - программист и hardware-щик, Демьян Бажин - генератор идей, Кирилла Райзих - копирайтер, Дарья Степанова - дизайн

Идея: Решение проблемы негибкости расписания в существующей системе автоматической подачи звонков. Этот бот - логическое продолжение репозитория https://github.com/school146/school-bells, частичная реализация TODO из README того репозитория. Бот позволяет сдвигать расписание, изменять длину любых уроков и перемен, менять расписание по json-файлу

Инструменты: показывает гитхаб. PyTelegramBotApi, sqlite3, LCD-скрипты с гитхаба

Планы: Доделать корпус, починить LCD (возможно, поменять), поменять экран на 4-х строчный, добавить конфигуратор, отрефакторить

Проблемы в коде, о которых мы осведомлены: 

    Связность
    
    Функции с сайд-эффектами намешаны с чистыми функциями в области, где виды функций следовало бы сделать одинаковыми
    
    PEP 8 + неиспользование logging
    
    Daemon не соответствует SRP (писали, очень торопясь)
    
    Кривые наименования во многих местах
    
    Неэффективные запросы в БД и вызовы конструктора TimetableStorage
    
    Отсутствие валидации команд и возможности убрать дату из аргументов почти всех команд
    
    Мелкие баги с zfill

# Beller
A powerful telegram bot that provides a convenient interface for ring controlling at schools

# Commands (in Russian)

**/get_timetable** - Расписание звонков 

**/ring** - Вызвать звонок вручную

**/add_admin** - Добавить администратора
**/rm_admin** - Удалить администратора

**/pre_ring_edit** - Изменить интервал между предзвонком и основным звонком (в секундах) [TODO]

**/lesson_duration** - Изменить длину уроков [TODO]
**/break_duration** - Изменить длину перемен [TODO]

**/shift dd.mm.yyyy +-(int)(min/h)** - Сдвинуть всё расписание

**/resize dd.mm.yyyy lesson/break int +-int(h/min)** - Изменение длины конкретной перемены или конкретного урока в конкретный день (по правой границе)
    
    Пример: /resize 26.12.2022 break 1 +10min
            /resize 31.12.2022 lesson 2 -5min

**/mute dd.mm.yyyy hh:mm** - Заглушить звонок, который должен произвенеть в заданное время
   
    Пример: /mute 01.12.2022 9:45** - Заглушить звонок в 9:45 1 декабря 2022 года
    
**/unmute dd.mm.yyyy hh:mm** - Действие, обратное **/mute**
**/set_timetable** - Установка расписания из JSON
**/silent_mode** - Выключает всю автоматику [TODO]
**/wakeup** - Включает всю автоматику, если она выключена [TODO]


# Architecture

main.py - command routes 

 admins.middleware - command text processors for admin tools (/add_admin, /rm_admin)

   admins/(edit, storage, validator etc.) - tools for SQL sync

 timetable.middleware - command text processors for timetable editing tools (/shift, /resize, /mute etc.)

   timetable/(shifting, resizing, getting, setting etc.) - tools for SQL sync
        
 daemon - the process that does all the waiting work
    
  
