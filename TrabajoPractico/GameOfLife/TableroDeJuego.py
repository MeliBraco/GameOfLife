import random
from Excepciones import ValorCelularNoValido
import time
#PEP-8

class TableroDeJuego(object):

    def __init__(self, numero_filas, numero_columnas):

        self.matriz = self.crear_matriz(numero_filas, numero_columnas)

        self.matriz_antigua = []
        self.contador_vidas_estaticas = 0
        self.diccionario_de_celdas = {}

    def crear_matriz(self, numero_filas, numero_columnas):
        matriz_nueva = []
        for i in range(numero_filas):
            matriz_nueva.append(['-'] * numero_columnas)
        return matriz_nueva

    def inicializar_tablero_random(self, numero_de_celdas_vivas):

        combinaciones = []

        if (numero_de_celdas_vivas <= len(self.matriz) * len(self.matriz[0])):
            for fila in range(len(self.matriz)):
                for columna in range(len(self.matriz[0])):
                    combinaciones.append((fila, columna))
            random.shuffle(combinaciones)
            for i in range(numero_de_celdas_vivas):
                combinacion_random = combinaciones.pop()
                self.matriz[combinacion_random[0]][combinacion_random[1]] = '*'
        else:
            raise IndexError

    def inicializar_tablero_manual(self, fila, columna, estado):

        if (fila > len(self.matriz) or columna > len(self.matriz[0])):
            raise IndexError
        elif (estado != '-' and estado != '*'):
            raise ValorCelularNoValido
        else:
            self.matriz[fila][columna] = estado
            self.contador_vidas_estaticas = 0

    def imprimir_tablero(self):
        juego = ''
        for fila in self.matriz:
            for celda in fila:
                juego += ' * ' if celda == '*' else ' - '
            juego += '\n'
        return juego

#_________________________________________________________________________________

    def mutar_celulas(self):

        matriz_actualizada = self.crear_matriz(len(self.matriz), len(self.matriz[0]))
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):

                self.__condiciones_de_mutacion(x,y,matriz_actualizada)

        self.matriz_antigua = self.matriz
        self.matriz = matriz_actualizada
        self.__vidas_estaticas()

    def __cantidad_de_vecinos(self, fila, columna):

        distancia_de_celdas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        celdas_vivas = 0
        for x, y in distancia_de_celdas:
            if (fila + x >= 0 and fila + x < len(self.matriz) and (columna + y >= 0 and columna + y < len(self.matriz[0]))):
                if (self.matriz[fila + x][columna + y] == '*'):
                    celdas_vivas += 1
        return celdas_vivas

    def __condiciones_de_mutacion(self,x,y,matriz_actualizada):

        if (self.matriz[x][y] == '-'):
            if (self.__cantidad_de_vecinos(x, y) == 3):
                matriz_actualizada[x][y] = '*'
        else:
            if self.__cantidad_de_vecinos(x, y) == 2 or self.__cantidad_de_vecinos(x, y) == 3:
                matriz_actualizada[x][y] = '*'
            elif self.__cantidad_de_vecinos(x, y) < 2 or self.__cantidad_de_vecinos(x, y) > 3:
                matriz_actualizada[x][y] = '-'


    def __vidas_estaticas(self):

        son_iguales = True
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[0])):
                if self.matriz[x][y] != self.matriz_antigua[x][y]:
                    son_iguales = False
        if son_iguales:
            self.contador_vidas_estaticas += 1
        else:
            self.contador_vidas_estaticas = 0


#_______________________________________________________________________

    def mutar_modo_vida_estatica(self):

        if self.diccionario_de_celdas == {}:  # Si el diccionario esta vacio, lo crea con todos ceros
            for x in range(len(self.matriz)):
                for y in range(len(self.matriz[x])):
                    self.diccionario_de_celdas[(x, y)] = 0

        self.mutar_celulas_no_estaticas()  # Llama al metodo para mutar
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[0])):
                if self.matriz[x][y] == self.matriz_antigua[x][y]:  # Si no hubo cambios en una celda, suma el contador
                    self.diccionario_de_celdas[(x, y)] = self.diccionario_de_celdas[(x, y)] + 1
                elif self.matriz[x][y] != self.matriz_antigua[x][y]:  # Si no es estatica y cambio, el contador vuelve a cero
                    self.diccionario_de_celdas[(x, y)] = 0


    def mutar_celulas_no_estaticas(self):
        matriz_actualizada = self.crear_matriz(len(self.matriz), len(
            self.matriz[0]))  # Crea matriz nueva a partir del tamaño de la original

        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):  # Recorre el tablero

                if self.diccionario_de_celdas[(x, y)] < 3:  # Si la celula no es estatica, se fija si puede mutar
                    if self.matriz[x][y] == '-':  # Si esta muerta, se fija si puede vivir
                        if self.__cantidad_de_vecinos(x, y) >= 3:
                            matriz_actualizada[x][y] = '*'
                    else:  # Si esta viva, se fija si sigue viva. De lo contrario se queda como muerta en la matriz actualizada
                        if self.__cantidad_de_vecinos(x, y) == 2 or self.__cantidad_de_vecinos(x, y) == 3:
                            matriz_actualizada[x][y] = '*'
                else:  # Si la celula es estatica, guarda la misma celda estatica en la nueva matriz
                    matriz_actualizada[x][y] = self.matriz[x][y]
        self.matriz_antigua = self.matriz
        self.matriz = matriz_actualizada
        self.__vidas_estaticas()







