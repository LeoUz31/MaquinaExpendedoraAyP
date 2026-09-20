#main

"""
Módulo principal para iniciar el programa. 
"""

from maquina_expendedora import MaquinaExpendedora


def main():
    maquina = MaquinaExpendedora()
    maquina.iniciarSistema()

    while True:
        maquina.mostrarMenu()
        try:
            comando = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSistema apagado. ¡Hasta luego!")
            break
        if not comando:
            continue

        maquina.procesarComando(comando)


if __name__ == "__main__":
    main()