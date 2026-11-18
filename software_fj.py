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


#Clase Cliente con atributos privados y validaciones.
class Cliente(Entidad):
    def __init__(self, id, nombre=None, email=None, telefono=None):
        super().__init__(id)
        if not nombre or not email or not telefono:
            raise ClienteError("Faltan datos del cliente.")
        if not isinstance(nombre, str) or not isinstance(email, str) or not isinstance(telefono, str):
            raise ClienteError("Nombre, email y teléfono deben ser texto.")
        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío.")
        partes = email.split("@")
        if " " in email or len(partes) != 2 or not partes[0] or "." not in partes[1]:
            raise ClienteError(f"Email inválido: {email}")
        if not telefono.isdigit() or not 7 <= len(telefono) <= 10:
            raise ClienteError(f"Teléfono inválido: {telefono} (debe tener de 7 a 10 dígitos)")
        self.__nombre = nombre.strip()
        self.__email = email
        self.__telefono = telefono

    def obtener_nombre(self):
        return self.__nombre

    def describir(self):
        return f"Cliente {self._id}: {self.__nombre} ({self.__email})"
