from jsonModel import InOutModel

class Room:
    def __init__(self, nome):
        self.nome = nome
        self.inputs = []
        self.outputs = []
        self.temperatura = 0
        self.humidade = 0
        self.contagem = InOutModel(None, None, 0, 0)

    def addInput(self, input: InOutModel):
        self.inputs.append(input)

    def addOutput(self, output: InOutModel):
        self.outputs.append(output)

    def setTemperatura(self, temperatura):
        self.temperatura = temperatura

    def setHumidade(self, humidade):
        self.humidade = humidade

    def setContagem(self, contagem):
        self.contagem = contagem

