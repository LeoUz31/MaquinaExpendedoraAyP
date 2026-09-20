#Reporteador

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Reporteador:

    """
    Se encarga de recopilar las métricas de ventas y generar los informes del sistema.
    
    Registra las transacciones en tiempo real, genera reportes estructurados en texto
    y renderiza gráficos estadísticos (barras, pastel y líneas) con matplotlib.
    """

    def __init__(self):

        self.cantidadTotalProductosVendidos: int = 0
        self.dineroTotalCobrado: float = 0.0
        self.cantidadUsuariosUnicos: int = 0
        self._historialVentas: list = []

    def registrarVenta(self, casilla, tarjeta) -> None:

        """
        Registra los detalles de una transacción exitosa.
        
        Actualiza los contadores globales e inserta un nuevo registro en el historial.
        """

        if casilla.producto:
            precio = casilla.producto.getPrecio()
            self.cantidadTotalProductosVendidos += 1
            self.dineroTotalCobrado += precio
            self._historialVentas.append({
                "coordenada": casilla.coordenada,
                "producto": casilla.producto.getNombre(),
                "precio": precio,
                "hashTarjeta": tarjeta.hashId,
                "totalVendidoAcumulado": self.cantidadTotalProductosVendidos
            })

    def generarReporteTexto(self, casillas: list, tarjetas: list) -> str:
        
        """
        Construye un informe formateado en texto plano con el balance comercial.
        
        Muestra el desglose de existencias por casilla, los ingresos totales y el 
        gasto individualizado por usuario único.
        """
        
        lineas = []
        lineas.append("=" * 50)
        lineas.append("       REPORTE DE VENTAS - MÁQUINA EXPENDEDORA")
        lineas.append("=" * 50)
        lineas.append("")
        lineas.append("--- PRODUCTOS ---")
        lineas.append(f"{'Coordenada':<12} {'Producto':<20} {'Cargado':<10} {'Vendido':<10} {'Restante':<10}")
        lineas.append("-" * 62)

        for casilla in casillas:
            metricas = casilla.obtenerMetricas()
            lineas.append(
                f"{metricas['coordenada']:<12} "
                f"{metricas['nombre']:<20} "
                f"{metricas['agregadoUltimoStock']:<10} "
                f"{metricas['cantidadVendida']:<10} "
                f"{metricas['cantidadActual']:<10}"
            )

        lineas.append("")
        lineas.append(f"Total de productos vendidos : {self.cantidadTotalProductosVendidos}")
        lineas.append(f"Total de dinero cobrado     : {self.dineroTotalCobrado:.2f}")
        lineas.append("")
        lineas.append("--- USUARIOS ---")
        lineas.append(f"{'Hash de Tarjeta':<25} {'Total Gastado':<15}")
        lineas.append("-" * 40)

        usuarios_unicos = set()
        for tarjeta in tarjetas:
            if tarjeta.getTotalGastado() > 0:
                usuarios_unicos.add(tarjeta.hashId)
                lineas.append(f"{tarjeta.hashId:<25} {tarjeta.getTotalGastado():<15.2f}")

        self.cantidadUsuariosUnicos = len(usuarios_unicos)
        lineas.append("")
        lineas.append(f"Cantidad de usuarios únicos : {self.cantidadUsuariosUnicos}")
        lineas.append("=" * 50)

        return "\n".join(lineas)

    def generarGraficasMatplotlib(self) -> list:
        
        """
        Genera tres objetos de gráficas basados en el historial actual de ventas.
        
        - Gráfica 1: Barras con las unidades vendidas por tipo de producto.
        - Gráfica 2: Pastel con la distribución de gastos por usuario.
        - Gráfica 3: Línea con la evolución temporal acumulada de las ventas.
        
        Devuelve una lista de tuplas con la estructura (figura_plt, nombre_archivo).
        """
        
        figuras = []

        # --- Gráfica 1: Barras (cargado vs vendido por coordenada) ---
        if self._historialVentas:
            conteo_productos = {}
            cargado_productos = {}
            for venta in self._historialVentas:
                prod = venta["producto"]
                conteo_productos[prod] = conteo_productos.get(prod, 0) + 1

            nombres = list(conteo_productos.keys())
            vendidos = [conteo_productos[n] for n in nombres]

            fig1, ax1 = plt.subplots(figsize=(10, 5))
            x = range(len(nombres))
            ax1.bar([i - 0.2 for i in x], vendidos, width=0.4, label="Vendido", color="steelblue")
            ax1.set_xticks(list(x))
            ax1.set_xticklabels(nombres, rotation=45, ha="right")
            ax1.set_title("Unidades vendidas por producto")
            ax1.set_ylabel("Cantidad")
            ax1.legend()
            plt.tight_layout()
            figuras.append((fig1, "grafica_barras.png"))
        else:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.text(0.5, 0.5, "Sin datos de ventas", ha="center", va="center")
            ax1.set_title("Unidades cargadas vs vendidas por producto")
            figuras.append((fig1, "grafica_barras.png"))

        # --- Gráfica 2: Circular (compras por usuario) ---
        gasto_usuario = {}
        for venta in self._historialVentas:
            h = venta["hashTarjeta"]
            gasto_usuario[h] = gasto_usuario.get(h, 0) + venta["precio"]

        fig2, ax2 = plt.subplots(figsize=(7, 7))
        if gasto_usuario:
            etiquetas = [f"Usuario {i+1}" for i in range(len(gasto_usuario))]
            valores = list(gasto_usuario.values())
            ax2.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=140)
            ax2.set_title("Distribución de compras por usuario")
        else:
            ax2.text(0.5, 0.5, "Sin datos de ventas", ha="center", va="center")
            ax2.set_title("Distribución de compras por usuario")
        figuras.append((fig2, "grafica_circular.png"))

        # --- Gráfica 3: Línea (total vendido acumulado con cada venta) ---
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        if self._historialVentas:
            x_ventas = list(range(1, len(self._historialVentas) + 1))
            y_acumulado = [v["totalVendidoAcumulado"] for v in self._historialVentas]
            ax3.plot(x_ventas, y_acumulado, marker="o", color="green")
            ax3.set_title("Evolución acumulada de ventas")
            ax3.set_xlabel("Número de venta")
            ax3.set_ylabel("Total acumulado vendido")
        else:
            ax3.text(0.5, 0.5, "Sin datos de ventas", ha="center", va="center")
            ax3.set_title("Evolución acumulada de ventas")
        plt.tight_layout()
        figuras.append((fig3, "grafica_linea.png"))

        return figuras
