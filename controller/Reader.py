from rich.console import Console
import xml.dom.minidom
from classes.AttentionPoint import AttentionPoint
from classes.Client import Client
from classes.Company import Company

from classes.Desktop import Desktop
from classes.Transaction import Transaction
from classes.TransactionType import TransactionType
from data.Data import Data


class Reader():

    def __init__(self, path: str):
        self.path = path.replace('\\', '/')
        self.console = Console()

    def readCompaniesFile(self):
        try:
            domTree = xml.dom.minidom.parse(self.path)
            group = domTree.documentElement

            companiesTag = group.getElementsByTagName('empresa')
            companies = []

            for company in companiesTag:
                # * Basic info
                companyId = company.getAttribute('id')
                companyName = company.getElementsByTagName('nombre')[0].firstChild.nodeValue
                companyAbbreviaton = company.getElementsByTagName('abreviatura')[0].firstChild.nodeValue

                # * Attention points
                attentionPoints = company.getElementsByTagName('puntoAtencion')
                companyAttentionPoints = []

                for attentionPoint in attentionPoints:
                    attentionPointId = attentionPoint.getAttribute('id')
                    attentionPointName = attentionPoint.getElementsByTagName('nombre')[0].firstChild.nodeValue
                    attentionPointAddress = attentionPoint.getElementsByTagName('direccion')[0].firstChild.nodeValue

                    # * Desktops
                    desktops = attentionPoint.getElementsByTagName('escritorio')
                    attentionPointDesktops = []

                    for desktop in desktops:
                        desktopId = desktop.getAttribute('id')
                        desktopIdentification = desktop.getElementsByTagName('identificacion')[0].firstChild.nodeValue
                        desktopAttendant = desktop.getElementsByTagName('encargado')[0].firstChild.nodeValue
                        attentionPointDesktops.append(Desktop(desktopId, desktopIdentification, desktopAttendant))

                    companyAttentionPoints.append(AttentionPoint(attentionPointId, attentionPointName, attentionPointAddress, attentionPointDesktops))

                # * Available transactions
                availableTransactions = company.getElementsByTagName('transaccion')
                companyAvailableTransactions = []

                for transaction in availableTransactions:
                    transactionId = transaction.getAttribute('id')
                    transactionName = transaction.getElementsByTagName('nombre')[0].firstChild.nodeValue
                    transactionTimeOfAttention = transaction.getElementsByTagName('tiempoAtencion')[0].firstChild.nodeValue
                    companyAvailableTransactions.append(TransactionType(transactionId, transactionName, transactionTimeOfAttention))

                companies.append(Company(companyId, companyName, companyAbbreviaton, companyAttentionPoints, companyAvailableTransactions))

                Data.addCompanies(companies)

            return True
        except Exception as e:
            self.console.print(e, style='bold red')
            return False

    def readConfigFile(self):
        try:
            domTree = xml.dom.minidom.parse(self.path)
            group = domTree.documentElement

            configTag = group.getElementsByTagName('configInicial')

            for config in configTag:
                companyId = config.getAttribute('idEmpresa')
                attentionPointId = config.getAttribute('idPunto')

                posibleCompany = Data.searchCompanyById(companyId)
                if posibleCompany is None:
                    self.console.print('La empresa con id: ' + companyId + ' no existe', style='bold red')
                    continue
                posibleAttentionPoint = Data.searchAttentionPointById(attentionPointId, posibleCompany)

                if posibleAttentionPoint is None:
                    self.console.print('El punto de atención con id: ' + attentionPointId + ' no existe', style='bold red')
                    continue

                desktopTag = config.getElementsByTagName('escritorio')

                # * Active desktops

                for desktop in desktopTag:
                    desktopId = desktop.getAttribute('idEscritorio')
                    posibleDesktop = Data.searchDesktopById(desktopId, posibleAttentionPoint)

                    if posibleDesktop is None:
                        self.console.print('El escritorio con id: ' + desktopId + ' no existe', style='bold red')
                        continue

                    posibleDesktop.isActive = True

                # * Clients

                clientsTag = config.getElementsByTagName('cliente')

                companyClients = []
                for client in clientsTag:
                    clientId = client.getAttribute('dpi')
                    clientName = client.getElementsByTagName('nombre')[0].firstChild.nodeValue

                    # * Client transactions

                    clientTransactionsTag = client.getElementsByTagName('transaccion')

                    clientTransactions = []
                    for transaction in clientTransactionsTag:
                        transactionTypeId = transaction.getAttribute('idTransaccion')
                        transactionQuantity = transaction.getAttribute('cantidad')

                        posibleTransactionType = Data.searchTransactionTypeById(transactionTypeId, posibleCompany)

                        if posibleTransactionType is None:
                            self.console.print('La transacción con id: ' + transactionTypeId + ' no existe en la empresa ' + posibleCompany.name, style='bold red')
                            continue

                        clientTransactions.append(Transaction(posibleTransactionType, transactionQuantity))

                    companyClients.append(Client(clientId, clientName, clientTransactions))

                posibleCompany.clients = companyClients

            aw = Data.companies
            return True
        except Exception as e:
            self.console.print_exception()
            self.console.print(e, style='bold red')
            return False
