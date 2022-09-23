

from typing import List
from classes.Company import Company


class Data():

    companies: List[Company] = []

    @classmethod
    def resetData(cls):
        cls.companies = []

    @classmethod
    def addCompany(cls, company: Company):
        cls.companies.append(company)
