
from rich.console import Console
from copy import deepcopy
import threading
from classes.AttentionPoint import AttentionPoint
import time

from utils.clear import clear

from pynput import keyboard as kb


class Simulation():

    def __init__(self, attentionPoint: AttentionPoint, view):
        self.view = view
        self.attentionPointInitialState = deepcopy(attentionPoint)
        self.attentionPoint = attentionPoint

        self.console = Console()

        self.running = False
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.simulationThread = None

    def start(self, runChronometer=True):

        if runChronometer:
            self.running = True
            self.keyListener = kb.Listener(self.keypress)
            # self.simulationThread = threading.Thread(target=self.printInfo, daemon=True)

            self.keyListener.start()
            # self.simulationThread.start()

            while self.running:
                self.attentionPoint.elapsedOneSecond()
                self.console.print(self.getSimulationInfoAsStr())
                time.sleep(1)
                clear()
                self.updateTime()

            print(' terminé')
        else:
            self._evaluteStateImmediately()

    def stop(self):
        self.running = False
        # self.simulationThread.join()
        self.keyListener.stop()

    def _evaluteStateImmediately(self):
        # Begin counter from last cronomter value
        pass

    def getSimulationInfoAsStr(self):
        return f"""
        
        {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}
        Presione ESC para detener la simulación

        {self.attentionPoint.getAsStr()}

        {self.attentionPoint.getSimulationPropsAsStr()}
        """

    def keypress(self, key):
        if key == kb.Key.esc:
            self.stop()

    def updateTime(self):
        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1
