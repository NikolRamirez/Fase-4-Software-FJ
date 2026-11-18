#Software FJ - Sistema de gestión de clientes, servicios y reservas (POO, sin base de datos).
#Los datos viven en listas internas; el único archivo que se usa es logs.txt (eventos y errores).
#Para ejecutar: python software_fj.py
from abc import ABC, abstractmethod
from datetime import datetime

#Función para guardar eventos y errores en el archivo de logs.
#Si el archivo no se puede escribir, se avisa por pantalla y el programa sigue funcionando.
def registrar_log(nivel, mensaje):
    try:
        with open("logs.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {nivel} | {mensaje}\n")
    except OSError as error:
        print(f"   (No se pudo escribir en el log: {error})")


#Excepciones personalizadas, todas heredan de ErrorFJ.
class ErrorFJ(Exception):
    pass

class ClienteError(ErrorFJ):
    pass

class ServicioError(ErrorFJ):
    pass

class ServicioNoDisponibleError(ErrorFJ):
    pass

class ReservaError(ErrorFJ):
    pass

class OperacionNoPermitidaError(ErrorFJ):
    pass

class CalculoError(ErrorFJ):
    pass


#Clase abstracta que representa las entidades generales del sistema.
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def describir(self):
        pass
