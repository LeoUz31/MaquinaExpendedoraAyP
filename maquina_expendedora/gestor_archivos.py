#gestor_archivos
import json
import os


class GestorArchivos:

    """
    Gestiona la lectura y escritura de archivos locales del sistema.
    
    Se encarga de persistir el inventario en formato JSON, guardar los reportes
    de ventas en texto y exportar las gráficas generadas.
    """

    def __init__(self, rutaInventario: str, rutaReportes: str):

        self.rutaInventario = rutaInventario
        self.rutaReportes = rutaReportes

    def leerEstadoLocal(self) -> dict:

        """
        Lee el archivo de inventario local y lo convierte en un diccionario.
        
        Devuelve un diccionario vacío si el archivo no existe o está corrupto.
        """

        if not os.path.exists(self.rutaInventario):
            return {}
        try:
            with open(self.rutaInventario, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception:
            return {}

    def guardarEstadoLocal(self, datos: dict) -> None:

        """
        Guarda los datos actualizados del inventario en el archivo JSON local.
        
        Crea las carpetas necesarias en la ruta si estas no existen.
        """
        
        directorio = os.path.dirname(self.rutaInventario)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        with open(self.rutaInventario, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

    def generarArchivoReporteTexto(self, texto_reporte: str) -> None:

        """
        Escribe el contenido del reporte de ventas en un archivo de texto plano.
        """

        directorio = os.path.dirname(self.rutaReportes)

        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        with open(self.rutaReportes, "w", encoding="utf-8") as archivo:
            archivo.write(texto_reporte)

    def guardarGraficas(self, figuras: list) -> None:

        """
        Guarda una lista de gráficos estadísticos (figuras de matplotlib) 
        en la carpeta de reportes.
        """

        directorio = os.path.dirname(self.rutaReportes)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        for figura, nombre in figuras:
            ruta_grafica = os.path.join(
                os.path.dirname(self.rutaReportes), nombre
            )
            figura.savefig(ruta_grafica)
