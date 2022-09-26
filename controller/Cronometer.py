

import threading
import time


class Cronometer():

    def __init__(self):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.running = False

    def restart(self):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def runCronometer(self):
        try:
            while True:
                if not self.running:
                    break

                self.seconds += 1
                if self.seconds == 60:
                    self.seconds = 0
                    self.minutes += 1
                    if self.minutes == 60:
                        self.minutes = 0
                        self.hours += 1
                time.sleep(1)

            return True
        except Exception as e:
            print(e)

    def start(self):
        self.running = True
        self.cronometerThread = threading.Thread(target=self.runCronometer, daemon=True)
        self.cronometerThread.start()

    def stop(self):
        try:
            self.running = False
            # self.cronometerThread.join()
        except Exception as e:
            print(e)

    def getCronomterAsStr(self):
        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
