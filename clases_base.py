# clases_base.py
# Archivo con excepciones simples, registro en log y clases orientadas a objetos.

from abc import ABC, abstractmethod
from datetime import datetime


# --- EXCEPCIONES PERSONALIZADAS SENCILLAS ---

class ErrorSistemaFJ(Exception):
    """Error general del sistema de Software FJ."""
    pass


class ErrorDatosInvalidos(ErrorSistemaFJ):
    """Error cuando un dato de entrada no es válido."""
    pass


class ErrorDisponibilidad(ErrorSistemaFJ):
    """Error cuando un servicio no está disponible."""
    pass


class ErrorOperacionReserva(ErrorSistemaFJ):
    """Error cuando no se puede crear, confirmar o cancelar una reserva."""
    pass


# --- FUNCIÓN PARA ESCRIBIR EN EL ARCHIVO DE LOGS ---

def escribir_log(tipo, mensaje, archivo="registro_eventos.log"):
    """Escribe un evento o error en el archivo de texto de logs."""
    # Obtiene la fecha y hora actual como texto.
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Abre el archivo en modo 'a' (agregar al final) y guarda la línea.
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"[{fecha_hora}] [{tipo}] {mensaje}\n")


# --- CLASE ABSTRACTA GENERAL ---

class Entidad(ABC):
    """Clase abstracta base para clientes, servicios y reservas."""

    def __init__(self, codigo):
        # Verifica que el código no esté vacío.
        if not codigo or str(codigo).strip() == "":
            raise ErrorDatosInvalidos("El código no puede estar vacío.")
        self._codigo = str(codigo).strip()

    @property
    def codigo(self):
        """Devuelve el código de la entidad."""
        return self._codigo

    @abstractmethod
    def mostrar_info(self):
        """Cada clase hija debe decir cómo mostrar su información."""
        pass


# --- CLASE CLIENTE ---

class Cliente(Entidad):
    """Representa un cliente con datos encapsulados y validados."""

    def __init__(self, codigo, nombre, correo):
        super().__init__(codigo)
        # Usa los setters para validar desde el inicio.
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(str(valor).strip()) < 2:
            raise ErrorDatosInvalidos("El nombre del cliente debe tener al menos 2 letras.")
        self._nombre = str(valor).strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in str(valor):
            raise ErrorDatosInvalidos(f"Correo inválido: '{valor}'. Debe contener '@'.")
        self._correo = str(valor).strip()

    def mostrar_info(self):
        return f"Cliente {self._codigo} - Nombre: {self._nombre} - Correo: {self._correo}"


# --- CLASE ABSTRACTA SERVICIO Y 3 SERVICIOS ---

class Servicio(Entidad):
    """Clase abstracta para los servicios que ofrece Software FJ."""

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        super().__init__(codigo)
        if not nombre or str(nombre).strip() == "":
            raise ErrorDatosInvalidos("El nombre del servicio es obligatorio.")
        if precio_base <= 0:
            raise ErrorDatosInvalidos("El precio base debe ser mayor que cero.")

        self._nombre = str(nombre).strip()
        self._precio_base = float(precio_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_tiempo(self, cantidad):
        """Valida si la cantidad de horas o días es válida para este servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, cantidad, descuento=0.0, impuesto=0.19):
        """Calcula el costo con parámetros opcionales (sobrecarga por valores por defecto)."""
        pass

    def _calcular_total_con_ajustes(self, subtotal, descuento, impuesto):
        """Aplica descuento e impuesto y encadena errores si algo falla."""
        try:
            # Convierte los valores a número decimal.
            sub = float(subtotal)
            desc = float(descuento)
            imp = float(impuesto)

            # Revisa que el descuento y el impuesto estén en un rango lógico.
            if desc < 0 or desc >= 1:
                raise ErrorDatosInvalidos("El descuento debe estar entre 0 y 0.99.")
            if imp < 0 or imp > 1:
                raise ErrorDatosInvalidos("El impuesto debe estar entre 0 y 1.")

            con_descuento = sub * (1 - desc)
            total = con_descuento * (1 + imp)
            return round(total, 2)

        except ErrorDatosInvalidos:
            # Vuelve a lanzar si ya es un error de datos inválidos.
            raise
        except Exception as error_original:
            # Encadena el error original con una excepción del sistema.
            raise ErrorSistemaFJ("Error al calcular el costo total.") from error_original


class ReservaSala(Servicio):
    """Servicio 1: Reserva de salas por horas."""

    def __init__(self, codigo, nombre, precio_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, precio_hora, disponible)
        if capacidad <= 0:
            raise ErrorDatosInvalidos("La capacidad de la sala debe ser mayor que cero.")
        self.capacidad = capacidad

    def validar_tiempo(self, cantidad):
        if cantidad < 1 or cantidad > 10:
            raise ErrorDatosInvalidos("Una sala se reserva entre 1 y 10 horas.")

    def calcular_costo(self, cantidad, descuento=0.0, impuesto=0.19):
        self.validar_tiempo(cantidad)
        subtotal = self._precio_base * cantidad
        return self._calcular_total_con_ajustes(subtotal, descuento, impuesto)

    def mostrar_info(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Sala [{self._codigo}] {self._nombre} (Cap: {self.capacidad}) - ${self._precio_base}/h - {estado}"


class AlquilerEquipo(Servicio):
    """Servicio 2: Alquiler de equipos por días."""

    def __init__(self, codigo, nombre, precio_dia, tipo_equipo, disponible=True):
        super().__init__(codigo, nombre, precio_dia, disponible)
        if not tipo_equipo or str(tipo_equipo).strip() == "":
            raise ErrorDatosInvalidos("El tipo de equipo es obligatorio.")
        self.tipo_equipo = tipo_equipo

    def validar_tiempo(self, cantidad):
        if cantidad < 1 or cantidad > 15:
            raise ErrorDatosInvalidos("El alquiler de equipo es de 1 a 15 días.")

    def calcular_costo(self, cantidad, descuento=0.0, impuesto=0.19):
        self.validar_tiempo(cantidad)
        # Suma un cargo fijo de 10000 por revisión del equipo.
        subtotal = (self._precio_base * cantidad) + 10000
        return self._calcular_total_con_ajustes(subtotal, descuento, impuesto)

    def mostrar_info(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Equipo [{self._codigo}] {self._nombre} ({self.tipo_equipo}) - ${self._precio_base}/día - {estado}"


class Asesoria(Servicio):
    """Servicio 3: Asesorías especializadas por horas."""

    def __init__(self, codigo, nombre, precio_hora, area, disponible=True):
        super().__init__(codigo, nombre, precio_hora, disponible)
        if not area or str(area).strip() == "":
            raise ErrorDatosInvalidos("El área de asesoría es obligatoria.")
        self.area = area

    def validar_tiempo(self, cantidad):
        if cantidad < 2 or cantidad > 20:
            raise ErrorDatosInvalidos("Una asesoría debe ser de 2 a 20 horas.")

    def calcular_costo(self, cantidad, descuento=0.0, impuesto=0.19):
        self.validar_tiempo(cantidad)
        subtotal = self._precio_base * cantidad
        return self._calcular_total_con_ajustes(subtotal, descuento, impuesto)

    def mostrar_info(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Asesoría [{self._codigo}] {self._nombre} ({self.area}) - ${self._precio_base}/h - {estado}"
