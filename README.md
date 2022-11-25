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
**/resize dd.mm.yyyy lesson/break int +-int(h/min)** - Изменение длины конкретной перемены или конкретного урока в конкретный день (по правой границе
    Пример: **/resize 26.12.2022 break 1 +10min**
            **/resize 31.12.2022 lesson 2 -5min**

**/mute dd.mm.yyyy hh:mm** - Заглушить звонок, который должен произвенеть в заданное время
    Пример: **/mute 01.12.2022 9:45** - Заглушить звонок в 9:45 1 декабря 2022 года
**/unmute dd.mm.yyyy hh:mm** - Действие, обратное **/mute**

**/set_timetable** - Установка расписания из JSON
**/silent_mode** - Выключает всю автоматику [TODO]
**/wakeup** - Включает всю автоматику, если она выключена [TODO]




