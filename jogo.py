import pygame
from constantes import *
from tela_do_jogo import tela_jogo
from tela_inicio import tela_inicio
from tela_ganhou import tela_ganhou
from tela_perdeu import tela_perdeu

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
    elif estado == FINAL_RUIM:
        estado = tela_perdeu(window)
    elif estado == FINAL_BOM:
        estado = tela_ganhou(window)
    else:
        estado = QUIT

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
