#maquina_expendedora
import os
import re #L: agregado para evitar un error de input
from inventario import Inventario
from gestor_tarjetas import GestorTarjetas
from gestor_archivos import GestorArchivos
from gestor_api import GestorAPI
from reporteador import Reporteador



class MaquinaExpendedora:


    """
    Clase principal que coordina los subsistemas de la máquina expendedora.
    
    Orquesta el flujo del inventario, la autorización de tarjetas, el acceso a la 
    API remota, la persistencia de datos en archivos locales y la generación de reportes.
    """

    def __init__(self):

        self.inventario = Inventario()
        self.gestorTarjetas = GestorTarjetas()
        self.gestorArchivos = GestorArchivos(
            rutaInventario="./datos/inventario.json",
            rutaReportes="./datos/reporte.txt"
        )
        self.gestorAPI = GestorAPI(
            urlRepositorio="https://github.com/FernandoSapient/BPTSP05_2526-3"
        )
        self.reporteador = Reporteador()

    def iniciarSistema(self) -> None:
        
        
        """
        Carga el estado inicial de la máquina desde el almacenamiento local
        e intenta sincronizar productos y clientes desde el repositorio remoto.
        """
        
        print("Iniciando sistema de máquina expendedora...")

        # Paso 1: Cargar inventario local
        estado_local = self.gestorArchivos.leerEstadoLocal()
        if estado_local:
            inventario_datos = estado_local.get("inventario", {})
            if inventario_datos:
                self.inventario.cargarCatalogo(inventario_datos)
                print("✓ Inventario cargado desde archivo local.")
            else:
                print("⚠ Archivo local sin inventario. Máquina iniciando vacía.")

            tarjetas_datos = estado_local.get("tarjetas", {})
            if tarjetas_datos:
                self.gestorTarjetas.cargarTarjetasValidas(tarjetas_datos)
                print("✓ Tarjetas cargadas desde archivo local.")
        else:
            print("⚠ No se encontró archivo local. Máquina iniciando vacía.")

        # Paso 2: Conectar al repositorio y verificar cambios
        print("Conectando al repositorio de GitHub...")
        datos_remotos = self.gestorAPI.verificarCambiosPrecio()

    

        if datos_remotos:
            print("✓ Conexión exitosa. Actualizando datos desde repositorio.")

            productos_remotos = datos_remotos.get("productos", [])
            #L: Lo pongo aca pq sino no funciona sin internet
            clientes_remotos = datos_remotos.get("clientes", [])
            if productos_remotos:

                inventario_convertido = {}

                fila = 1
                letra = "A"
                #L: en la mayoria agrego .get para evitar error 
                for producto in productos_remotos:

                    coordenada = f"{letra}{fila}"

                    inventario_convertido[coordenada] = {
                        "codigoLetras": producto.get("cod", ""),
                        "nombreCompleto": producto.get("prod", ""),
                        "precio": float(producto.get("precio", 0.0)),
                        "mensajeDespedida": producto.get("despedida", ""),
                        "cantidad": 10
                    }

                    fila += 1

                    if fila > 9:
                        fila = 1
                        letra = chr(ord(letra) + 1)

                self.inventario.cargarCatalogo(inventario_convertido)

                print("✓ Productos cargados desde GitHub.")
            

        if clientes_remotos:

            tarjetas_convertidas = {}

            for cliente in clientes_remotos:
                #L: Agregue el .get
                tarjetas_convertidas[str(cliente.get("id", ""))] = {
                    "saldo": float(cliente.get("saldo", 0.0))
                }

            self.gestorTarjetas.cargarTarjetasValidas(
                tarjetas_convertidas
            )

            print("✓ Clientes cargados desde GitHub.")

            # Guardar estado actualizado localmente
            self._guardarEstado()
        else:
            print("⚠ No se pudo conectar al repositorio. Usando datos locales.")

        print("Sistema listo.\n")
    
    def _moduloEsc(self) -> None:
        """
        Módulo para salir del sistema de manera segura.
        Guarda el estado actual antes de salir.
        """
        print("\n--- SALIENDO DEL SISTEMA ---")
        
        try:
            # Guardar estado actual antes de salir
            self._guardarEstado()
            print("✓ Estado guardado correctamente.")
            
            # Confirmar salida
            confirmacion = input("¿Está seguro que desea salir? (s/n): ").strip().lower()
            if confirmacion == "s":
                print("¡Hasta luego! Cerrando máquina expendedora...")
                exit(0)  # Salir del programa
            elif confirmacion == "n":
                print("Operación cancelada. Regresando al menú principal.")
            else:
                print("⚠ Ingrese un dato valido")
                
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada. Regresando al menú principal.")

    def mostrarMenu(self) -> None:

        print("\n" + "=" * 55)
        print("         MÁQUINA EXPENDEDORA - CATÁLOGO")
        print("=" * 55)
        self.inventario.imprimirCatalogo()
        print("-" * 55)
        print("Opciones: [coordenada] Comprar  |  RS Restock  |  RP Reporte | ESC Salir")
        print("-" * 55)

    def procesarComando(self, comando: str) -> None:
        comando = comando.strip().upper()

        if comando == "RS":
            self._moduloRestock()
        elif comando == "RP":
            self._moduloReporte()
        elif comando == "ESC":
            self._moduloEsc()
        else:
            self._moduloVenta(comando)

    def _moduloVenta(self, coordenada: str) -> None:

        if coordenada not in self.inventario.matrizCasillas:
            print(f"⚠ La coordenada '{coordenada}' no existe en el catálogo.")
            return

        casilla = self.inventario.matrizCasillas[coordenada]

        if casilla.estaVacia():
            print(f"⚠ No hay existencias disponibles en {coordenada}.")
            return

        producto = casilla.producto
        print(f"\nProducto  : {producto.getNombre()} ({producto.getCodigo()})")
        print(f"Precio    : {producto.getPrecio():.2f}")

        # Solicitar número de tarjeta
        #L: utilizo try y except para evitar errores por el input(KeyboardInterrupt)
        try:
            numero_tarjeta = input("Introduzca su número de tarjeta (Enter para cancelar): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Venta cancelada.")
            return
        if not numero_tarjeta:
            print("Venta cancelada.")
            return

        hash_tarjeta = self.gestorTarjetas.obtenerHash(numero_tarjeta)

        

        if not self.gestorTarjetas.validarTarjeta(hash_tarjeta):
            print("⚠ Tarjeta no válida. Venta cancelada.")
            return

        tarjeta = self.gestorTarjetas.baseTarjetas[hash_tarjeta]
        print(f"Saldo disponible: {tarjeta.getSaldo():.2f}")

        # Pedir confirmación
        #L: Otra vez lo del input
        try:
            confirmacion = input(
                f"¿Confirma la compra de '{producto.getNombre()}' por {producto.getPrecio():.2f}? (s/n): "
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("Venta cancelada.")
            return

        if confirmacion != "s":
            print("Venta cancelada.")
            return

        # Procesar pago
        if not self.gestorTarjetas.procesarPago(hash_tarjeta, producto.getPrecio()):
            print("⚠ Saldo insuficiente. Venta cancelada.")
            return

        # Descontar stock y registrar venta
        casilla.dispensar()
        self.reporteador.registrarVenta(casilla, tarjeta)

        # Persistir estado actualizado
        self._guardarEstado()

        print(f"\n>>> Dispensando {producto.getNombre()}...")
        #L: Utilizo el getMensajeDespedida que agregue
        print(f">>> {producto.getMensajeDespedida()}")


    def _moduloRestock(self) -> None:

        print("\n--- MÓDULO DE RESTOCK ---")
        print("1. Actualizar existencia de inventario")
        print("2. Cambiar producto")

        while True:
            opcion = input("Seleccione una opción (1 o 2): ").strip()
            if opcion in ("1", "2"):
                break
            print("⚠ Opción no válida. Ingrese 1 o 2.")

        coordenada = input("Ingrese la coordenada (e.g. A1): ").strip().upper()
        if not coordenada:
            print("⚠ Coordenada vacía. Operación cancelada.")
            return

        #L: Al escribir cualquier cosa que no tuviera formato de coordenada petaba, esto es por si no tiene formato de coordenada
        if not re.fullmatch(r"[A-Z]\d+", coordenada):
            print("⚠ Formato de coordenada inválido. Debe ser una letra seguida de un número (ej. A1).")
            return
        
        if opcion == "1":
            while True:
                cantidad_str = input("Ingrese la nueva cantidad: ").strip()
                try:
                    cantidad = int(cantidad_str)
                    #L: Se podia poner cantidad negativa (No se muy bien si prefieres que sea asi para poder quitar cosas pero como es restock no se)
                    if cantidad < 0:
                        print("⚠ La cantidad no puede ser negativa.")
                        continue
                    break
                except ValueError:
                    print("⚠ Entrada inválida. Debe ingresar un número entero.")

            self.inventario.actualizarStock(coordenada, cantidad)
            self._guardarEstado()
            print(f"✓ Existencia de {coordenada} actualizada a {cantidad}.")

        elif opcion == "2":
            nuevo_codigo = input("Ingrese el nuevo código de 5 letras del producto: ").strip()
            if not nuevo_codigo:
                print("⚠ Código vacío. Operación cancelada.")
                return

            while True:
                cantidad_str = input("Ingrese la cantidad en existencia: ").strip()
                try:
                    cantidad = int(cantidad_str)
                    #L: otra vez se podia poner input negativo
                    if cantidad < 0:
                        print("⚠ La cantidad no puede ser negativa.")
                        continue
                    break
                except ValueError:
                    print("⚠ Entrada inválida. Debe ingresar un número entero.")

            self.inventario.cambiarProducto(coordenada, nuevo_codigo, cantidad)
            self._guardarEstado()
            print(f"✓ Producto en {coordenada} cambiado a '{nuevo_codigo}' con {cantidad} unidades.")


    def _moduloReporte(self) -> None:
        print("\n--- GENERANDO REPORTE ---")

        casillas = list(self.inventario.matrizCasillas.values())
        tarjetas = list(self.gestorTarjetas.baseTarjetas.values())

        texto_reporte = self.reporteador.generarReporteTexto(casillas, tarjetas)
        print(texto_reporte)
        print("Ruta reporte:", self.gestorArchivos.rutaReportes)

        # Guardar reporte en archivo de texto
        try:
            directorio = os.path.dirname(self.gestorArchivos.rutaReportes)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            with open(self.gestorArchivos.rutaReportes, "w", encoding="utf-8") as f:
                f.write(texto_reporte)
            print(f"\n✓ Reporte guardado en: {self.gestorArchivos.rutaReportes}")
        except Exception as e:
            print(f"⚠ No se pudo guardar el reporte: {e}")

        # Generar y guardar gráficas
        try:
            figuras = self.reporteador.generarGraficasMatplotlib()
            self.gestorArchivos.guardarGraficas(figuras)
            print(f"✓ Gráficas guardadas en: {os.path.dirname(self.gestorArchivos.rutaReportes)}/")
        except Exception as e:
            print(f"⚠ No se pudieron generar las gráficas: {e}")


    def _guardarEstado(self) -> None:
        datos_inventario = {}
        for coord, casilla in self.inventario.matrizCasillas.items():
            if casilla.producto:
                datos_inventario[coord] = {
                    "codigoLetras": casilla.producto.getCodigo(),
                    "nombreCompleto": casilla.producto.getNombre(),
                    "precio": casilla.producto.getPrecio(),
                    #Uso el getMensajeDespedida que agregue para que sea igual que los otros atributos
                    "mensajeDespedida": casilla.producto.getMensajeDespedida(),
                    "cantidad": casilla.cantidadActual,
                    "agregadoUltimoStock": casilla.agregadoUltimoStock,
                    "cantidadVendida": casilla.cantidadVendida
                }
            else:
                datos_inventario[coord] = {
                    "codigoLetras": "",
                    "nombreCompleto": "",
                    "precio": 0.0,
                    "mensajeDespedida": "",
                    "cantidad": casilla.cantidadActual,
                    "agregadoUltimoStock": casilla.agregadoUltimoStock,
                    "cantidadVendida": casilla.cantidadVendida
                }

        datos_tarjetas = {}
        for hash_id, tarjeta in self.gestorTarjetas.baseTarjetas.items():
            datos_tarjetas[hash_id] = {
                "saldo": tarjeta.getSaldo(),
                "totalGastado": tarjeta.getTotalGastado()
            }

        estado = {
            "inventario": datos_inventario,
            "tarjetas": datos_tarjetas
        }
        self.gestorArchivos.guardarEstadoLocal(estado)
