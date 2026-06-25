# -*- coding: utf-8 -*-
"""
Sistema de alquiler de bicicletas
=================================
Implementación en Python de la especificación de variables, constantes,
procedimientos y funciones provista por la cátedra.

Estructura de datos: listas paralelas ancladas por posición al ID de bicicleta.
"""

# ---------------------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------------------
ID_ADMIN = 84938194
DESCUENTO = 0.10  # 10% si se paga en efectivo

# ---------------------------------------------------------------------------
# VARIABLES / ESTADO GLOBAL
# ---------------------------------------------------------------------------
precio_excelente = 5000.0
precio_bueno = 4000.0
precio_regular = 2500.0

# Listas paralelas (índice = posición de la bicicleta, ancladas por ID)
lista_id_bicicleta = []
lista_disponible = []          # bool: True = disponible
lista_dni = []                 # int: 0 = sin usuario asignado
lista_estado = []              # "excelente" | "bueno" | "regular" | "mantenimiento"
lista_horas_uso = []           # horas de uso en el día, por bici
lista_veces_alquilada = []     # veces alquilada en el día, por bici

# Acumuladores solo visibles para administrador
horas_uso_excelente = 0
horas_uso_bueno = 0
horas_uso_regular = 0

recaudado_excelente = 0.0
recaudado_bueno = 0.0
recaudado_regular = 0.0

# Variable temporal usada por obtener_ID() dentro de alquilar()
ID_seleccionado = 0


# ---------------------------------------------------------------------------
# INICIALIZACIÓN
# ---------------------------------------------------------------------------
def inicializar_sistema():
    """Crea las 60 bicicletas iniciales: 20 excelente, 20 bueno, 20 regular."""
    id_actual = 1
    for _ in range(20):
        _crear_bici(id_actual, "excelente")
        id_actual += 1
    for _ in range(20):
        _crear_bici(id_actual, "bueno")
        id_actual += 1
    for _ in range(20):
        _crear_bici(id_actual, "regular")
        id_actual += 1


def _crear_bici(id_bici, estado):
    lista_id_bicicleta.append(id_bici)
    lista_disponible.append(True)
    lista_dni.append(0)
    lista_estado.append(estado)
    lista_horas_uso.append(0)
    lista_veces_alquilada.append(0)




# ---------------------------------------------------------------------------
# FUNCIONES DE CONSULTA DE DISPONIBILIDAD
# ---------------------------------------------------------------------------
def cantidad_disponiblesexc():
    total = 0
    for i in range(len(lista_id_bicicleta)):
        if lista_estado[i] == "excelente" and lista_disponible[i]:
            total += 1
    return total


def cantidad_disponiblebueno():
    total = 0
    for i in range(len(lista_id_bicicleta)):
        if lista_estado[i] == "bueno" and lista_disponible[i]:
            total += 1
    return total


def cantidad_disponiblereg():
    total = 0
    for i in range(len(lista_id_bicicleta)):
        if lista_estado[i] == "regular" and lista_disponible[i]:
            total += 1
    return total


def cantidad_disponibles_total():
    return cantidad_disponiblesexc() + cantidad_disponiblebueno() + cantidad_disponiblereg()


def cantidad_en_uso():
    total = 0
    for dni in lista_dni:
        if dni != 0:
            total += 1
    return total


def cantidad_en_uso_por_estado(estado):
    total = 0
    for i in range(len(lista_id_bicicleta)):
        if lista_estado[i] == estado and lista_dni[i] != 0:
            total += 1
    return total


def cantidad_mantenimiento():
    total = 0
    for estado in lista_estado:
        if estado == "mantenimiento":
            total += 1
    return total


def obtener_ID(estado_buscado):
    """Devuelve el primer ID de bici disponible en el estado pedido, o -1."""
    for i in range(len(lista_id_bicicleta)):
        if lista_estado[i] == estado_buscado and lista_disponible[i]:
            return lista_id_bicicleta[i]
    return -1


def _index_por_id(id_bici):
    if id_bici in lista_id_bicicleta:
        return lista_id_bicicleta.index(id_bici)
    return -1


def _precio_por_estado(estado):
    if estado == "excelente":
        return precio_excelente
    if estado == "bueno":
        return precio_bueno
    if estado == "regular":
        return precio_regular
    return 0.0


# ---------------------------------------------------------------------------
# ENTRADA DE DATOS AUXILIARES (con validación básica)
# ---------------------------------------------------------------------------
def pedir_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.lstrip("-").isdigit():
            return int(valor)
        print("Error: debe ingresar un número entero.")


def pedir_dni():
    while True:
        dni = pedir_entero("Ingrese su DNI (8 dígitos): ")
        if dni == 0:
            print("Error: el DNI no puede ser 0. Intente nuevamente.")
            continue
        if len(str(dni)) != 8:
            print("Error: el DNI debe tener 8 dígitos.")
            continue
        return dni


def pedir_metodo_pago():
    while True:
        metodo = input("Método de pago (td=tarjeta débito, tc=tarjeta crédito, "
                        "t=transferencia, e=efectivo): ").strip().lower()
        if metodo in ("td", "tc", "t", "e"):
            return metodo
        print("Error: opción de pago inválida.")


# ---------------------------------------------------------------------------
# PROCEDIMIENTO: ALQUILAR
# ---------------------------------------------------------------------------
def alquilar():
    global ID_seleccionado
    print("\n--- Alquilar bicicleta ---")
    print("1) Excelente")
    print("2) Bueno")
    print("3) Regular")
    opcion = input("Seleccione el tipo de bicicleta: ").strip()

    mapa_estados = {"1": "excelente", "2": "bueno", "3": "regular"}
    if opcion not in mapa_estados:
        print("Opción inválida. Volviendo al menú principal.")
        return

    estado_buscado = mapa_estados[opcion]
    ID_seleccionado = obtener_ID(estado_buscado)

    if ID_seleccionado == -1:
        print(f"No hay bicicletas disponibles en estado '{estado_buscado}'. "
              f"Volviendo al menú principal.")
        ID_seleccionado = 0
        return

    dni = pedir_dni()
    if dni in lista_dni:
        print("Error: el usuario con ese DNI ya alquiló una bicicleta. "
              "No puede tener más de 1 bicicleta alquilada al mismo tiempo.")
        ID_seleccionado = 0
        return

    nombre_apellido = input("Ingrese su nombre y apellido: ").strip()[:50]
    metodo_pago = pedir_metodo_pago()

    horas = pedir_entero("Ingrese la cantidad de horas de alquiler (mínimo 1): ")
    while horas < 1:
        print("Error: el alquiler es de mínimo 1 hora.")
        horas = pedir_entero("Ingrese la cantidad de horas de alquiler (mínimo 1): ")

    precio_hora = _precio_por_estado(estado_buscado)
    costo_total = precio_hora * horas
    if metodo_pago == "e":
        costo_total *= (1 - DESCUENTO)

    print(f"\nResumen del alquiler:")
    print(f"  Bicicleta ID: {ID_seleccionado} ({estado_buscado})")
    print(f"  Usuario: {nombre_apellido} (DNI: {dni})")
    print(f"  Horas: {horas}")
    print(f"  Costo total: ${costo_total:.2f}")
    confirmar = input("¿Confirma el alquiler? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Alquiler cancelado. Volviendo al menú principal.")
        ID_seleccionado = 0
        return

    idx = _index_por_id(ID_seleccionado)
    lista_dni[idx] = dni
    lista_disponible[idx] = False
    lista_veces_alquilada[idx] += 1
    lista_horas_uso[idx] += horas

    _actualizar_acumuladores(estado_buscado, horas, costo_total)

    print("¡Alquiler realizado con éxito!")
    ID_seleccionado = 0


def _actualizar_acumuladores(estado, horas, costo_total):
    global horas_uso_excelente, horas_uso_bueno, horas_uso_regular
    global recaudado_excelente, recaudado_bueno, recaudado_regular

    if estado == "excelente":
        horas_uso_excelente += horas
        recaudado_excelente += costo_total
    elif estado == "bueno":
        horas_uso_bueno += horas
        recaudado_bueno += costo_total
    elif estado == "regular":
        horas_uso_regular += horas
        recaudado_regular += costo_total

if __name__ == "__main__":
    inicializar_sistema()
    print(f"Sistema inicializado con {len(lista_id_bicicleta)} bicicletas.")
