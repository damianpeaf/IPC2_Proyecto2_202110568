from rich.console import Console
from copy import deepcopy
from classes.AttentionPoint import AttentionPoint
import time
from classes.Client import Client
from utils.clear import clear
from pynput import keyboard as kb


class Simulation():

    def __init__(self, attentionPoint: AttentionPoint):
        self.attentionPointInitialState = deepcopy(attentionPoint)
        self.attentionPoint = attentionPoint

        self.console = Console()
        self.reportNumber = 0

        self.running = False
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.simulationThread = None

    def createNewReport(self):
        from controller.GraphvizParser import GraphvizParser
        self.reportNumber += 1
        GraphvizParser(self).createPDF()
        return "Reporte generado"

    def start(self, runDelay=True):

        self.keyListener = kb.Listener(self.keypress)
        self.keyListener.start()
        self.evalAutoStop()

        if runDelay:

            while self.running:
                self.attentionPoint.elapsedOneSecond()
                self.console.print(self.getSimulationInfoAsStr())
                self.updateTime()
                time.sleep(1)
                clear()
                if self.running:
                    self.evalAutoStop()
        else:
            while self.running:
                self.attentionPoint.elapsedOneSecond()
                self.updateTime()
                if self.running:
                    self.evalAutoStop()

    def evalAutoStop(self):
        # * Free desktops

        if self.attentionPoint.activeDesktops.size == 0:
            self.stop()

        isAttending = self.attentionPoint.isDesktopAttending()
        if isAttending or self.attentionPoint.clients.size > 0:
            self.running = True
        else:
            self.running = False

    def stop(self):
        self.running = False
        self.keyListener.stop()

    def createClient(self, client: Client):
        self.attentionPoint.addClient(client)

    def deactivateDesktop(self):
        self.attentionPoint.haveToDeactivateDesktop = True

    def activateDesktop(self):
        return self.attentionPoint.activateDesktop()

    def getChronometerAsStr(self):
        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'

    def endNextClientTransaction(self):
        self.attentionPoint.endNextClientTransaction(self.updateTime)

    def getSimulationInfoAsStr(self):
        return f"""
        {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}

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
