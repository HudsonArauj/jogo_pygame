import pygame
import random

pygame.init()

#tela principal
window = pygame.display.set_mode((450, 500))
pygame.display.set_caption('Diploma Battle')

background = pygame.image.load('imagens/fachada_insper.jpg').convert()
background_scale = pygame.transform.scale(background, (568, 513))
letra_I = pygame.image.load('imagens/letra_i.jpeg').convert_alpha()
letra_D = pygame.image.load('imagens/letra_d.jpeg').convert_alpha()
letra_I_menor = pygame.transform.scale(letra_I, (50, 50))
letra_D_menor = pygame.transform.scale(letra_D, (50, 50))

letra_ix = 225
letra_iy = 0

letra_dx = 225
letra_dy = 0

letra_i_speedx = random.randint(-3,3)
letra_i_speedy =  random.randint(2,9)

letra_d_speedx = random.randint(-3,3)
letra_d_speedy =  random.randint(2,9)


game = True

#Loop principal
while game:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game = False

    letra_ix += letra_i_speedx
    letra_iy += letra_i_speedy

    letra_dx += letra_d_speedx
    letra_dy += letra_d_speedy

    
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background_scale, (-20, 0))
    window.blit(letra_I_menor,(letra_ix,letra_iy))
    window.blit(letra_D_menor,(letra_dx,letra_dy))
    #Atualiza jogo
    pygame.display.update()  

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
