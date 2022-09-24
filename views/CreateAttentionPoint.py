from rich.console import Console
from rich.table import Table
import inquirer
from classes.AttentionPoint import AttentionPoint
from classes.Company import Company
from classes.Desktop import Desktop

from utils.clear import clear


class CreateAttentionPoint():

    def __init__(self, createdCompany: Company):
        self.console = Console()
        self.createdCompany = createdCompany
        self.show()

    def show(self):

        self.console.print('Creación de punto de atención', style='bold blue')

        questions = [
            inquirer.Text('id', message="Id del punto de atención"),
            inquirer.Text('name', message="Nombre del punto de atención"),
            inquirer.Text('address', message="Dirección del punto de atención"),
        ]

        answers = inquirer.prompt(questions)
        self.createdAtentionPoint = AttentionPoint(answers['id'], answers['name'], answers['address'])
        clear()
        self.console.print('Punto de atención creado', style='green')
        self.customizeAttentionPoint()

    def createDesktop(self, active: bool):
        # * Create a new desktop
        questions = [
            inquirer.Text('id', message="Id del escritorio"),
            inquirer.Text('identification', message="Identificacion del escritorio"),
            inquirer.Text('attendant', message="Encargado del escritorio"),
        ]

        answers = inquirer.prompt(questions)

        createdDesktop = Desktop(answers['id'], answers['identification'], answers['attendant'])

        if active:
            self.createdAtentionPoint.activeDesktops.push(createdDesktop)
        else:
            self.createdAtentionPoint.inactiveDesktops.push(createdDesktop)

        clear()
        self.console.print('Escritorio creado', style='bold green')
        self.customizeAttentionPoint()

    def customizeAttentionPoint(self):
        # * Menu of actions to do with the created company

        # attention point info
        self.console.print('Información del punto de atención', style='bold green')
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Id", width=5)
        table.add_column("Nombre", width=10)
        table.add_column("Direccion", width=10)
        table.add_column("Escritorios activos", width=20)
        table.add_column("Escritorios inactivos", width=20)
        table.add_row(
            self.createdAtentionPoint.id,
            self.createdAtentionPoint.name,
            self.createdAtentionPoint.address,
            self.createdAtentionPoint.getActiveDesktopsAsStr(),
            self.createdAtentionPoint.getInactiveDesktopsAsStr(),
        )
        self.console.print(table)

        self.console.print('Personalización del punto de atención', style='bold blue')
        questions = [
            inquirer.List('action',
                          message="¿Qué deseas crear con este punto de atencion?",
                          choices=['1. Crear escritorio activo',
                                   '2. Crear escritorio inactivo',
                                   '3. Salir y guardar',
                                   '4. Salir sin guardar',
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            self.createDesktop(True)
            return
        elif selectedOption == 2:
            self.createDesktop(False)
            return
        elif selectedOption == 3:
            from views.CreateCompany import CreateCompany
            self.createdCompany.attentionPoints.addAtEnd(self.createdAtentionPoint)
            c = CreateCompany(self.createdCompany)
            c.customizeCompany()
            return
        elif selectedOption == 4:
            from views.CreateCompany import CreateCompany
            c = CreateCompany(self.createdCompany)
            c.customizeCompany()
            return

        self.customizeAttentionPoint()
