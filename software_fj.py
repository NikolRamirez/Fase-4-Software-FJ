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


#Lista interna de clientes (en lugar de base de datos).
clientes = []

def registrar_cliente(nombre=None, email=None, telefono=None):
    cliente = Cliente(len(clientes) + 1, nombre, email, telefono)
    clientes.append(cliente)
    return cliente

# PARTE 2 - GESTIÓN DE SERVICIOS
# Responsable: Yeny Rios

from abc import ABC, abstractmethod


# Clase abstracta Servicio que hereda de Entidad.
# Clase abstracta que establece la estructura general
# de los servicios ofrecidos por Software FJ.
class Servicio(Entidad, ABC):

    def __init__(self, id, nombre, precio_base, disponible=True):
        super().__init__(id)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError("El nombre del servicio es obligatorio.")

        try:
            precio_base = float(precio_base)
        except (TypeError, ValueError) as error:
            raise ServicioError("El precio debe ser numérico.") from error

        if precio_base <= 0:
            raise ServicioError("El precio debe ser mayor que cero.")

        if not isinstance(disponible, bool):
            raise ServicioError("La disponibilidad debe ser verdadera o falsa.")

        self.__nombre = nombre.strip()
        self.__precio_base = precio_base
        self.__disponible = disponible

    # Permite consultar el nombre del servicio.
    def obtener_nombre(self):
        return self.__nombre

    # Permite consultar la disponibilidad.
    def esta_disponible(self):
        return self.__disponible

    # Permite consultar el precio base.
    def obtener_precio(self):
        return self.__precio_base

    # Valida que la duración sea positiva.
    def validar_duracion(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise ServicioError("La duración debe ser numérica.") from error

        if duracion <= 0:
            raise ServicioError("La duración debe ser mayor que cero.")

        return duracion

    # Método auxiliar para calcular el costo final.
    def calcular_total(self, cantidad, impuesto=0, descuento=0):

        try:
            impuesto = float(impuesto)
            descuento = float(descuento)
        except (TypeError, ValueError) as error:
            raise CalculoError("Impuesto y descuento deben ser numéricos.") from error

        if not 0 <= impuesto <= 100:
            raise CalculoError("El impuesto debe estar entre 0 y 100.")

        if not 0 <= descuento <= 100:
            raise CalculoError("El descuento debe estar entre 0 y 100.")

        subtotal = cantidad * self.__precio_base
        valor_descuento = subtotal * descuento / 100
        valor_impuesto = (subtotal - valor_descuento) * impuesto / 100

        total = subtotal - valor_descuento + valor_impuesto

        if total < 0:
            raise CalculoError("El cálculo produjo un valor inconsistente.")

        return round(total, 2)

    # Cada servicio debe implementar sus propios métodos.
    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

# Servicio especializado para reservar salas.
class ReservaSala(Servicio):

    def __init__(self, id, nombre, precio_base, capacidad=10, disponible=True):
        super().__init__(id, nombre, precio_base, disponible)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioError("La capacidad debe ser un entero positivo.")

        self.__capacidad = capacidad

    def validar_parametros(self, duracion):
        duracion = self.validar_duracion(duracion)

        if self.__capacidad <= 0:
            raise ServicioError("La capacidad de la sala no es válida.")

        return True

    # Calcula el costo según las horas reservadas.
    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        duracion = self.validar_duracion(duracion)

        return self.calcular_total(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Sala: {self.obtener_nombre()} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Precio por hora: ${self.obtener_precio()}"
        )



