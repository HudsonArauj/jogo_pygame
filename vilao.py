import random
import pygame
from constantes import *
from recursos import *

#Cria a classe letra
class Letra(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.mask = pygame.mask.from_surface(self.image) #Melhora colisão
        self.rect = self.image.get_rect()
        self.rect.x = posicao_x_letra + comprimento_professor/2
        self.rect.y = posicao_y_letra + altura_professor/2
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 7)

    def update(self):
        # Atualizando a posição da letra
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se a letra passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > comprimento:
            self.rect.x =posicao_x_letra + comprimento_professor/2
            self.rect.y = posicao_y_letra + altura_professor/2
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 7)

#Cria a classe professor
class Professor(pygame.sprite.Sprite):
    def __init__(self, recursos, grupos):
        #Construtor da classe mãe(Sprite)
        pygame.sprite.Sprite.__init__(self)
        self.pos = 0
        self.image = recursos['professor_imagem'][self.pos]   
        self.mask = pygame.mask.from_surface(self.image)   #Melhora colisão
        self.rect = self.image.get_rect()     
        self.rect.centerx = comprimento/2  #Define posição no eixo x
        self.rect.top = 5    #Define posição no eixo y
        self.grupos = grupos
        self.recursos = recursos
    def update(self):
        self.pos = (self.pos+1)%len(self.recursos['professor_imagem']) #faz as imagens formarem um loop
        self.image = self.recursos['professor_imagem'][self.pos]