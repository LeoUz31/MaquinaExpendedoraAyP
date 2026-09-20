#gestor_tarjetas
from tarjeta import Tarjeta
import json


class GestorTarjetas:

    """
    Gestiona el conjunto de tarjetas válidas y autoriza los pagos en el sistema.
    
    Permite cargar el saldo de los clientes, validar la identidad de las tarjetas
    y procesar los cobros correspondientes.
    """

    def __init__(self):

        self.baseTarjetas: dict = {}
    
    def cargarTarjetasValidas(self, datos: dict) -> None:

        """
        Mapea y registra las tarjetas activas a partir de un diccionario de datos.
        """

        self.baseTarjetas = {}
        for hashId, info in datos.items():
            tarjeta = Tarjeta(
                hashId=str(hashId),
                saldo=float(info["saldo"])
            )
            tarjeta.totalGastado = float(info.get("totalGastado", 0.0))
            self.baseTarjetas[str(hashId)] = tarjeta

    def obtenerHash(self, numero: str) -> str:
        
        """
        Busca el identificador único (hash) de una tarjeta usando el archivo de equivalencias.
        """
        
        with open('equivalencias.json', 'r') as archivo:
            equivalencias_json = json.load(archivo)
        equivalencias = equivalencias_json.get("equivalencias", {})
        return equivalencias.get(numero, "")

    """
    Esta es la función básica del hash, sin embargo, debido a la naturaleza de esta función no es posible decifrar las tarjetas o cifrarlas de las misma manera en las que se cifro en el github.
    def obtenerHash(self, numero: str) -> str:
        return str(hash(numero))
    """
    def validarTarjeta(self, hash_id: str) -> bool:

        """
        Verifica si el identificador de la tarjeta existe en los registros actuales.
        """

        return hash_id in self.baseTarjetas

    def procesarPago(self, hash_id: str, monto: float) -> bool:

        """
        Descuenta el monto solicitado de la tarjeta si esta es válida y cuenta con saldo suficiente.
        """
        
        if not self.validarTarjeta(hash_id):
            return False
        return self.baseTarjetas[hash_id].descontarSaldo(monto)
