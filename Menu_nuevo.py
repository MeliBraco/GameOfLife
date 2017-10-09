from GameOfLife.TableroDeJuego import TableroDeJuego
from Excepciones.NumeroFueraDeRango import NumeroFueraDeRango
from Excepciones.PatronInvalido import PatronInvalido
from Excepciones.TipoDeValorIncorrecto import TipoDeValorIncorrecto
from Excepciones.ClaveInexistente import ClaveInexistente
from GameOfLife.Persistencia import Persistencia
from Combinations.combination import combinations
import sys
import time

class Menu_nuevo(object):

    def menu(self):
        while True:
            try:
                self.choice = self.input(self.leer_teclado('Ingrese modo de juego: \n' '1- Modo normal \n'
                                                             '2- Modo vida estatica \n' '3- Salir \n'))
                self.tablero = TableroDeJuego(0,0)

                if self.choice == 1:
                    '''MODO NORMAL'''
                    self.crear_tablero()
                elif self.choice == 2:
                    try:
                        '''MODO DE VIDA ESTATICA'''
                        self.crear_tablero()
                    except PatronInvalido as e:
                        print(e.get_msg())
                elif self.choice == 3:
                    self.__exit()
                    break
                else:
                     raise NumeroFueraDeRango


            except NumeroFueraDeRango as e:
                print(e.get_msg(), '\n')


    def crear_tablero(self):

        while True:
            try:
                choice2 = self.input(self.leer_teclado('Elija una opción: \n' '1- Crear tablero al azar \n'
                                      '2- Crear tablero manualmente \n' '3- Cargar tablero \n' '4- Menu principal \n' '5-Salir \n'))

                if choice2 == 1:
                    '''TABLERO AL AZAR'''

                    self.fila = self.input(self.leer_teclado("ingrese la cantidad de filas: "))
                    self.columna = self.input(self.leer_teclado("ingrese la cantidad de columnas: "))

                    while True:
                        try:
                            self.tablero = TableroDeJuego(self.fila, self.columna)
                            cantidad_celulas_vivas = self.input(self.leer_teclado('Ingrese la cantidad de celulas vivas:'))
                            print()
                            self.tablero.inicializar_tablero_random(cantidad_celulas_vivas)

                            self.dimencion_de_tablero = self.fila * self.columna
                            self.patrones = cantidad_celulas_vivas

                            print("TABLERO INICIAL:")
                            print(self.tablero.imprimir_tablero())

                            if self.choice == 1:
                                self.modo_normal()
                            elif self.choice == 2:
                                self.modo_estatico()
                            break

                        except IndexError:
                            print('La cantidad de celdas vivas tiene que ser menor a  ' + str(
                                len(self.tablero.matriz) * len(self.tablero.matriz)), '\n')

                elif choice2 == 2:
                    '''TABLERO MANUAL'''

                    self.fila = self.input(self.leer_teclado("ingrese la cantidad de filas: "))
                    self.columna = self.input(self.leer_teclado("ingrese la cantidad de columnas: "))
                    self.tablero = TableroDeJuego(self.fila, self.columna)

                    cantidad_celulas_vivas = self.input(self.leer_teclado('ingrese la cantidad de celulas'))
                    self.dimencion_de_tablero = self.fila * self.columna
                    self.patrones = cantidad_celulas_vivas

                    while True:
                        try:
                            if cantidad_celulas_vivas < (self.fila*self.columna):
                                while cantidad_celulas_vivas > 0:
                                    fila = self.input(self.leer_teclado("ingrese fila: "))
                                    columna = self.input(self.leer_teclado("ingrese columna: "))
                                    estado = input('Ingrese estado */-:')
                                    try:
                                        self.tablero.inicializar_tablero_manual(fila,columna,estado)
                                    except IndexError:
                                        print("Por favor ingrese un numero de fila comprendido entre 0 y " + str(
                                        len(self.tablero.matriz)) + " y columna comprendido entre 0 y " + str(
                                        len(self.tablero.matriz[0])), '\n')
                                    except TypeError as e:
                                        print("Valor celular no valido")
                                    else:
                                        cantidad_celulas_vivas -= 1
                            else:
                                raise IndexError
                        except IndexError:
                                print('La cantidad de celdas vivas tiene que ser menor a  ' + str(
                                    len(self.tablero.matriz) * len(self.tablero.matriz)), '\n')

                        print()
                        print("TABLERO INICIAL:")
                        print(self.tablero.imprimir_tablero())

                        if self.choice == 1:
                            self.modo_normal()
                        elif self.choice == 2:
                            self.modo_estatico()
                        break

                elif choice2 == 3:
                    '''MODO NORMAL - CARGAR PARTIDA'''
                    while True:
                        ruta = input('Ingrese ruta del archivo: ')
                        clave = input('Ingrese una clave: ')
                        try:
                            self.tablero.matriz = Persistencia.recuperar_instancia(ruta,clave)
                            if self.choice == 1:
                                self.modo_normal()
                            elif self.choice == 2:
                                self.modo_estatico()
                            break
                        except ClaveInexistente as e:
                            print(e.get_msg())

                elif choice2 == 4:
                    '''MENU PRINCIPAL'''
                    return self.menu()
                elif choice2 == 5:
                    '''SALIR'''
                    self.__exit()
                else:
                    raise NumeroFueraDeRango
            except NumeroFueraDeRango as e:
                print(e.get_msg())


    def modo_normal(self):

        while True:
            try:
                self.tablero.imprimir_tablero()
                choice3 = self.input(self.leer_teclado('Ingrese una accion: \n' '1- Siguiente paso \n'
                                      '2- Modificar tablero \n' '3- Guardar tablero \n' '4- Volver \n'))

                if choice3 == 1:
                    '''MODO NORMAL - SIGUIENTE PASO'''

                    if self.tablero.contador_vidas_estaticas < 3:
                        self.tablero.mutar_celulas()
                        if self.tablero.contador_vidas_estaticas < 1:
                            print(self.tablero.imprimir_tablero())
                        else:
                            print('El tablero es vida estática. Fin del Juego\n')
                            while True:
                                self.__submenu()
                    else:
                        print('El tablero es vida estática. Fin del Juego\n')
                        while True:
                            self.__submenu()

                elif choice3 == 2:
                    '''MODIFICAR TABLERO'''

                    while True:
                        try:
                            fila = self.input(self.leer_teclado('Ingrese posicion de fila:'))
                            columna = self.input(self.leer_teclado('Ingrese posicion de columna:'))
                            valor = input('Ingrese "*" o "-":')
                            print()
                            self.tablero.inicializar_tablero_manual(fila, columna, valor)
                            print(self.tablero.imprimir_tablero())
                            break
                        except IndexError:
                            print("Por favor ingrese un numero de fila comprendido entre 0 y " + str(
                                len(self.tablero.matriz)) + "y columna comprendido entre 0 y " + str(
                                len(self.tablero.matriz[0]))), '\n'
                        except Exception:
                            print(Exception)

                elif choice3 == 3:
                    '''GUARDAR'''
                    self.__guardar()
                    break
                elif choice3 == 4:
                    ''' VOLVER MENU INTERNO'''
                    break
                else:
                    raise NumeroFueraDeRango

            except NumeroFueraDeRango as e:
                print(e.get_msg()), '\n'


    def modo_estatico(self):

        if (self.patrones <= self.dimencion_de_tablero):
            for x in combinations(range(self.dimencion_de_tablero), self.patrones):
                print(' ')
                print("En estas combinaciones" + " " + str(x))
                self.tablero.matriz = self.tablero.crear_matriz(self.fila, self.columna)
                self.tablero.contador_vidas_estaticas = 0
                self.tablero.diccionario_de_celdas = {}
                encontro = True
                contador = 0

                for posicion_tupla in x:  # este for rellena los vivos con las combinaciones
                    coordenadas = (posicion_tupla // len(self.tablero.matriz[0]), posicion_tupla % len(self.tablero.matriz[0]))
                    self.tablero.inicializar_tablero_manual(coordenadas[0], coordenadas[1], '*')

                while self.tablero.contador_vidas_estaticas < 3:
                    # LO QUE HACE ESTO ES MUTAR HASTA QUE QUEDE ESTATICO!!!
                    self.tablero.mutar_modo_vida_estatica()
                    contador += 1
                    if contador > 30:
                        encontro = False
                        break

                if (encontro == False):
                    print(self.tablero.imprimir_tablero())
                else:
                    print("Se encontro este tablero estatico: ")
                    print(self.tablero.imprimir_tablero())
                    break

                time.sleep(2.0)
        else:
            raise PatronInvalido

        while True:
            self.__submenu()



    def leer_entero(self, entrada):
        while True:
            try:
                if type(entrada) == int:
                    return entrada
                else:
                    raise Exception
            except Exception:
                print('Por favor ingrese un numero entero')
                break

    def input(self,entrada):
        if type(entrada) == int:
            return entrada
        else:
            raise TipoDeValorIncorrecto

    def leer_teclado(self, texto):
        while True:
            try:
                ingresado = eval(input(texto))
                if (ingresado == ''):
                    return None
                else:
                    return ingresado
            except (KeyboardInterrupt):
                print("KeyboardInterrupt")
            except (SyntaxError):
                print("Valor invalido")
            except (EOFError):
                print("EOFError")
            except (NameError):
                print("Debe ingresar un numero entero")


    def __submenu(self):
        submenu = self.input(self.leer_teclado('1- Guardar \n' '2- Menu Principal \n' '3- Salir\n'))
        try:
            if submenu == 1:
                self.__guardar()
            elif submenu == 2:
                return self.menu()
            elif submenu == 3:
                self.__exit()
            else:
                raise NumeroFueraDeRango

        except NumeroFueraDeRango as e:
            print(e.get_msg()), '\n'

    def __guardar(self):

        '''GUARDAR TABLERO'''

        tablero = self.tablero.matriz
        ruta = input('Ingrese la ruta del archivo:')
        clave = input('Ingrese una clave:')
        Persistencia.almacenar_instancia(ruta, tablero, clave)

        print("JUEGO GUARDADO")
        print()
        self.__exit()

    def __exit(self):
        sys.exit("El Juego finalizo con exito")





if __name__ == '__main__':
    Menu_nuevo().menu()