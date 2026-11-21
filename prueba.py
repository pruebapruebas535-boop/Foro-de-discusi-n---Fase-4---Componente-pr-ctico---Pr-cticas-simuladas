# prueba.py
# Ejecuta 12 operaciones (válidas e inválidas) para probar que el sistema no se detiene.

from clases_base import ReservaSala, AlquilerEquipo, Asesoria, ErrorSistemaFJ, escribir_log
from sistema_reservas import SistemaSoftwareFJ


def main():
    sistema = SistemaSoftwareFJ()

    print("\n--- 1. CLIENTES ---")
    # Op 1: Cliente válido
    sistema.agregar_cliente("C1", "Ana Pérez", "ana@gmail.com")
    # Op 2: Cliente válido
    sistema.agregar_cliente("C2", "Luis Torres", "luis@empresa.com")
    # Op 3: Error por correo sin '@'
    sistema.agregar_cliente("C3", "Pedro Ruiz", "pedro_sin_arroba.com")
    # Op 4: Error por nombre vacío
    sistema.agregar_cliente("C4", "", "correo@valido.com")

    print("\n--- 2. SERVICIOS ---")
    # Op 5: Sala válida
    sala1 = ReservaSala("S1", "Sala Principal", 50000, 10)
    sistema.agregar_servicio(sala1)

    # Op 6: Equipo válido
    equipo1 = AlquilerEquipo("S2", "Portátil HP", 40000, "Laptop")
    sistema.agregar_servicio(equipo1)

    # Op 7: Asesoría válida
    asesoria1 = Asesoria("S3", "Asesoría de Software", 90000, "Programación")
    sistema.agregar_servicio(asesoria1)

    # Op 8: Error al crear servicio con precio negativo
    try:
        sala_mala = ReservaSala("S4", "Sala Mala", -10000, 6)
        sistema.agregar_servicio(sala_mala)
    except ErrorSistemaFJ as e:
        print("Error creando servicio:", e)
        escribir_log("ERROR", f"Crear servicio S4: {e}")

    print("\n--- 3. RESERVAS ---")
    # Op 9: Reserva válida de sala
    sistema.hacer_reserva("R1", "C1", "S1", 3)

    # Op 10: Error porque la sala S1 ya quedó ocupada en R1
    sistema.hacer_reserva("R2", "C2", "S1", 2)

    # Op 11: Error porque el cliente C3 no se pudo registrar antes
    sistema.hacer_reserva("R3", "C3", "S2", 2)

    # Op 12: Reserva válida de asesoría con descuento del 10% (0.10) y cancelación posterior
    sistema.hacer_reserva("R4", "C2", "S3", 4, descuento=0.10)
    sistema.cancelar_reserva("R4")

    print("\n--- ESTADO FINAL ---")
    print("Total clientes guardados:", len(sistema.clientes))
    print("Total servicios guardados:", len(sistema.servicios))
    print("Total reservas guardadas:", len(sistema.reservas))
    print("Revisa el archivo 'registro_eventos.log' para ver todo lo registrado.")


if __name__ == "__main__":
    main()
