#tarjeta

class Tarjeta:

    """
    Representa la tarjeta de un cliente del sistema.
    
    Almacena la identidad segura (hash), el saldo disponible y lleva un 
    registro acumulativo de los gastos asociados para fines estadísticos.
    """

    def __init__(self, hashId: str, saldo: float):
        self.hashId = hashId
        self.saldo = saldo
        self.totalGastado = 0.0

    def descontarSaldo(self, monto: float) -> bool:
        
        """
        Verifica el saldo disponible y procesa el cobro del producto.
        
        Si los fondos son suficientes, descuenta el monto, actualiza el
        acumulado de gastos y confirma la transacción.
        """

        if self.saldo >= monto:
            self.saldo -= monto
            self.totalGastado += monto
            return True
        return False

    def getSaldo(self) -> float:

        """Devuelve el saldo remanente en la tarjeta."""
        
        return self.saldo

    def getTotalGastado(self) -> float:

        """Devuelve el total histórico de dinero gastado con esta tarjeta."""

        return self.totalGastado
