import pprint
import copy
import random
from gen import Gen


if __name__ == "__main__":
    mtx = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(8)]
    dirs = [[a * x, a * y] for a in range(1, len(mtx)) for x, y in [ (1, -1), (1, 1), (-1, 1), (-1, -1), (0, -1), (0, 1), (-1, 0), (1, 0)]]
    cromosoma = [
        Gen("010"),
        Gen("100"),
        Gen("000"),
        Gen("110"),
        Gen("001"),
        Gen("011"),
        Gen("101"),
        Gen("001"),
    ]

    def getBinario(binario):
        for objeto in cromosoma:
            if objeto.binario == binario:
                return objeto

    def printGenes():
        for gen in cromosoma:
            print(gen)
    
    def printCromosoma():
        concat = ""
        for gen in cromosoma:
            concat += gen.binario + "-"
        concat = concat[:-1]
        print(concat)

    def actualizar_tablero():
        global mtx
        mtx = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(8)]
        for index, value in enumerate(cromosoma):
            mtx[value.valor][index] = 1

    def colisiones(fila, columna):
        def is_valid(x, y):
            if 0 <= fila + y < len(mtx) and 0 <= columna + x < len(mtx[0]):
                return True

        colision = 0
        for x, y in dirs:
            if is_valid(x, y) and mtx[fila + y][columna + x] == 1:
                colision += 1
        return colision

    def checkObjetivo():
        for columna, gen in enumerate(cromosoma):
            if colisiones(gen.valor, columna) != 0:
                return False
        return True
        # print(f"Total de colisiones la reina en la posicion [columna = {columna}, fila = {gen.valor}] = {colisiones(gen.valor, columna)}")

    def cruzamiento():
        def custom_pos():
            return random.randint(1, len(cromosoma[0].binario) - 1)

        for index in range(0, len(cromosoma), 2):
            pos = custom_pos()
            copy_binario = cromosoma[index].binario

            cromosoma[index].binario = (
                cromosoma[index].binario[:pos] + cromosoma[index + 1].binario[pos:]
            )
            cromosoma[index + 1].binario = (
                cromosoma[index + 1].binario[:pos] + copy_binario[pos:]
            )

    def mutacion(mutar):
        change = random.randint(0, len(cromosoma[0].binario) - 1)
        contrario = not bool(int(cromosoma[mutar].binario[change : change + 1]))
        # copy_binary = cromosoma[mutar].binario
        cromosoma[mutar].binario = (
            cromosoma[mutar].binario[:change]
            + str(int(contrario))
            + cromosoma[mutar].binario[change + 1 :]
        )

    contador = 1
    while True:
        contador += 1
        actualizar_tablero()
        for columna, gen in enumerate(cromosoma):
            gen.setFitness(colisiones(gen.valor, columna))
        if checkObjetivo():
            print(f">>>> [CROMOSOMA ENCONTRADO] GENERACION:{contador} <<<<")
            # printGenes()
            printCromosoma()
            pprint.pprint(mtx)
            break
        else:
            # el mejor hasta arriba, el peor hasta abajo
            mejor = min(enumerate(cromosoma), key=lambda x: x[1].fitness)
            cromosoma.pop(mejor[0])
            peor = max(enumerate(cromosoma), key=lambda x: x[1].fitness)
            cromosoma.pop(peor[0])
            cromosoma.insert(0, mejor[1])
            cromosoma.insert(len(cromosoma), peor[1])
            if cromosoma[-1].fitness != mejor[1].fitness:
                cromosoma[-1] = copy.copy(
                    mejor[1]
                )  # el peor es sustituido por el mejor

            cruzamiento()

            probabilidad_mutacion = 20
            probabilidad_mutacion_actual = probabilidad_mutacion * 0.01

            for i, cromo in enumerate(cromosoma):
                if cromo.fitness >= 1 and random.random() < probabilidad_mutacion_actual:
                    mutacion(i)

            continue

        break
