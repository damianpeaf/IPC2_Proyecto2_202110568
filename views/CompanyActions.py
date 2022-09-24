from rich.console import Console
import inquirer
from data.Data import Data

from utils.clear import clear
from views.LoadFile import LoadFile


class CompanyActions():

    def __init__(self) -> None:
        self.console = Console()
        self.show()

    def cleanSystem(self):
        Data.resetData()
        self.console.print('Sistema limpiado', style='green')
        self.show()

    def show(self):

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. Limpiar sistema',
                                   '2. Cargar un archivo (incremental)',
                                   '3. Crear una nueva empresa',
                                   '4. Cargar archivo de configuración inicial',
                                   '5. Regresar al menu principal',
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            self.cleanSystem()
        elif selectedOption == 2:
            LoadFile(1)
            return
        elif selectedOption == 3:
            self.console.print('Crear una nueva empresa')
        elif selectedOption == 4:
            LoadFile(2)
            return
        elif selectedOption == 5:
            from views.MainMenu import MainMenu
            MainMenu()
            return

        self.show()
