#Casilla

from producto import Producto


class Casilla:

    def __init__(self, coordenada: str, producto: Producto = None, cantidadActual: int = 0):

        self.coordenada = coordenada
        self.cantidadActual = cantidadActual
        self.agregadoUltimoStock = cantidadActual
        self.cantidadVendida = 0
        self.producto = producto

    def dispensar(self) -> None:

        self.cantidadActual -= 1
        self.cantidadVendida += 1

    def setProducto(self, producto: Producto) -> None:
        #L: cambio para hacer que podamos cambiar cosas en el producto sin tener que cambiar en todos los archivos  
        self.producto = producto

    def estaVacia(self) -> bool:

        return self.producto is None or self.cantidadActual <= 0

    def obtenerMetricas(self) -> dict:

        nombre = self.producto.getNombre() if self.producto else "Vacía"
        codigo = self.producto.getCodigo() if self.producto else ""
        precio = self.producto.getPrecio() if self.producto else 0.0
        return {
            "coordenada": self.coordenada,
            "nombre": nombre,
            "codigo": codigo,
            "precio": precio,
            "agregadoUltimoStock": self.agregadoUltimoStock,
            "cantidadVendida": self.cantidadVendida,
            "cantidadActual": self.cantidadActual
        }
