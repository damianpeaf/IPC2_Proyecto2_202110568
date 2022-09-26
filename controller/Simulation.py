
from rich.console import Console
from copy import deepcopy
import threading
from classes.AttentionPoint import AttentionPoint
from classes.Company import Company
from controller.Cronometer import Cronometer
import time

from utils.clear import clear

from pynput import keyboard as kb


class Simulation():

    def __init__(self, attentionPoint: AttentionPoint, view):
        self.view = view
        self.attentionPointInitialState = deepcopy(attentionPoint)
        self.attentionPoint = attentionPoint
        self.activeDesktops = self.attentionPoint.activeDesktops
        self.inactiveDesktops = self.attentionPoint.inactiveDesktops

        self.console = Console()

        self.running = False
        self.cronometer = Cronometer()

    def start(self, time=True):

        if time:
            self.keyListener = kb.Listener(self.keypress)
            self.simulationThread = threading.Thread(target=self.printInfo, daemon=True)

            self.running = True

            self.keyListener.start()
            self.cronometer.start()
            self.simulationThread.start()

            while self.cronometer.running:
                self._evaluateStateBySecond()
        else:
            self._evaluteStateImmediately()

    def stop(self):
        self.running = False
        self.simulationThread.join()
        self.keyListener.stop()
        self.cronometer.stop()
        from views.SimulationView import SimulationView
        SimulationView(self.view.attentionPoint)

    def _evaluateStateBySecond(self):
        pass

    def _evaluteStateImmediately(self):
        # Begin counter from last cronomter value
        pass

    def getSimulationInfoAsStr(self):
        return f"""{self.attentionPoint.getAsStr()}
        {self.cronometer.getCronomterAsStr()}
        Presione ESC para detener la simulación
        """

    def keypress(self, key):
        if key == kb.Key.esc:
            self.stop()

    def printInfo(self):

        while self.running and self.keyListener.is_alive():
            self.console.print(self.getSimulationInfoAsStr())
            time.sleep(1)
            clear()
