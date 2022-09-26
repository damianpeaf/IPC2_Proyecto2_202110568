from rich.console import Console
import inquirer

from utils.clear import clear


class MainMenu():

    def __init__(self) -> None:
        self.console = Console()
        self.show()

    def show(self):
        self.console.print(
            'Proyecto 2 - IPC2 - Damián Ignacio Peña Afre - 202110568', style='bold cyan ')

        self.console.print(
            'Bienvenido al sistema de simulación de colas', style='green')

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. Configurar empresas',
                                   '2. Seleccionar Empresa para simular',
                                   '3. Salir'
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            from views.CompanyActions import CompanyActions
            CompanyActions()
        elif selectedOption == 2:
            from views.SelectCompany import SelectCompany
            SelectCompany()
        elif selectedOption == 3:
            self.console.print('Hasta pronto :)', style='red')
            exit()
        else:
            self.console.print('Opción no valida', style='red')
            self.show()
