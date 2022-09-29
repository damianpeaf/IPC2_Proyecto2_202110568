

from classes.AttentionPoint import AttentionPoint
from classes.Company import Company
from core.SimpleList import SimpleList


class Data():

    companies = SimpleList[Company]()

    @classmethod
    def resetData(cls):
        cls.companies.clear()

    @classmethod
    def addCompany(cls, company: Company):
        cls.companies.addAtEnd(company)

    @classmethod
    def searchCompanyById(cls, companyId: str):

        for index in range(0, cls.companies.size):
            evalCompany = cls.companies.getItem(index)
            if evalCompany.id == companyId:
                return evalCompany
        return None

    @classmethod
    def searchAttentionPointById(cls, attentionPointId: str, company: Company):

        for index in range(0, company.attentionPoints.size):
            evalAttentionPoint = company.attentionPoints.getItem(index)
            if evalAttentionPoint.id == attentionPointId:
                return evalAttentionPoint
        return None

    @classmethod
    def searchInactiveDesktopById(cls, desktopId: str, attentionPoint: AttentionPoint):

        for index in range(0, attentionPoint.inactiveDesktops.size):
            evalDesktop = attentionPoint.inactiveDesktops.getItem(index)
            if evalDesktop.id == desktopId:
                return evalDesktop
        return None

    @classmethod
    def searchTransactionTypeById(cls, transactionTypeId: str, company: Company):
        for index in range(0, company.availableTransactions.size):
            evalTransactionType = company.availableTransactions.getItem(index)
            if evalTransactionType.id == transactionTypeId:
                return evalTransactionType
        return None

    @classmethod
    def getCompanyChoices(cls):
        choices = []
        for index in range(0, cls.companies.size):
            evalCompany = cls.companies.getItem(index)
            choices.append(f"{str(index+1)} - {evalCompany.name}")
        return choices

    @staticmethod
    def getAttentionPointChoices(company: Company):
        choices = []
        for index in range(0, company.attentionPoints.size):
            evalAttentionPoint = company.attentionPoints.getItem(index)
            choices.append(f"{str(index+1)} - {evalAttentionPoint.name}")
        return choices

    @staticmethod
    def getTransactionTypesChoices(company: Company):
        choices = []

        for index in range(0, company.availableTransactions.size):
            evalTransactionType = company.availableTransactions.getItem(index)
            choices.append(f"{str(index+1)}. - {evalTransactionType.name}")
        return choices

    @staticmethod
    def getTransactionTypeByIndex(company: Company, index: int):
        return company.availableTransactions.getItem(index)
