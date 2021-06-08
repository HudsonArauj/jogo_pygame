import pygame
from constantes import *
from tela_do_jogo import tela_jogo
from tela_inicio import tela_inicio

pygame.init()
pygame.mixer.init()

# ----Gera tela principal
window = pygame.display.set_mode((comprimento, altura))
pygame.display.set_caption('Diploma Battle')

estado = INIT
while estado != QUIT:
    if estado == INIT:
        estado = tela_inicio(window)
    elif estado == GAME:
        estado = tela_jogo(window)
    else:
        estado = QUIT

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
