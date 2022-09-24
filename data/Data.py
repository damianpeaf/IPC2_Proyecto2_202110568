

from typing import List
from classes.AttentionPoint import AttentionPoint
from classes.Company import Company


class Data():

    companies: List[Company] = []

    @classmethod
    def resetData(cls):
        cls.companies = []

    @classmethod
    def addCompanies(cls, companies: List[Company]):
        cls.companies += companies

    @classmethod
    def searchCompanyById(cls, companyId: str):
        for company in cls.companies:
            if company.id == companyId:
                return company
        return None

    @classmethod
    def searchAttentionPointById(cls, attentionPointId: str, company: Company):

        for attentionPoint in company.attentionPoints:
            if attentionPoint.id == attentionPointId:
                return attentionPoint
        return None

    @classmethod
    def searchDesktopById(cls, desktopId: str, attentionPoint: AttentionPoint):
        for desktop in attentionPoint.desktops:
            if desktop.id == desktopId:
                return desktop
        return None

    @classmethod
    def searchTransactionTypeById(cls, transactionTypeId: str, company: Company):
        for transactionType in company.availableTransactions:
            if transactionType.id == transactionTypeId:
                return transactionType
        return None
