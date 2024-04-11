class Gen:
    def __init__(self, binario: str):
        self._binario = binario
        self.valor = self.binary2decimal()

    @property
    def binario(self):
        return self._binario

    @binario.setter
    def binario(self, value):
        if self._binario != value:
            self._binario = value
            self.valor = self.binary2decimal()

    def binary2decimal(self):
        return int(self._binario, 2)

    def setFitness(self, value):
        self.fitness = value

    def __str__(self):
        return f"Binario: {self.binario}, valor: {self.valor}, Fitness: {self.fitness}"
