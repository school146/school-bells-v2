import displaying.LCD_2004
import threading
import os
import time
from termcolor import colored
import timetable.utils
import configuration
from datetime import datetime
import daemon.ring_callbacks as ring_callbacks

class Daemon(threading.Thread):
    today_timetable: list
    muted_rings: list
    order = 0
    last_called_timing: str = '00:00'
    next_called_timing: str = '00:00'
    gpio_mode = False
    status: bool = True

    def __init__(self, table, muted):
        super().__init__()
        self.daemon = True
        self.update(table, muted)
        
        if (os.system('echo 1 > /sys/class/gpio10/value && echo 0 > /sys/class/gpio10/value') == 0):
            self.gpio_mode = True
        
        ring_callbacks.init()
        # UNCOMMENT ON PI
        displaying.LCD_2004.initial_output(table)

    def update(self, new_timetable, new_muted):
        self.today_timetable, self.muted_rings = new_timetable, new_muted # Обращаться к sqlite из другого потока нельзя
        self.today_timetable = list(map(lambda e: e.zfill(5), self.today_timetable))
        
        # Uncomment on PI
        displaying.LCD_2004.update(self.today_timetable, self.order, self.next_called_timing)

        print(colored('[DAEMON] ', 'blue') + "Updated timetable:", self.today_timetable)
        print(colored('[DAEMON] ', 'blue') + "Updated muted list:", *self.muted_rings)

    def run(self):
        while self.status:
            time.sleep(1)
            timing = str(datetime.now().time())[:5]
            timing_forward = timetable.utils.sum_times(timing, configuration.pre_ring_delta)

            if (timing in self.today_timetable and timing != self.last_called_timing):
                self.screen.clear()
                self.order += 1

                ring_order = self.today_timetable.index(str(datetime.now().time())[:5])

                if self.muted_rings[ring_order] == 0:
                    ring_callbacks.start_ring()
                    
                    self.last_called_timing = timing
                    time.sleep(configuration.ring_duration)
                    ring_callbacks.stop_ring()
                else:
                    print(f'No ring (muted ring at {timing})')
                    self.last_called_timing = timing

            if (timing_forward in self.today_timetable and timing != self.last_called_timing):
                ring_order = self.today_timetable.index(timing_forward)

                if self.muted_rings[ring_order] == 0:
                    ring_callbacks.start_pre_ring()
                    
                    self.last_called_timing = timing
                    time.sleep(configuration.pre_ring_duration)
                    ring_callbacks.stop_ring()
                    self.last_called_timing = timing
                else:
                    print(f'No prering (muted ring at {timing})')
                    self.last_called_timing = timing


        # Uncomment on PI
        displaying.LCD_2004.next(self.next_called_timing)

    def instant_ring(self):
        ring_callbacks.start_ring()
        time.sleep(configuration.ring_duration)
        ring_callbacks.stop_ring()
