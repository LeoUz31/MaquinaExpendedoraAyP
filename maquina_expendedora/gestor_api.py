#gestor_api
import json
import urllib.request


class GestorAPI:

    """
    Gestiona la descarga y sincronización de datos desde un repositorio remoto.
    
    Se encarga de conectar con las URLs de GitHub para obtener la información
    actualizada de los productos y clientes de la máquina expendedora.
    """

    def __init__(self, urlRepositorio=None):
        self.urlRepositorio = urlRepositorio

        self.urlProductos = (
            "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/main/productos.json"
        )

        self.urlClientes = (
            "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/main/clientes.json"
        )
    def descargarJSON(self, url):

        """
        Realiza una petición web para descargar y parsear un archivo JSON.
        
        Devuelve un diccionario/lista con los datos o None si ocurre un error.
        """


        try:
            with urllib.request.urlopen(url, timeout=10) as respuesta:
                contenido = respuesta.read().decode("utf-8")
                return json.loads(contenido)

        except Exception as e:
            print(f"Error al conectar con GitHub: {e}")
            return None

    def verificarCambiosPrecio(self):

        """
        Descarga los datos actuales de productos y clientes para sincronizar el sistema.
        
        Devuelve un diccionario con toda la información unificada o None si falla
        la descarga de algún archivo.
        """


        productos = self.descargarJSON(self.urlProductos)
        clientes = self.descargarJSON(self.urlClientes)

        if productos is None or clientes is None:
            return None

        return {
            "productos": productos,
            "clientes": clientes
        }
