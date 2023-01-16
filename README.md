## School bells v2 | Beller Bot | BridgeBell146

Система управления школьными звонками
Полностью управляется из Telegram
Проект: Служба Звонков (ru) и BridgeBell (en)

## Запуск
Роли: Василий Гайсен - программист, Федор Жаков - программист и hardware-щик, Демьян Бажин - генератор идей, Кирилла Райзих - копирайтер, Дарья Степанова - дизайн

```git clone https://github.com/school146/school-bells-v2/
pip3 install pyTelegramBotApi
pip3 install smbus2
export BELLER_TOKEN=токен # ОПЦИОНАЛЬНО
screen -dmS bells python3 main.py
```
# Команды
Идея: Решение проблемы негибкости расписания в существующей системе автоматической подачи звонков. Этот бот - логическое продолжение репозитория https://github.com/school146/school-bells, частичная реализация TODO из README того репозитория. Бот позволяет сдвигать расписание, изменять длину любых уроков и перемен, менять расписание по json-файлу

<Х> обозначает опциональность аргумента Х -- при отсутствии он запомлняется аргументом по умолчанию
Инструменты: показывает гитхаб. PyTelegramBotApi, sqlite3, LCD-скрипты с гитхаба

Для не-администраторов доступна команда
**/get_timetable** - Расписание звонков 
Планы: Доделать корпус, починить LCD (возможно, поменять), поменять экран на 4-х строчный, добавить конфигуратор, отрефакторить

Для администраторов доступны команды:
# Beller
A powerful telegram bot that provides a convenient interface for ring controlling at schools

# Commands (in Russian)

**/get_timetable** - Расписание звонков 

**/ring** - Вызвать звонок вручную

**/add_admin** - Добавить администратора

**/rm_admin** - Удалить администратора

**/pre_ring_edit** - Изменить интервал между предзвонком и основным звонком (в секундах)
**/pre_ring_edit** - Изменить интервал между предзвонком и основным звонком (в секундах) [TODO]

**/lesson_duration** - Изменить длину уроков
**/lesson_duration** - Изменить длину уроков [TODO]
**/break_duration** - Изменить длину перемен [TODO]

**/break_duration** - Изменить длину перемен
**/shift dd.mm.yyyy +-(int)(min/h)** - Сдвинуть всё расписание

**/shift <dd.mm.yyyy> +-(int)(min/h)** - Сдвинуть всё расписание
**/resize dd.mm.yyyy lesson/break int +-int(h/min)** - Изменение длины конкретной перемены или конкретного урока в конкретный день (по правой границе)

    Пример: /shift 26.12.2022 +10min    Сдвинуть расписание 26-го декабря на 10 минут вперед 
            /shift -1h                  Сдвинуть расписание сегодня на час назад
    Пример: /resize 26.12.2022 break 1 +10min
            /resize 31.12.2022 lesson 2 -5min

**/resize <dd.mm.yyyy> lesson/break int +-int(h/min)** - Изменение длины конкретной перемены или конкретного урока в конкретный день (по правой границе)

    Пример: /resize 26.12.2022 break 1 +10min     Сделать первую перемену 26 декабря длиннее на 10 минут   
            /resize lesson 2 -5min                Сделать второй урок короче на пять минут

**/mute <dd.mm.yyyy> hh:mm** - Заглушить звонок, который должен произвенеть в заданное время
**/mute dd.mm.yyyy hh:mm** - Заглушить звонок, который должен произвенеть в заданное время

    Пример: /mute 01.12.2022 9:45      Заглушить звонок в 09:45 1 декабря 2022 года
            /mute 10:40**              Заглушить звонок в 10:40   

    Пример: /mute 01.12.2022 9:45** - Заглушить звонок в 9:45 1 декабря 2022 года

**/unmute <dd.mm.yyyy> hh:mm** - Действие, обратное **/mute**
**/unmute dd.mm.yyyy hh:mm** - Действие, обратное **/mute**
**/set_timetable** - Установка расписания из JSON
**/silent_mode** - Выключает всю автоматику [TODO]
**/wakeup** - Включает всю автоматику, если она выключена [TODO]

    Пример: /unmute 01.12.2022 9:45.     Убрать глушение с звонка в 09:45 1 декабря 2022 года
            /unmute 10:40**.             Убрать глушение с звонка в 10:40   

**/set_timetable** - Установка расписания из JSON
# Architecture

**/mute_all <dd.mm.yyyy>** - Заглушить все звонки на определенный день
**/unmute_all <dd.mm.yyyy>** - Убрать глушение со всех звонков на сегодняшний день
main.py - command routes 

# Архитектура
 admins.middleware - command text processors for admin tools (/add_admin, /rm_admin)

main.py - Точка входа, обработчик команд с валидацией
   admins/(edit, storage, validator etc.) - tools for SQL sync

timetable.middleware - промежуточный слой, группа функций, которые обрабатывают сообщения с командами по управлению расписанием, занимаются декомпозицией на аргументы и вызовом функций по управлению БД
admins.middleware - то же, но обрабатывает сообщения с командами по управлению привилегиями
 timetable.middleware - command text processors for timetable editing tools (/shift, /resize, /mute etc.)

timetable.(shifting, resizing...) - слой по управлению БД с информацией о расписании
admins.(edit, storage, validator etc.) - слой по управлению БД с информацией об адиминах
   timetable/(shifting, resizing, getting, setting etc.) - tools for SQL sync

daemon - Фоновый процесс, отвечающий за то, чтобы звонить по временамм из БД
Главный его метод, помимо run -   
daemon.update(...) вызывается, когда расписание меняется во время работы, а так же на старте демона
 daemon - the process that does all the waiting work


configuration.py - статические переменные и конфигурационная информация
