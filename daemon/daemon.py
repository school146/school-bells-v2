# import displaying.LCD_1602
import threading
import time
from termcolor import colored
from datetime import datetime
import daemon.ring_callbacks as ring_callbacks

class Daemon(threading.Thread):
    ring_duration = 3
    today_timetable: list
    muted_rings: list
    order = 0
    last_called_timing: str = '00:00'
    next_called_timing: str = '00:00'
    #screen = LCD()
    time_buffer = 0
    status: bool = True

    def __init__(self, timetable, muted):
        super().__init__()
        self.daemon = True
        self.update(timetable, muted)
        ring_callbacks.init()
        # UNCOMMENT ON PI
        # displaying.LCD_1602.initial_output(timetable)

    def update(self, new_timetable, new_muted):
        self.today_timetable, self.muted_rings = new_timetable, new_muted # Обращаться к sqlite из другого потока нельзя
        self.today_timetable = list(map(lambda e: e.zfill(5), self.today_timetable))

        # Uncomment on PI
        # displaying.LCD_1602.update(self.today_timetable, self.order, self.next_called_timing)

        print(colored('[DAEMON] ', 'blue') + "Updated timetable:", self.today_timetable)
        print(colored('[DAEMON] ', 'blue') + "Updated muted list:", *self.muted_rings)

    def run(self):
        while self.status:
            time.sleep(3)
            timing = str(datetime.now().time())[:5]
            
            if (timing in self.today_timetable and timing != self.last_called_timing):
          #      self.screen.clear()
                self.order += 1

                ring_order = self.today_timetable.index(str(datetime.now().time())[:5])

                if self.muted_rings[ring_order] == 0:
                    ring_callbacks.start_ring()
                    
                    self.last_called_timing = timing
                    time.sleep(self.ring_duration)
                    ring_callbacks.stop_ring()

                    self.next_called_timing = str(self.today_timetable[self.today_timetable.index(timing) + 1])
                else:
                    print(f'No ring (muted ring at {timing})')
                    self.last_called_timing = timing

        # Uncomment on PI
        # displaying.LCD_1602.next(self.next_called_timing)

    def instant_ring(self):
        ring_callbacks.start_ring()
        time.sleep(self.ring_duration)
        ring_callbacks.stop_ring()