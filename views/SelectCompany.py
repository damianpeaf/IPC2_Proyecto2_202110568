from re import X
from rich.console import Console
import inquirer
from data.Data import Data

from utils.clear import clear
from views.LoadFile import LoadFile
from views.SimulationView import SimulationView


class SelectCompany():

    def __init__(self) -> None:
        self.console = Console()
        self.show()

    def show(self):

        questions = [
            inquirer.List('action',
                          message="¿Qué empresa deseas simular?",
                          choices=['0. Regresar al menu principal'] + Data.getCompanyChoices(),
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 0:
            from views.MainMenu import MainMenu
            MainMenu()
            return
        else:
            self.selectedCompany = Data.companies.getItem(selectedOption - 1)
            self.console.print(f'Has seleccionado la empresa: {self.selectedCompany.name}', style='green')
            self.selectAttentionPoint()

    def selectAttentionPoint(self):
        questions = [
            inquirer.List('action',
                          message="¿Qué punto de atención deseas simular?",
                          choices=['0. Regresar al menu principal'] + Data.getAttentionPointChoices(self.selectedCompany),
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 0:
            from views.MainMenu import MainMenu
            MainMenu()
            return
        else:
            self.selectedAttentionPoint = self.selectedCompany.attentionPoints.getItem(selectedOption - 1)
            self.console.print(f'Has seleccionado el punto de atencion: {self.selectedAttentionPoint.name}', style='green')
            SimulationView(self.selectedAttentionPoint)
