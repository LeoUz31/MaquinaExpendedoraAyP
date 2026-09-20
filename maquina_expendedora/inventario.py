#inventario
from casilla import Casilla
from producto import Producto


class Inventario:
    """
    Gestiona el conjunto de casillas y la distribución física de la máquina.
    
    Controla la carga del catálogo, la búsqueda de productos, el renderizado de la 
    matriz visual de la máquina y la actualización de stock mediante optimización por caché.
    """

    def __init__(self):

        self.matrizCasillas: dict = {}
        self._columnasCache: list = []
        self._filasCache: list = []

    def _recalcularEstructura(self) -> None:

        """
        Calcula y almacena en caché el orden de filas y columnas de la matriz.
        
        Evita procesar y ordenar las coordenadas en cada renderizado del catálogo.
        """

        self._columnasCache = sorted(set(c[0] for c in self.matrizCasillas.keys()))
        self._filasCache = sorted(set(int(c[1:]) for c in self.matrizCasillas.keys()))

    def cargarCatalogo(self, datos: dict) -> None:

        """
        Puebla el inventario de la máquina a partir de un diccionario de datos.
        """

        self.matrizCasillas = {}
        for coordenada, info in datos.items():
            producto = Producto(
                codigoLetras=info["codigoLetras"],
                nombreCompleto=info["nombreCompleto"],
                precio=float(info["precio"]),
                mensajeDespedida=info["mensajeDespedida"]
            )
            casilla = Casilla(
                coordenada=coordenada,
                producto=producto,
                cantidadActual=int(info["cantidad"])
            )
            casilla.agregadoUltimoStock = int(info.get("agregadoUltimoStock", info["cantidad"]))
            casilla.cantidadVendida = int(info.get("cantidadVendida", 0))
            self.matrizCasillas[coordenada] = casilla
        
        #L: Recalcular cache estructura despues de cargar el catálogo
        self._recalcularEstructura()


    def imprimirCatalogo(self) -> None:

        """
        Muestra en consola la distribución visual de la máquina como una matriz alfanumérica.
        """
        
        if not self.matrizCasillas:
            print("  [Máquina vacía]")
            return
        
        #L: para esto lo guarde en variables, para que no se realize la funcion siempre que se imprime
        columnas = self._columnasCache
        filas = self._filasCache

        encabezado = "   " + "  ".join(f"{col:^7}" for col in columnas)
        print(encabezado)
        print("   " + "-" * (9 * len(columnas)))

        for fila in filas:
            fila_str = f"{fila:<3}"
            for col in columnas:
                coord = f"{col}{fila}"
                if coord in self.matrizCasillas:
                    casilla = self.matrizCasillas[coord]
                    if casilla.estaVacia():
                        fila_str += f"{'':^7}  "
                    else:
                        fila_str += f"{casilla.producto.getCodigo():^7}  "
                else:
                    fila_str += f"{'':^7}  "
            print(fila_str)

    def buscarProducto(self, coordenada: str) -> Producto:
        
        """
        Busca y retorna el producto de una casilla específica si cuenta con existencias.
        """
        
        coordenada = coordenada.upper()
        if coordenada in self.matrizCasillas:
            casilla = self.matrizCasillas[coordenada]
            if not casilla.estaVacia():
                return casilla.producto
        return None

    def actualizarStock(self, coordenada: str, cantidad: int) -> None:

        """
        Modifica la cantidad disponible en una casilla o crea una nueva si no existía.
        """

        coordenada = coordenada.upper()
        if coordenada in self.matrizCasillas:
            self.matrizCasillas[coordenada].cantidadActual = cantidad
            self.matrizCasillas[coordenada].agregadoUltimoStock = cantidad
        else:
            nueva = Casilla(coordenada=coordenada, cantidadActual=cantidad)
            nueva.agregadoUltimoStock = cantidad
            self.matrizCasillas[coordenada] = nueva

        #Recalcular cache de estructura despues de modificar matrizCasillas
        self._recalcularEstructura()

    def cambiarProducto(self, coordenada: str, nuevoCodigo: str, cantidad: int) -> None:

        """
        Asigna un nuevo producto a una coordenada, reutilizando instancias existentes 
        o creando una plantilla genérica si es un artículo nuevo.
        """

        coordenada = coordenada.upper()

        # Buscar si el producto ya existe en alguna casilla
        producto_encontrado = None
        for cas in self.matrizCasillas.values():
            if cas.producto and cas.producto.getCodigo().upper() == nuevoCodigo.upper():
                producto_encontrado = cas.producto
                break

        if producto_encontrado is None:
            # Crear un producto básico con la información disponible
            producto_encontrado = Producto(
                codigoLetras=nuevoCodigo,
                nombreCompleto=nuevoCodigo,
                precio=0.0,
                mensajeDespedida=f"¡Gracias por comprar {nuevoCodigo}!"
            )

        if coordenada in self.matrizCasillas:
            #L: Aprovecho la funcion de casilla
            self.matrizCasillas[coordenada].setProducto(producto_encontrado)
            self.matrizCasillas[coordenada].cantidadActual = cantidad
            self.matrizCasillas[coordenada].agregadoUltimoStock = cantidad
            self.matrizCasillas[coordenada].cantidadVendida = 0
        else:
            nueva = Casilla(coordenada=coordenada, producto=producto_encontrado, cantidadActual=cantidad)
            nueva.agregadoUltimoStock = cantidad
            self.matrizCasillas[coordenada] = nueva
        #Actualizar el cache estructura al modificar matrizCasillas
        self._recalcularEstructura()
