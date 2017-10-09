import shelve
from Excepciones.ClaveInexistente import ClaveInexistente

class Persistencia(object):

    def almacenar_instancia(archivo, objects, clave):
        db = shelve.open(archivo)
        db[clave] = objects
        db.close()


    def recuperar_diccionario(archivo):
        lista = []
        fichero = shelve.open(archivo)
        for clave in fichero:
            lista.append(fichero[clave])

        return lista


    def recuperar_instancia(archivo, clave):
        fichero = shelve.open(archivo)
        if clave not in fichero:
            raise ClaveInexistente
        else:
            for x in fichero:
                if (x == clave):
                    return (fichero[x])