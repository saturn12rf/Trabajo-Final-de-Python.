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


if __name__ == "__main__":
    inicializar_sistema()
    print(f"Sistema inicializado con {len(lista_id_bicicleta)} bicicletas.")
