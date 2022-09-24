from rich.console import Console
from rich.table import Table
import inquirer
from classes.Company import Company
from classes.TransactionType import TransactionType
from data.Data import Data

from utils.clear import clear
from views.CreateAttentionPoint import CreateAttentionPoint


class CreateCompany():

    def __init__(self, createdCompany: Company = None):
        self.console = Console()
        self.createdCompany = createdCompany

    def init(self):

        self.console.print('Creación de empresa', style='bold blue')

        questions = [
            inquirer.Text('id', message="Id de la compañía"),
            inquirer.Text('name', message="Nombre de la compañía"),
            inquirer.Text('abbreviaton', message="Abreviatura de la compañía"),
        ]

        answers = inquirer.prompt(questions)
        self.createdCompany = Company(answers['id'], answers['name'], answers['abbreviaton'])
        clear()
        self.console.print('Empresa creada', style='green')
        self.customizeCompany()

    def customizeCompany(self):
        # * Menu of actions to do with the created company

        # company info
        self.console.print('Información de la empresa', style='bold green')
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Id", width=5)
        table.add_column("Nombre", width=10)
        table.add_column("Abreviatura", width=7)
        table.add_column("Puntos de atención", width=25)
        table.add_column("Transacciones", width=25)
        table.add_row(
            self.createdCompany.id,
            self.createdCompany.name,
            self.createdCompany.abbreviaton,
            self.createdCompany.getAtentionPointsAsStr(),
            self.createdCompany.getAvailableTransactions(),
        )
        self.console.print(table)

        self.console.print('Personalización de empresa', style='bold blue')
        questions = [
            inquirer.List('action',
                          message="¿Qué deseas crear con esta empresa?",
                          choices=['1. Crear puntos de atención',
                                   '2. Crear transacciones',
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
            CreateAttentionPoint(self.createdCompany)
            return
        elif selectedOption == 2:
            self.createTransaction()
            return
        elif selectedOption == 3:
            Data.addCompany(self.createdCompany)
            self.console.print('Empresa guardada', style='green')
            from views.CompanyActions import CompanyActions
            CompanyActions()
        elif selectedOption == 4:
            from views.CompanyActions import CompanyActions
            CompanyActions()

        self.customizeCompany()

    def createTransaction(self):
        self.console.print('Creación de transaccion', style='bold blue')

        questions = [
            inquirer.Text('id', message="Id de la transaccion"),
            inquirer.Text('name', message="Nombre de la transaccion"),
            inquirer.Text('timeOfAttention', message="Tiempo de atención"),
        ]

        answers = inquirer.prompt(questions)
        self.createdTransactionType = TransactionType(answers['id'], answers['name'], answers['timeOfAttention'])
        self.console.print('transaccion creada', style='green')

        self.createdCompany.availableTransactions.addAtStart(self.createdTransactionType)
        self.customizeCompany()
