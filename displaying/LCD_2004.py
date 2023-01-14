try:
    from RPLCD import i2c
    from datetime import datetime
    import time
    import timetable.utils as utils

    lcdmode = 'i2c'
    charmap = 'A00'
    i2c_expander = 'PCF8574'
    cols = 20
    rows = 4
    port = 0
    address = 0x27
    lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                    cols=cols, rows=rows)
    lcd.backlight_enabled = True

    def set_screen(timetable: list, nearest: int):
        if nearest != -1:
            thisPeriod = 0
            nextPeriod = 0
            nowEvent = "Off"
            if nearest != 0:
                hours, minutes = map(int, timetable[nearest-1].split(':'))
                difference = list(map(int, utils.sub_times(timetable[nearest], hours * 3600 + minutes * 60).split(":")))
                thisPeriod = str(difference[0] * 60 + difference[1]) + " min"

                if nearest % 2 == 0:
                    nowEvent = "Break"
                else:
                    nowEvent = "Lesson"
            if nearest == len(timetable)-1:
                nextPeriod = "Off"
            else:
                hours, minutes = map(int, timetable[nearest].split(':'))
                difference = list(map(int, utils.sub_times(timetable[nearest+1], hours * 3600 + minutes * 60).split(":")))
                nextPeriod = str(difference[0] * 60 + difference[1]) + " min"
            if nowEvent == "Off":
                thisPeriod = "Off"
            lcd.clear()
            lcd.write_string(f'Next ring: {timetable[nearest]}')
            lcd.crlf()
            lcd.write_string(f'Now: {nowEvent}')
            lcd.crlf()
            lcd.write_string(f'Next period: {nextPeriod}')
            lcd.crlf()
            lcd.write_string(f'This period: {thisPeriod}')
        else:
            lcd.clear()
            lcd.write_string('No more rings today')

    def initial_output(timetable: list):
        nowtime = [datetime.now().hour, datetime.now().minute]
        nearest = -1
        for i in range(len(timetable)):
            if int(timetable[i].split(":")[0]) > nowtime[0] or (int(timetable[i].split(":")[0]) == nowtime[0] and int(timetable[i].split(":")[1]) > nowtime[1]):
                nearest = i
                break
        lcd.clear()
        lcd.write_string('    Bridge Bell')
        lcd.crlf()
        lcd.write_string('    Version: 1.2')
        lcd.crlf()
        lcd.write_string(' Last update: 29.12')
        lcd.crlf()
        lcd.write_string('        2022')
        lcd.crlf()
        time.sleep(5)
        lcd.clear()

        set_screen(timetable, nearest)
        
    def update(timetable: list, order: int, next_called_timing):
        nowtime = [datetime.now().hour, datetime.now().minute]
        nearest = -1
        for i in range(len(timetable)):
            if int(timetable[i].split(":")[0]) > nowtime[0] or (int(timetable[i].split(":")[0]) == nowtime[0] and int(timetable[i].split(":")[1]) > nowtime[1]):
                nearest = i
                break
        set_screen(timetable, nearest)
    def next(timetable: list, order: int):
        lcd.clear()
        set_screen(timetable, order)
    def no_more_rings():
        lcd.clear()
        lcd.write_string('No more rings today')
        print('no more rings')
except:
    print("You are not running the system on a Pi computer. All GPIO logic will be ignored")
