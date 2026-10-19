from math import radians, sin, cos, sqrt, atan2
import heapq

import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview


# ============================================================
# 1. NOMBRES DE LOS VÉRTICES
# ============================================================

vertices = [
    "Amazonas",
    "Vaupes",
    "Caqueta",
    "Putumayo",
    "Guaviare",
    "Guainia",
    "Nariño",
    "Cauca",
    "Huila",
    "Valle del cauca",
    "Tolima",
    "Meta",
    "Vichada",
    "Casanare",
    "Arauca",
    "Boyaca",
    "Cundinamarca",
    "Bogota",
    "Santander",
    "Norte de santander"
]


# ============================================================
# 2. COORDENADAS GEOGRÁFICAS
# ============================================================

coordenadas = {

    "Amazonas": (-4.21079, -69.93944),
    "Vaupes": (1.25778, -70.23472),
    "Caqueta": (1.61438, -75.60623),
    "Putumayo": (1.15284, -76.65208),
    "Guaviare": (2.57286, -72.64591),
    "Guainia": (3.86528, -67.92389),
    "Nariño": (1.21361, -77.28111),
    "Cauca": (2.43823, -76.61316),
    "Huila": (2.92730, -75.28189),
    "Valle del cauca": (3.43722, -76.52250),
    "Tolima": (4.43889, -75.23222),
    "Meta": (4.14200, -73.62664),
    "Vichada": (6.18900, -67.48588),
    "Casanare": (5.33775, -72.39586),
    "Arauca": (7.08471, -70.75908),
    "Boyaca": (5.53528, -73.36778),
    "Cundinamarca": (4.60971, -74.08175),
    "Bogota": (4.60971, -74.08175),
    "Santander": (7.12500, -73.11895),
    "Norte de santander": (7.90750, -72.50472)
}


# ============================================================
# 3. RELACIONAR NOMBRES CON ÍNDICES
# ============================================================

indice = {
    nombre: i
    for i, nombre in enumerate(vertices)
}


# ============================================================
# 4. MATRIZ DE ADYACENCIA
# ============================================================

conexiones = [
    ("Amazonas", "Vaupes", 570),
    ("Amazonas", "Caqueta", 590),

    ("Vaupes", "Guaviare", 290),

    ("Caqueta", "Putumayo", 85),
    ("Caqueta", "Guaviare", 180),

    ("Putumayo", "Nariño", 120),
    ("Putumayo", "Huila", 210),
    ("Putumayo", "Meta", 370),

    ("Guaviare", "Guainia", 290),
    ("Guaviare", "Meta", 170),

    ("Guainia", "Vichada", 370),

    ("Nariño", "Cauca", 190),

    ("Cauca", "Huila", 140),
    ("Cauca", "Valle del cauca", 105),

    ("Huila", "Tolima", 170),

    ("Valle del cauca", "Cundinamarca", 305),

    ("Tolima", "Boyaca", 130),
    ("Tolima", "Cundinamarca", 130),

    ("Meta", "Casanare", 190),
    ("Meta", "Bogota", 75),

    ("Vichada", "Casanare", 310),

    ("Casanare", "Arauca", 260),

    ("Arauca", "Boyaca", 300),
    ("Arauca", "Norte de santander", 210),

    ("Boyaca", "Bogota", 115),
    ("Boyaca", "Santander", 170),

    ("Cundinamarca", "Santander", 290),

    ("Bogota", "Tolima", 130),
    ("Bogota", "Boyaca", 115),

    ("Santander", "Norte de santander", 112)
]

grafo = [
    [0 for _ in range(len(vertices))]
    for _ in range(len(vertices))
]


for origen, destino, peso in conexiones:

    i = indice[origen]
    j = indice[destino]

    # Conexión en ambos sentidos
    grafo[i][j] = peso
    grafo[j][i] = peso



# ============================================================
# 5. BUSCAR VÉRTICE IGNORANDO MAYÚSCULAS
# ============================================================

def buscar_vertice(nombre):

    nombre = nombre.strip().lower()

    for vertice in vertices:

        if vertice.lower() == nombre:
            return vertice

    return None


# ============================================================
# 6. DISTANCIA GEOGRÁFICA - HAVERSINE
# ============================================================

def distancia_directa(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Convertir latitudes a radianes
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    # Diferencias
    diferencia_latitud = radians(lat2 - lat1)
    diferencia_longitud = radians(lon2 - lon1)

    # Fórmula de Haversine
    a = (
        sin(diferencia_latitud / 2) ** 2
        +
        cos(lat1_rad)
        * cos(lat2_rad)
        * sin(diferencia_longitud / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# ============================================================
# 7. CREAR HEURÍSTICA
# ============================================================

def crear_heuristica(destino):

    heuristica = {}

    for vertice in vertices:

        heuristica[vertice] = distancia_directa(
            coordenadas[vertice],
            coordenadas[destino]
        )

    return heuristica


# ============================================================
# 8. OBTENER VECINOS
# ============================================================

def obtener_vecinos(nombre):

    nodo = indice[nombre]

    vecinos = []

    for i in range(len(grafo[nodo])):

        if grafo[nodo][i] != 0:

            vecinos.append(vertices[i])

    return vecinos


# ============================================================
# 9. BÚSQUEDA AVARA
# ============================================================

def busqueda_avara(inicio, destino, heuristica):

    actual = inicio

    ruta = [actual]

    visitados = set()

    while actual != destino:

        visitados.add(actual)

        vecinos = obtener_vecinos(actual)

        vecinos_disponibles = [
            vecino
            for vecino in vecinos
            if vecino not in visitados
        ]

        if not vecinos_disponibles:

            return None

        siguiente = min(
            vecinos_disponibles,
            key=lambda vecino: heuristica[vecino]
        )

        actual = siguiente

        ruta.append(actual)

    return ruta


# ============================================================
# 10. BÚSQUEDA A*
# ============================================================

def busqueda_a_estrella(inicio, destino, heuristica):

    # --------------------------------------------------------
    # Cola de prioridad
    # --------------------------------------------------------

    cola = []

    # f(n) = g(n) + h(n)
    f_inicial = heuristica[inicio]

    heapq.heappush(
        cola,
        (f_inicial, 0, inicio)
    )


    # --------------------------------------------------------
    # Costos desde el inicio
    # --------------------------------------------------------

    costos = {
        vertice: float("inf")
        for vertice in vertices
    }

    costos[inicio] = 0


    # --------------------------------------------------------
    # Predecesores para reconstruir la ruta
    # --------------------------------------------------------

    anteriores = {
        vertice: None
        for vertice in vertices
    }


    # --------------------------------------------------------
    # Conjunto de visitados
    # --------------------------------------------------------

    visitados = set()


    # --------------------------------------------------------
    # Algoritmo A*
    # --------------------------------------------------------

    while cola:

        f_actual, g_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue

        visitados.add(actual)


        # ----------------------------------------------------
        # Llegamos al destino
        # ----------------------------------------------------

        if actual == destino:

            ruta = []

            nodo = destino

            while nodo is not None:

                ruta.append(nodo)

                nodo = anteriores[nodo]

            ruta.reverse()

            return ruta


        # ----------------------------------------------------
        # Revisar vecinos
        # ----------------------------------------------------

        for vecino in obtener_vecinos(actual):

            if vecino in visitados:
                continue


            peso = grafo[
                indice[actual]
            ][
                indice[vecino]
            ]


            nuevo_g = (
                costos[actual]
                + peso
            )


            # ------------------------------------------------
            # Si encontramos un camino mejor
            # ------------------------------------------------

            if nuevo_g < costos[vecino]:

                costos[vecino] = nuevo_g

                anteriores[vecino] = actual

                nuevo_f = (
                    nuevo_g
                    + heuristica[vecino]
                )

                heapq.heappush(
                    cola,
                    (
                        nuevo_f,
                        nuevo_g,
                        vecino
                    )
                )


    # --------------------------------------------------------
    # No existe ruta
    # --------------------------------------------------------

    return None


# ============================================================
# 11. ÁRBOL DE EXPANSIÓN MÍNIMA - KRUSKAL
# ============================================================

def arbol_kruskal():

    # Ordenar todas las conexiones por peso ascendente
    aristas_ordenadas = sorted(
        conexiones,
        key=lambda arista: arista[2]
    )

    # Cada vértice comienza en su propio conjunto
    padre = {vertice: vertice for vertice in vertices}
    rango = {vertice: 0 for vertice in vertices}

    # Encontrar el representante de un conjunto
    def encontrar(vertice):
        if padre[vertice] != vertice:
            padre[vertice] = encontrar(padre[vertice])
        return padre[vertice]

    # Unir dos conjuntos si son diferentes
    def unir(origen, destino):
        raiz_origen = encontrar(origen)
        raiz_destino = encontrar(destino)

        if raiz_origen == raiz_destino:
            return False

        if rango[raiz_origen] < rango[raiz_destino]:
            padre[raiz_origen] = raiz_destino
        elif rango[raiz_origen] > rango[raiz_destino]:
            padre[raiz_destino] = raiz_origen
        else:
            padre[raiz_destino] = raiz_origen
            rango[raiz_origen] += 1

        return True

    arbol = []

    # Agregar las conexiones más económicas sin formar ciclos
    for origen, destino, peso in aristas_ordenadas:

        if unir(origen, destino):
            arbol.append((origen, destino, peso))

        # Un árbol de expansión tiene V - 1 conexiones
        if len(arbol) == len(vertices) - 1:
            break

    return arbol




# ============================================================
# 12. ÁRBOL DE EXPANSIÓN MÍNIMA - PRIM
# ============================================================

def arbol_prim(inicio=None):

    # Si no se indica un inicio, usar el primer vértice
    if inicio is None:
        inicio = vertices[0]

    visitados = {inicio}
    arbol = []
    cola = []

    # Agregar las conexiones del vértice inicial
    for vecino in obtener_vecinos(inicio):
        peso = grafo[indice[inicio]][indice[vecino]]
        heapq.heappush(
            cola,
            (peso, inicio, vecino)
        )

    while cola and len(visitados) < len(vertices):

        # Sacar la conexión de menor peso
        peso, origen, destino = heapq.heappop(cola)

        # Ignorar conexiones que llegan a vértices visitados
        if destino in visitados:
            continue

        # Agregar la conexión al árbol
        arbol.append((origen, destino, peso))
        visitados.add(destino)

        # Buscar conexiones hacia vértices no visitados
        for vecino in obtener_vecinos(destino):

            if vecino not in visitados:
                nuevo_peso = grafo[
                    indice[destino]
                ][
                    indice[vecino]
                ]

                heapq.heappush(
                    cola,
                    (nuevo_peso, destino, vecino)
                )

    return arbol



def buscar_ruta_en_arbol(arbol, inicio, destino):
    # Crear una lista de vecinos para cada vértice
    adyacencia = {vertice: [] for vertice in vertices}

    for origen, fin, peso in arbol:
        adyacencia[origen].append(fin)
        adyacencia[fin].append(origen)

    # Recorrer el árbol desde el punto A
    pendientes = [(inicio, [inicio])]
    visitados = set()

    while pendientes:
        actual, ruta = pendientes.pop()

        if actual == destino:
            return ruta

        if actual in visitados:
            continue

        visitados.add(actual)

        for vecino in adyacencia[actual]:
            if vecino not in visitados:
                pendientes.append((vecino, ruta + [vecino]))

    # No se encontró una conexión entre los puntos
    return []





# ============================================================
# 13. CALCULAR DISTANCIA TOTAL DE UNA RUTA
# ============================================================

def calcular_distancia_ruta(ruta):

    distancia_total = 0

    for i in range(len(ruta) - 1):

        origen = indice[ruta[i]]
        destino = indice[ruta[i + 1]]

        distancia_total += grafo[origen][destino]

    return distancia_total



# ============================================================
# 14. DIBUJAR EL GRAFO, LOS ÁRBOLES Y LAS RUTAS
# ============================================================

def dibujar_grafo(
    ruta_avara=None,
    ruta_a_estrella=None,
    arbol_kruskal=None,
    arbol_prim=None,
    ruta_kruskal=None,
    ruta_prim=None
):

    mapa.delete_all_marker()
    mapa.delete_all_path()

    # --------------------------------------------------------
    # FUNCION AUXILIAR PARA DIBUJAR UNA CONEXION
    # --------------------------------------------------------

    def dibujar_conexion(origen, destino, color, ancho):

        lat1, lon1 = coordenadas[origen]
        lat2, lon2 = coordenadas[destino]

        mapa.set_path(
            [(lat1, lon1), (lat2, lon2)],
            color=color,
            width=ancho
        )

    # --------------------------------------------------------
    # 1. DIBUJAR TODAS LAS CONEXIONES EN GRIS
    # --------------------------------------------------------

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):

            if grafo[i][j] == 0:
                continue

            dibujar_conexion(
                vertices[i],
                vertices[j],
                "#999999",
                2
            )

    # --------------------------------------------------------
    # 2. DIBUJAR LOS ARBOLES COMPLETOS
    # --------------------------------------------------------

    aristas_kruskal = set()
    aristas_prim = set()

    if arbol_kruskal is not None:
        aristas_kruskal = {
            frozenset((origen, destino))
            for origen, destino, peso in arbol_kruskal
        }

    if arbol_prim is not None:
        aristas_prim = {
            frozenset((origen, destino))
            for origen, destino, peso in arbol_prim
        }

    # Dibujar las conexiones de ambos árboles
    todas_aristas_arbol = aristas_kruskal | aristas_prim

    for arista in todas_aristas_arbol:

        origen, destino = tuple(arista)

        if arista in aristas_kruskal and arista in aristas_prim:
            color = "#9C27B0"  # Compartida por ambos árboles
        elif arista in aristas_kruskal:
            color = "#4CAF50"  # Kruskal
        else:
            color = "#FF9800"  # Prim

        dibujar_conexion(
            origen,
            destino,
            color,
            4
        )

    
# ========================================================
# 3. DIBUJAR LAS RUTAS AVARA Y A*
#    LAS ARISTAS COMPARTIDAS SE DIBUJAN EN MORADO
# ========================================================

    def obtener_aristas_ruta(ruta):
        """Devuelve las conexiones de una ruta sin importar su sentido."""
        if ruta is None:
            return set()

        return {
            frozenset((ruta[i], ruta[i + 1]))
            for i in range(len(ruta) - 1)
        }


    # Obtener las conexiones de cada ruta
    aristas_avara = obtener_aristas_ruta(ruta_avara)
    aristas_a_estrella = obtener_aristas_ruta(ruta_a_estrella)

    # Identificar las conexiones compartidas
    aristas_compartidas = aristas_avara & aristas_a_estrella

    # Dibujar primero las rutas individuales
    def dibujar_ruta(ruta, color, ancho=6):

        if ruta is None:
            return

        for i in range(len(ruta) - 1):

            arista = frozenset((ruta[i], ruta[i + 1]))

            # No dibujar aquí las conexiones compartidas
            if arista in aristas_compartidas:
                continue

            dibujar_conexion(
                ruta[i],
                ruta[i + 1],
                color,
                ancho
            )


    dibujar_ruta(ruta_avara, "#E53935")
    dibujar_ruta(ruta_a_estrella, "#2196F3")


    # Dibujar las conexiones compartidas en morado
    for arista in aristas_compartidas:

        origen, destino = tuple(arista)

        dibujar_conexion(
            origen,
            destino,
            "#9C27B0",
            7
        )


    # --------------------------------------------------------
    # 4. RESALTAR LAS RUTAS DENTRO DE LOS ARBOLES
    # --------------------------------------------------------

    dibujar_ruta(ruta_kruskal, "#00C853", 7)
    dibujar_ruta(ruta_prim, "#00B8D4", 7)

    # --------------------------------------------------------
    # 5. DIBUJAR LOS VERTICES
    # --------------------------------------------------------

    for vertice in vertices:

        latitud, longitud = coordenadas[vertice]

        mapa.set_marker(
            latitud,
            longitud,
            text=vertice
        )



# ============================================================
# 15. EJECUTAR BÚSQUEDA
# ============================================================

def ejecutar_busqueda():

    inicio = combo_inicio.get()
    destino = combo_destino.get()


    # ========================================================
    # VERIFICAR DATOS
    # ========================================================

    if inicio == "" or destino == "":

        messagebox.showwarning(
            "Datos faltantes",
            "Seleccione un punto de inicio y un destino."
        )

        return


    # ========================================================
    # MISMO ORIGEN Y DESTINO
    # ========================================================

    if inicio == destino:

        ruta_avara = [inicio]
        ruta_a_estrella = [inicio]

        dibujar_grafo(
            ruta_avara,
            ruta_a_estrella
        )

        etiqueta_ruta.config(
            text=(
                "🔴 Búsqueda Avara:\n"
                + inicio
                + "\n\n"
                "🔵 Búsqueda A*:\n"
                + inicio
            )
        )

        etiqueta_distancia.config(
            text=(
                "🔴 Longitud Avara: 0 km    "
                "🔵 Longitud A*: 0 km"
            )
        )

        etiqueta_heuristica.config(
            text=""
        )

        return


    # ========================================================
    # CREAR HEURÍSTICA
    # ========================================================

    heuristica = crear_heuristica(
        destino
    )


    # ========================================================
    # EJECUTAR AVARA
    # ========================================================

    ruta_avara = busqueda_avara(
        inicio,
        destino,
        heuristica
    )


    # ========================================================
    # EJECUTAR A*
    # ========================================================

    ruta_a_estrella = busqueda_a_estrella(
        inicio,
        destino,
        heuristica
    )


    # ========================================================
    # SI NO EXISTE NINGUNA RUTA
    # ========================================================

    if (
        ruta_avara is None
        and
        ruta_a_estrella is None
    ):

        messagebox.showerror(
            "Ruta no encontrada",
            "Ninguno de los algoritmos encontró una ruta."
        )

        dibujar_grafo()

        return


    # ========================================================
    # DIBUJAR RESULTADOS
    # ========================================================

    dibujar_grafo(
        ruta_avara,
        ruta_a_estrella
    )


    # ========================================================
    # DISTANCIA AVARA
    # ========================================================

    if ruta_avara is not None:

        distancia_avara = calcular_distancia_ruta(
            ruta_avara
        )

    else:

        distancia_avara = None


    # ========================================================
    # DISTANCIA A*
    # ========================================================

    if ruta_a_estrella is not None:

        distancia_a_estrella = calcular_distancia_ruta(
            ruta_a_estrella
        )

    else:

        distancia_a_estrella = None


    # ========================================================
    # CANTIDAD DE VÉRTICES
    # ========================================================

    if ruta_avara is not None:

        nodos_avara = len(ruta_avara)

    else:

        nodos_avara = 0


    if ruta_a_estrella is not None:

        nodos_a_estrella = len(
            ruta_a_estrella
        )

    else:

        nodos_a_estrella = 0


    # ========================================================
    # MOSTRAR RUTAS
    # ========================================================

    texto_ruta = ""


    # --------------------------------------------------------
    # AVARA
    # --------------------------------------------------------

    if ruta_avara is not None:

        texto_ruta += (
            "🔴 BÚSQUEDA AVARA\n"
            "Ruta: "
            + " → ".join(ruta_avara)
            + "\n"
            "Vértices recorridos: "
            + str(nodos_avara)
            + "\n\n"
        )

    else:

        texto_ruta += (
            "🔴 BÚSQUEDA AVARA\n"
            "No encontró una ruta.\n\n"
        )


    # --------------------------------------------------------
    # A*
    # --------------------------------------------------------

    if ruta_a_estrella is not None:

        texto_ruta += (
            "🔵 BÚSQUEDA A*\n"
            "Ruta: "
            + " → ".join(ruta_a_estrella)
            + "\n"
            "Vértices recorridos: "
            + str(nodos_a_estrella)
        )

    else:

        texto_ruta += (
            "🔵 BÚSQUEDA A*\n"
            "No encontró una ruta."
        )


    etiqueta_ruta.config(
        text=texto_ruta
    )


    # ========================================================
    # MOSTRAR DISTANCIAS
    # ========================================================

    texto_distancia = ""


    if distancia_avara is not None:

        texto_distancia += (
            "🔴 Longitud total Avara: "
            + str(distancia_avara)
            + " km"
        )

    else:

        texto_distancia += (
            "🔴 Longitud total Avara: "
            "No disponible"
        )


    texto_distancia += "        "


    if distancia_a_estrella is not None:

        texto_distancia += (
            "🔵 Longitud total A*: "
            + str(distancia_a_estrella)
            + " km"
        )

    else:

        texto_distancia += (
            "🔵 Longitud total A*: "
            "No disponible"
        )


    etiqueta_distancia.config(
        text=texto_distancia
    )


    # ========================================================
    # MOSTRAR HEURÍSTICAS
    # ========================================================

    texto_heuristica = ""


    # --------------------------------------------------------
    # AVARA
    # --------------------------------------------------------

    if ruta_avara is not None:

        texto_heuristica += (
            "🔴 HEURÍSTICAS - AVARA\n"
        )

        for vertice in ruta_avara:

            texto_heuristica += (
                vertice
                + " → h = "
                + str(
                    round(
                        heuristica[vertice],
                        2
                    )
                )
                + " km\n"
            )


    texto_heuristica += "\n"


    # --------------------------------------------------------
    # A*
    # --------------------------------------------------------

    if ruta_a_estrella is not None:

        texto_heuristica += (
            "🔵 HEURÍSTICAS - A*\n"
        )

        for vertice in ruta_a_estrella:

            texto_heuristica += (
                vertice
                + " → h = "
                + str(
                    round(
                        heuristica[vertice],
                        2
                    )
                )
                + " km\n"
            )


    etiqueta_heuristica.config(
        text=texto_heuristica
    )



def ejecutar_arboles():
    # Obtener el punto A y el punto B seleccionados
    inicio = combo_inicio.get()
    destino = combo_destino.get()

    # Verificar que se hayan seleccionado ambos puntos
    if not inicio or not destino:
        etiqueta_ruta.configure(
            text="Selecciona un punto A y un punto B."
        )
        return

    # Construir los árboles de expansión mínima
    resultado_kruskal = arbol_kruskal()
    resultado_prim = arbol_prim()

    # Buscar la ruta entre A y B en cada árbol
    ruta_kruskal = buscar_ruta_en_arbol(
        resultado_kruskal, inicio, destino
    )

    ruta_prim = buscar_ruta_en_arbol(
        resultado_prim, inicio, destino
    )

    # Dibujar los árboles y resaltar las rutas encontradas
    dibujar_grafo(
        arbol_kruskal=resultado_kruskal,
        arbol_prim=resultado_prim,
        ruta_kruskal=ruta_kruskal,
        ruta_prim=ruta_prim
    )

    # Calcular el peso de cada ruta
    def calcular_peso_ruta(ruta):
        peso_total = 0

        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]

            peso_total += grafo[
                indice[origen]
            ][
                indice[destino]
            ]

        return peso_total

    peso_kruskal = calcular_peso_ruta(ruta_kruskal)
    peso_prim = calcular_peso_ruta(ruta_prim)

    # Mostrar los resultados
    etiqueta_ruta.configure(
        text=(
            f"Ruta en Kruskal: {' → '.join(ruta_kruskal)}\n"
            f"Ruta en Prim: {' → '.join(ruta_prim)}"
        )
    )

    etiqueta_distancia.configure(
        text=(
            f"Peso de la ruta en Kruskal: {peso_kruskal}\n"
            f"Peso de la ruta en Prim: {peso_prim}"
        )
    )



# ============================================================
# 16. CREAR VENTANA
# ============================================================

ventana = tk.Tk()

ventana.title(
    "Comparación de Búsqueda Avara y A*"
)

# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana.geometry("1200x800")
ventana.configure(bg="#eeeeee")


# ============================================================
# CONTENEDOR PRINCIPAL CON SCROLL
# ============================================================

contenedor_exterior = tk.Frame(
    ventana,
    bg="#eeeeee"
)

contenedor_exterior.pack(
    fill="both",
    expand=True
)


# ============================================================
# CANVAS PARA EL SCROLL
# ============================================================

canvas_scroll = tk.Canvas(
    contenedor_exterior,
    bg="#eeeeee",
    highlightthickness=0
)

canvas_scroll.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# BARRA DE DESPLAZAMIENTO
# ============================================================

barra_scroll = ttk.Scrollbar(
    contenedor_exterior,
    orient="vertical",
    command=canvas_scroll.yview
)

barra_scroll.pack(
    side="right",
    fill="y"
)


# ============================================================
# CONFIGURAR SCROLL
# ============================================================

canvas_scroll.configure(
    yscrollcommand=barra_scroll.set
)


# ============================================================
# FRAME QUE CONTENDRÁ TODA LA INTERFAZ
# ============================================================

contenedor_principal = tk.Frame(
    canvas_scroll,
    bg="#eeeeee"
)

ventana_scroll = canvas_scroll.create_window(
    (0, 0),
    window=contenedor_principal,
    anchor="nw"
)


# ============================================================
# ACTUALIZAR ÁREA DE SCROLL
# ============================================================

def actualizar_scroll(event=None):

    canvas_scroll.configure(
        scrollregion=canvas_scroll.bbox("all")
    )


contenedor_principal.bind(
    "<Configure>",
    actualizar_scroll
)


# ============================================================
# HACER QUE EL CONTENEDOR OCUPE TODO EL ANCHO
# ============================================================

def ajustar_ancho(event):

    canvas_scroll.itemconfig(
        ventana_scroll,
        width=event.width
    )


canvas_scroll.bind(
    "<Configure>",
    ajustar_ancho
)


# ============================================================
# SCROLL CON LA RUEDA DEL MOUSE
# ============================================================

def mover_scroll(event):

    canvas_scroll.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas_scroll.bind_all(
    "<MouseWheel>",
    mover_scroll
)



# ============================================================
# 17. TÍTULO
# ============================================================

titulo = tk.Label(
    contenedor_principal,
    text=(
        "Comparación de algoritmos: "
        "Búsqueda Avara vs A*"
    ),
    bg="#eeeeee",
    fg="#222222",
    font=("Arial", 16, "bold")
)

titulo.pack(
    pady=(10, 5)
)


# ============================================================
# 18. PANEL DE SELECCIÓN
# ============================================================

panel = tk.Frame(
    contenedor_principal,
    bg="#eeeeee"
)

panel.pack(
    pady=5
)


# ============================================================
# SELECTOR DE INICIO
# ============================================================

tk.Label(
    panel,
    text="Inicio:",
    bg="#eeeeee",
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=5
)


combo_inicio = ttk.Combobox(
    panel,
    values=vertices,
    state="readonly",
    width=22
)

combo_inicio.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# SELECTOR DE DESTINO
# ============================================================

tk.Label(
    panel,
    text="Destino:",
    bg="#eeeeee",
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=2,
    padx=5
)


combo_destino = ttk.Combobox(
    panel,
    values=vertices,
    state="readonly",
    width=22
)

combo_destino.grid(
    row=0,
    column=3,
    padx=5
)


# ============================================================
# BOTÓN
# ============================================================

boton_buscar = tk.Button(
    panel,
    text="Buscar ruta",
    command=ejecutar_busqueda,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5
)

boton_buscar.grid(
    row=0,
    column=4,
    padx=15
)


# ============================================================
# BOTÓN PARA MOSTRAR LOS ÁRBOLES DE KRUSKAL Y PRIM
# ============================================================

boton_arboles = tk.Button(
    panel,
    text="Mostrar árboles Kruskal y Prim",
    command=ejecutar_arboles,
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5
)

boton_arboles.grid(
    row=0,
    column=5,
    padx=15
)


# ============================================================
# 19. MAPA
# ============================================================

mapa = tkintermapview.TkinterMapView(
    contenedor_principal,
    width=1100,
    height=560,
    corner_radius=0
)

mapa.pack(
    pady=10
)


# ============================================================
# POSICIÓN INICIAL DEL MAPA
# ============================================================

mapa.set_position(
    4.5709,
    -74.2973
)

mapa.set_zoom(6)


# ============================================================
# 20. LEYENDA
# ============================================================

marco_leyenda = tk.Frame(
    contenedor_principal,
    bg="#ffffff",
    relief="solid",
    borderwidth=2
)

# IMPORTANTE:
# La leyenda se coloca ANTES del canvas
marco_leyenda.pack(
    fill="x",
    padx=30,
    pady=8
)


# ============================================================
# TÍTULO
# ============================================================

tk.Label(
    marco_leyenda,
    text="LEYENDA",
    bg="#ffffff",
    fg="#222222",
    font=("Arial", 12, "bold")
).pack(
    pady=(6, 4)
)


# ============================================================
# CONTENEDOR DE LOS ELEMENTOS
# ============================================================

elementos_leyenda = tk.Frame(
    marco_leyenda,
    bg="#ffffff"
)

elementos_leyenda.pack(
    pady=(0, 8)
)


# ============================================================
# AVARA
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#E53935",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=0,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="Búsqueda Avara",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=1,
    padx=(0, 25)
)


# ============================================================
# A*
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#2196F3",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=2,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="A*",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=3,
    padx=(0, 25)
)


# ============================================================
# RUTA COMPARTIDA
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#9C27B0",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=4,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="Ruta compartida",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=5,
    padx=(0, 25)
)


# ============================================================
# CONEXIONES RESTANTES
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#999999",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=6,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="Conexiones restantes",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=7,
    padx=(0, 10)
)


# ============================================================
# KRUSKAL
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#4CAF50",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=8,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="Exclusivos Kruskal",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=9,
    padx=(0, 10)
)


# ============================================================
# PRIM
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#FF9800",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(
    row=0,
    column=10,
    padx=(10, 4)
)

tk.Label(
    elementos_leyenda,
    text="Exclusivos Prim",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=11,
    padx=(0, 10)
)


# ============================================================
# RUTA A -> B EN EL ARBOL DE KRUSKAL
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#00C853",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(row=1, column=0, padx=(10, 4))

tk.Label(
    elementos_leyenda,
    text="Ruta en Kruskal",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(row=1, column=1, padx=(0, 10))


# ============================================================
# RUTA A -> B EN EL ARBOL DE PRIM
# ============================================================

tk.Label(
    elementos_leyenda,
    text="━━━━",
    fg="#00B8D4",
    bg="#ffffff",
    font=("Arial", 12, "bold")
).grid(row=1, column=2, padx=(10, 4))

tk.Label(
    elementos_leyenda,
    text="Ruta en Prim",
    fg="#222222",
    bg="#ffffff",
    font=("Arial", 10, "bold")
).grid(row=1, column=3, padx=(0, 10))





# ============================================================
# 21. PANEL DE RESULTADOS
# ============================================================

marco_resultados = tk.Frame(
    contenedor_principal,
    bg="#eeeeee"
)

marco_resultados.pack(
    fill="x",
    padx=50,
    pady=5
)


# ============================================================
# RESULTADO DE LAS RUTAS
# ============================================================

etiqueta_ruta = tk.Label(
    marco_resultados,
    text=(
        "Seleccione un punto de inicio "
        "y un destino."
    ),
    bg="#eeeeee",
    fg="#222222",
    font=("Arial", 10, "bold"),
    justify="left",
    anchor="w",
    wraplength=1100
)

etiqueta_ruta.pack(
    fill="x",
    pady=3
)


# ============================================================
# DISTANCIAS
# ============================================================

etiqueta_distancia = tk.Label(
    marco_resultados,
    text="",
    bg="#eeeeee",
    fg="#222222",
    font=("Arial", 10),
    justify="left",
    anchor="w"
)

etiqueta_distancia.pack(
    fill="x",
    pady=3
)


# ============================================================
# HEURÍSTICAS
# ============================================================

etiqueta_heuristica = tk.Label(
    marco_resultados,
    text="",
    bg="#eeeeee",
    fg="#333333",
    font=("Courier", 9),
    justify="left",
    anchor="w"
)

etiqueta_heuristica.pack(
    fill="x",
    pady=3
)


# ============================================================
# 22. DIBUJAR MAPA INICIAL
# ============================================================

dibujar_grafo()


# ============================================================
# 23. INICIAR PROGRAMA
# ============================================================

ventana.mainloop()
