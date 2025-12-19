# Arquivo principal para iniciar o PyFoot25
import sys
from core.game import main_loop

def detecta_pygame():
    try:
        import pygame
        return True
    except ImportError:
        return False

if __name__ == "__main__":
    modo_grafico = detecta_pygame()
    if len(sys.argv) > 1 and sys.argv[1] == "--texto":
        modo_grafico = False
    main_loop(modo_grafico=modo_grafico)
