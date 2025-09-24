temperatura = None
humedad = None
actuator = None
clave_boxy = None
sala = None

import os

def limpiar_consola():
    if os.name == 'nt': # Para Windows
         os.system('cls')
    else: # Para Linux/macOS
        os.system('clear')
