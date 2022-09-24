from rich.console import Console
import inquirer
from controller.Reader import Reader
from data.Data import Data

from utils.clear import clear


class LoadFile():

    def __init__(self, fileType: int):
        self.console = Console()
        self.fileType = fileType
        self.show()

    def readFile(self, path):
        reader = Reader(path)

        ok = None
        if self.fileType == 1:
            ok = reader.readCompaniesFile()
        elif self.fileType == 2:
            ok = reader.readConfigFile()

        if ok:
            self.console.print("Archivo cargado correctamente", style="bold green")
        else:
            self.console.print("Error al cargar el archivo", style="bold red")

        from views.CompanyActions import CompanyActions
        CompanyActions()

    def show(self):

        questions = [
            inquirer.Path('action',
                          message="¿Que archivo deseas cargar?",
                          path_type=inquirer.Path.FILE,
                          ),
        ]

        answers = inquirer.prompt(questions)
        path = answers['action']
        self.readFile(path)
