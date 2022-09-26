
class Desktop():

    def __init__(self, id, identification, attendant):
        self.id = id
        self.identification = identification
        self.attendant = attendant
        self.initSimulationProps()

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Identificación: " + self.identification + "\n- Encargado: " + self.attendant + "\n"

    def initSimulationProps(self):
        self.averageAttentionTime = 0
        self.maximumAttentionTime = 0
        self.minimumAttentionTime = 0
        self.recalculateSimulationProps()

    def recalculateSimulationProps(self):
        pass
