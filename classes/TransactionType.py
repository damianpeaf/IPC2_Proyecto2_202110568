

class TransactionType():

    def __init__(self, id, name: str, timeOfAttention: float):
        self.id = id
        self.name = name
        # * Time of attention in minutes
        # ? str
        self.timeOfAttention = timeOfAttention

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Nombre: " + self.name + "\n- Tiempo de atención: " + str(self.timeOfAttention) + " minutos\n"
