from rich.console import Console
from rich.table import Table
import inquirer
from data.Data import Data

from utils.clear import clear


class ListCompanies():

    def __init__(self):
        self.console = Console()
        self.show()

    def show(self):

        self.console.print('Informaciones de las empresas', style='bold blue')

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Id", width=10)
        table.add_column("Nombre", width=10)
        table.add_column("Abreviatura", width=7)
        table.add_column("Puntos de atención", width=25)
        table.add_column("Transacciones", width=25)

        for i in range(0, Data.companies.size):
            company = Data.companies.getItem(i)
            table.add_row(
                company.id,
                company.name,
                company.abbreviaton,
                company.getAtentionPointsAsStr(),
                company.getAvailableTransactions(),
            )

        self.console.print(table)

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. regresar'
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

        self.show()
