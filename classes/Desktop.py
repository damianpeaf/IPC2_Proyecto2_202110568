
class Desktop():

    def __init__(self, id, identification, attendant):
        self.id = id
        self.identification = identification
        self.attendant = attendant

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Identificación: " + self.identification + "\n- Encargado: " + self.attendant + "\n"
