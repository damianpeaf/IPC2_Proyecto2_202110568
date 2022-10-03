

from classes.Client import Client
from classes.Transaction import Transaction
from controller.Simulation import Simulation
from rich.console import Console
import inquirer
from data.Data import Data

from utils.clear import clear
from views.MainMenu import MainMenu


class SimulationView():

    def __init__(self, attentionPoint, company):
        self.console = Console()
        self.attentionPoint = attentionPoint
        self.company = company
        self.simulation = Simulation(self.attentionPoint)
        self.message = None
        self.init()

    def init(self):
        clear()

        self.console.print('Simulación', style='bold red underline')

        self.console.print(self.simulation.getSimulationInfoAsStr())

        if self.message:
            self.console.print(self.message, style='bold blue')
            self.message = None

        # ? Actual state
        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. Empezar/reanudar simulación',
                                   '2. Activar escritorios',
                                   '3. Desactivar escritorios',
                                   '4. Atender cliente',
                                   '5. Solicitar atención',
                                   '6. Simular todo',
                                   '7. Generar reporte',
                                   '8. Terminar simulación',
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            self.simulation.start(True)
        elif selectedOption == 2:
            if self.simulation.activateDesktop():
                self.message = 'Se ha activó un escritorio'
            else:
                self.message = 'No se hay ningun escritorio para activar'
        elif selectedOption == 3:
            self.simulation.deactivateDesktop()
            self.message = 'El proximo escritorio que se desocupe se desactivara'

        elif selectedOption == 4:
            self.simulation.endNextClientTransaction()
            self.message = 'Se ha atendieron todas las transacciones del proximo cliente en la cola'
        elif selectedOption == 5:
            self.createClient()
        elif selectedOption == 6:
            self.simulation.start(False)
        elif selectedOption == 7:
            self.simulation.createNewReport()
        elif selectedOption == 8:
            MainMenu()

        self.init()

    def createClient(self):
        self.console.print('Creación de punto de cliente', style='bold blue')

        questions = [
            inquirer.Text('dpi', message="DPI del cliente"),
            inquirer.Text('name', message="Nombre del cliente"),
        ]

        answers = inquirer.prompt(questions)
        self.createdClient = Client(answers['dpi'], answers['name'])
        clear()
        self.console.print('Cliente creado', style='green')
        self.customizeClientTransactions()

    def customizeClientTransactions(self):
        self.console.print('Personalización de transacciones', style='bold blue')

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['1. Añadir transaccion',
                                   '2. Salir sin guardar',
                                   '3. Salir y guardar',
                                   ],
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 1:
            self.addTransactionToClient()
        elif selectedOption == 2:
            self.message = "Se ha cancelado la creación del cliente"
            self.init()
        elif selectedOption == 3:
            self.message = f"Se ha creado el cliente se espera que lo atiendan en {str(round(self.simulation.attentionPoint.averageWaitingTime,2))} minutos"
            self.simulation.createClient(self.createdClient)
            self.init()

    def addTransactionToClient(self):
        self.console.print('Añadir transacción', style='bold blue')

        questions = [
            inquirer.List('action',
                          message="¿Qué accion deseas realizar?",
                          choices=['0. Regresar']+Data.getTransactionTypesChoices(self.company),
                          carousel=True
                          ),
        ]

        answers = inquirer.prompt(questions)
        selectedOption: int = int(answers['action'][0])
        clear()

        if selectedOption == 0:
            self.customizeClientTransactions()
        else:
            transascionType = Data.getTransactionTypeByIndex(self.company, selectedOption-1)

            questions = [
                inquirer.Text('quantity', message="¿Cantidad?"),
            ]

            answers = inquirer.prompt(questions)
            self.createdClient.addTransaction(Transaction(transascionType, answers['quantity']))
            clear()
            self.console.print('Transaccion añadida', style='green')
            self.customizeClientTransactions()
