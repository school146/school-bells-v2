from RPLCD import i2c
from datetime import datetime
import time

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
    lcd.write_string(' Last update: 28.12')
    lcd.crlf()
    lcd.write_string('        2022')
    lcd.crlf()
    time.sleep(5)
    lcd.clear()
    if nearest != -1:
        lcd.write_string(f'Next ring: {timetable[i]}')
        lcd.crlf()
        lcd.write_string(f'(if not muted)')
    else:
        lcd.write_string('No more rings today')
def update(timetable: list, order: int, next_called_timing):
    lcd.clear()
    lcd.write_string(f'Next ring at {timetable[order]}')
    print('update')
    print(timetable[order])
def next(next_called_timing: str):
    lcd.clear()
    lcd.write_string(f'Next ring at {next_called_timing}')
    print('next')
    print(next_called_timing)
def no_more_rings():
    lcd.clear()
    lcd.writestring('No more rings for today')
    print('no more rings')
