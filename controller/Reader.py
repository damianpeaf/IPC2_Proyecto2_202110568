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

            for company in companiesTag:
                # * Basic info

                companyId = company.getAttribute('id')
                companyName = company.getElementsByTagName('nombre')[0].firstChild.nodeValue
                companyAbbreviaton = company.getElementsByTagName('abreviatura')[0].firstChild.nodeValue

                companyObj = Company(companyId, companyName, companyAbbreviaton)

                # * Attention points
                attentionPoints = company.getElementsByTagName('puntoAtencion')

                for attentionPoint in attentionPoints:
                    attentionPointId = attentionPoint.getAttribute('id')
                    attentionPointName = attentionPoint.getElementsByTagName('nombre')[0].firstChild.nodeValue
                    attentionPointAddress = attentionPoint.getElementsByTagName('direccion')[0].firstChild.nodeValue

                    attentionPointObj = AttentionPoint(attentionPointId, attentionPointName, attentionPointAddress)

                    # * Desktops
                    desktops = attentionPoint.getElementsByTagName('escritorio')

                    for desktop in desktops:
                        desktopId = desktop.getAttribute('id')
                        desktopIdentification = desktop.getElementsByTagName('identificacion')[0].firstChild.nodeValue
                        desktopAttendant = desktop.getElementsByTagName('encargado')[0].firstChild.nodeValue

                        attentionPointObj.inactiveDesktops.push(Desktop(desktopId, desktopIdentification, desktopAttendant))

                    companyObj.attentionPoints.addAtEnd(attentionPointObj)

                # * Available transactions
                availableTransactions = company.getElementsByTagName('transaccion')

                for transaction in availableTransactions:
                    transactionId = transaction.getAttribute('id')
                    transactionName = transaction.getElementsByTagName('nombre')[0].firstChild.nodeValue
                    transactionTimeOfAttention = transaction.getElementsByTagName('tiempoAtencion')[0].firstChild.nodeValue

                    companyObj.availableTransactions.addAtEnd(TransactionType(transactionId, transactionName, transactionTimeOfAttention))

                Data.addCompany(companyObj)

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

                # Related company
                posibleCompany = Data.searchCompanyById(companyId)
                if posibleCompany is None:
                    self.console.print('La empresa con id: ' + companyId + ' no existe', style='bold red')
                    continue
                posibleAttentionPoint = Data.searchAttentionPointById(attentionPointId, posibleCompany)

                # Related attention point
                if posibleAttentionPoint is None:
                    self.console.print('El punto de atención con id: ' + attentionPointId + ' no existe', style='bold red')
                    continue

                desktopTag = config.getElementsByTagName('escritorio')

                # * Active desktops

                for desktop in desktopTag:
                    desktopId = desktop.getAttribute('idEscritorio')
                    posibleDesktop = Data.searchInactiveDesktopById(desktopId, posibleAttentionPoint)

                    if posibleDesktop is None:
                        self.console.print('El escritorio con id: ' + desktopId + ' no existe dentro de los escritorios inactivos', style='bold red')
                        continue

                    posibleAttentionPoint.inactiveDesktops.popNode(posibleDesktop)
                    posibleAttentionPoint.activeDesktops.push(posibleDesktop)

                # * Clients

                clientsTag = config.getElementsByTagName('cliente')

                for client in clientsTag:
                    clientId = client.getAttribute('dpi')
                    clientName = client.getElementsByTagName('nombre')[0].firstChild.nodeValue

                    clientObj = Client(clientId, clientName)

                    # * Client transactions

                    clientTransactionsTag = client.getElementsByTagName('transaccion')

                    for transaction in clientTransactionsTag:
                        transactionTypeId = transaction.getAttribute('idTransaccion')
                        transactionQuantity = transaction.getAttribute('cantidad')

                        posibleTransactionType = Data.searchTransactionTypeById(transactionTypeId, posibleCompany)

                        if posibleTransactionType is None:
                            self.console.print('La transacción con id: ' + transactionTypeId + ' no existe en la empresa ' + posibleCompany.name, style='bold red')
                            continue

                        clientObj.transactions.addAtEnd(Transaction(posibleTransactionType, transactionQuantity))

                    posibleCompany.clients.enqueue(clientObj)

            aw = Data.companies
            return True
        except Exception as e:
            self.console.print(e, style='bold red')
            return False
