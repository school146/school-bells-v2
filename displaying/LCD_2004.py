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
   # nearest = datetime.now()
#    for i in range(0, len(timetable)):
 #       if timetable[i] <= datetime.now().time():
  #          nearest = i
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

    #lcd.write_string(f'{i} ring: {timetable[i]}')
    #lcd.write_string(f'(if not muted)')
def update(timetable: list, order: int, next_called_timing):
    lcd.write_string(f'Next ring at')
    lcd.write_string(f'{timetable[order]}')

    lcd.write_string(next_called_timing)

def next(next_called_timing: str):
    lcd.write_string('Next ring at')
    lcd.write_string(next_called_timing)
    lcd.close()
