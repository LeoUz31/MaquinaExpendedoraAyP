#producto

class Producto:
    """
    Es un prodcuto individual disponible en la máquina expendedora.
    Almacena identificación, precio, mensaje de despedida y código del producto.


    """
    def __init__(self, codigoLetras: str, nombreCompleto: str, precio: float, mensajeDespedida: str):

        self.codigoLetras = codigoLetras
        self.nombreCompleto = nombreCompleto
        self.precio = precio
        self.mensajeDespedida = mensajeDespedida

    def getPrecio(self) -> float:
        """
        Obtener precio del producto.
        """
        return self.precio
        
    def getCodigo(self) -> str:
        """
        Obtener codigo del producto.
        """
        return self.codigoLetras

    def getNombre(self) -> str:
        """
        Obtener nombre del producto.
        """
        return self.nombreCompleto
    
    def getMensajeDespedida(self) -> str:
        """
        Obtener mensaje de despedida del producto.
        """
        return self.mensajeDespedida
