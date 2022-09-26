

from controller.Simulation import Simulation
from rich.console import Console
import inquirer

from utils.clear import clear


class SimulationView():

    def __init__(self, attentionPoint):
        self.console = Console()
        self.attentionPoint = attentionPoint
        self.simulation = Simulation(self.attentionPoint, self)
        self.init()

    def init(self):
        clear()

        self.console.print('Simulación', style='bold red underline')

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. Empezar simulación',
                                   '2. Reiniciar simulación',
                                   '3. Terminar simulación',
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            self.simulation.start(True)
