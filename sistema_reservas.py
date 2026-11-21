# sistema_reservas.py
# Maneja la clase Reserva y el sistema con listas internas y bloques try/except/else/finally.

from clases_base import (
    Entidad,
    Cliente,
    Servicio,
    ErrorSistemaFJ,
    ErrorDisponibilidad,
    ErrorOperacionReserva,
    escribir_log,
)


class Reserva(Entidad):
    """Representa una reserva hecha por un cliente para un servicio."""

    def __init__(self, codigo, cliente, servicio, cantidad, descuento=0.0):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            raise ErrorOperacionReserva("Debe asignarse un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorOperacionReserva("Debe asignarse un servicio válido.")

        # Valida la duración según el tipo de servicio.
        servicio.validar_tiempo(cantidad)

        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.descuento = descuento
        self.estado = "PENDIENTE"
        self.total = 0.0

    def confirmar(self):
        """Confirma la reserva si el servicio está disponible."""
        if self.estado != "PENDIENTE":
            raise ErrorOperacionReserva(f"No se puede confirmar una reserva en estado '{self.estado}'.")
        if not self.servicio.disponible:
            raise ErrorDisponibilidad(f"El servicio '{self.servicio.nombre}' no está disponible.")

        self.total = self.servicio.calcular_costo(self.cantidad, descuento=self.descuento)
        self.servicio.disponible = False
        self.estado = "CONFIRMADA"

    def cancelar(self):
        """Cancela la reserva y libera el servicio."""
        if self.estado == "CANCELADA":
            raise ErrorOperacionReserva("La reserva ya estaba cancelada.")

        if self.estado == "CONFIRMADA":
            self.servicio.disponible = True
        self.estado = "CANCELADA"

    def mostrar_info(self):
        return (
            f"Reserva [{self._codigo}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Cantidad: {self.cantidad} | "
            f"Estado: {self.estado} | Total: ${self.total}"
        )


class SistemaSoftwareFJ:
    """Administra clientes, servicios y reservas usando listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        escribir_log("INFO", "Sistema Software FJ iniciado.")

    def agregar_cliente(self, codigo, nombre, correo):
        """Registra un cliente usando try / except / else / finally."""
        try:
            cliente = Cliente(codigo, nombre, correo)
        except ErrorSistemaFJ as e:
            print("Error al registrar cliente:", e)
            escribir_log("ERROR", f"Cliente {codigo}: {e}")
        else:
            # Se ejecuta solo si no hubo errores en try.
            self.clientes.append(cliente)
            print("Cliente registrado:", cliente.mostrar_info())
            escribir_log("INFO", f"Cliente registrado: {cliente.mostrar_info()}")
        finally:
            # Se ejecuta siempre al terminar el intento.
            escribir_log("AUDITORIA", f"Intento de registro de cliente '{codigo}'.")

    def agregar_servicio(self, servicio):
        """Agrega un servicio a la lista de servicios."""
        try:
            if not isinstance(servicio, Servicio):
                raise ErrorOperacionReserva("El objeto enviado no es un servicio.")
        except ErrorSistemaFJ as e:
            print("Error al agregar servicio:", e)
            escribir_log("ERROR", f"Servicio: {e}")
        else:
            self.servicios.append(servicio)
            print("Servicio agregado:", servicio.mostrar_info())
            escribir_log("INFO", f"Servicio agregado: {servicio.mostrar_info()}")
        finally:
            escribir_log("AUDITORIA", "Intento de registro de servicio.")

    def buscar_cliente(self, codigo):
        for c in self.clientes:
            if c.codigo == codigo:
                return c
        raise ErrorOperacionReserva(f"Cliente con código '{codigo}' no encontrado.")

    def buscar_servicio(self, codigo):
        for s in self.servicios:
            if s.codigo == codigo:
                return s
        raise ErrorOperacionReserva(f"Servicio con código '{codigo}' no encontrado.")

    def hacer_reserva(self, codigo_reserva, codigo_cliente, codigo_servicio, cantidad, descuento=0.0):
        """Crea y confirma una reserva manejando posibles errores."""
        try:
            cliente = self.buscar_cliente(codigo_cliente)
            servicio = self.buscar_servicio(codigo_servicio)
            reserva = Reserva(codigo_reserva, cliente, servicio, cantidad, descuento)
            reserva.confirmar()
        except ErrorSistemaFJ as e:
            print("Error en reserva:", e)
            escribir_log("ERROR", f"Reserva {codigo_reserva}: {e}")
        else:
            self.reservas.append(reserva)
            print("Reserva confirmada:", reserva.mostrar_info())
            escribir_log("INFO", f"Reserva confirmada: {reserva.mostrar_info()}")
        finally:
            escribir_log("AUDITORIA", f"Intento de reserva '{codigo_reserva}'.")

    def cancelar_reserva(self, codigo_reserva):
        """Busca y cancela una reserva existente."""
        try:
            encontrada = None
            for r in self.reservas:
                if r.codigo == codigo_reserva:
                    encontrada = r
                    break
            if encontrada is None:
                raise ErrorOperacionReserva(f"No existe la reserva '{codigo_reserva}'.")
            encontrada.cancelar()
        except ErrorSistemaFJ as e:
            print("Error al cancelar:", e)
            escribir_log("ERROR", f"Cancelar {codigo_reserva}: {e}")
        else:
            print("Reserva cancelada:", encontrada.mostrar_info())
            escribir_log("INFO", f"Reserva cancelada: {encontrada.mostrar_info()}")
        finally:
            escribir_log("AUDITORIA", f"Intento de cancelación '{codigo_reserva}'.")
