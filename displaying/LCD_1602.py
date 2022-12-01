from displaying.LCD import LCD
from datetime import datetime

def initial_output(timetable: list):
    screen = LCD()

    nearest = datetime.now()
    for i in range(0, len(timetable)):
        if timetable[i] <= datetime.now().time():
            nearest = i


    screen.message(f'{i} ring: {timetable[i]}')
    screen.message(f'(if not muted)', 2)

def update(timetable: list, order: int, next_called_timing):
    screen = LCD()

    screen.clear()
    screen.message(f'Next ring at', 1)
    screen.message(f'{timetable[order]}', 2)

    screen.message(next_called_timing)


def next(next_called_timing: str):
    screen = LCD()
    
    screen.message('Next ring at', 1)
    screen.message(next_called_timing, 2)