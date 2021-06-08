import pygame
from os import path
from constantes import *

def tela_inicio(tela):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'perdeu.png')).convert()
    background = pygame.transform.scale(background, (comprimento_tela, altura_tela))
    background_rect = background.get_rect()

    acontecendo = True

    while acontecendo:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                estado = QUIT
                acontecendo = False

            if event.type == pygame.KEYUP:
                estado = GAME
                acontecendo = False
        # A cada loop, redesenha o fundo e os sprites
        tela.fill(BLACK)
        tela.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return estado