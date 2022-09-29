from classes.Transaction import Transaction
from core.SimpleList import SimpleList


class Client():

    def __init__(self, dpi, name):
        self.name = name
        self.dpi = dpi
        self.transactions = SimpleList[Transaction]()
        self.waitedTime = 0

    def addTransaction(self, transaction: Transaction):
        self.transactions.addAtEnd(transaction)

    def waitOneSecond(self):
        self.waitedTime += (1/60)

    def getTransactionsAsStr(self):

        if self.transactions.size == 0:
            return " No hay mas transacciones "

        result = ""
        for i in range(0, self.transactions.size):
            transaction = self.transactions.getItem(i)
            formatedNumber = "{:.2f}".format(transaction.pendingTime)
            result += f"Transaccion: {transaction.transactionType.name} - Tiempo restante - {str(formatedNumber)} minutos\n\t"

        return result

    def getTransactionTotalTimeAsStr(self):
        result = 0
        for i in range(0, self.transactions.size):
            transaction = self.transactions.getItem(i)
            result += transaction.transactionType.timeOfAttention

        formatedTime = "{:.2f}".format(result)

        return formatedTime
