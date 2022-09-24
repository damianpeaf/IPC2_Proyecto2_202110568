

class TransactionType():

    def __init__(self, id, name: str, timeOfAttention: float):
        self.id = id
        self.name = name
        # * Time of attention in minutes
        # ? str
        self.timeOfAttention = timeOfAttention
