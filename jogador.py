import random
import pygame
from constantes import *
from recursos import *

#Cria a classe aluno
class Aluno(pygame.sprite.Sprite):
    def __init__(self, recursos, grupos):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.pos = 2
        self.image = recursos['corridad'][self.pos]
        self.image = recursos['corridae'][self.pos]
        self.mask = pygame.mask.from_surface(self.image)   #Melhora colisão
        self.rect = self.image.get_rect()
        self.rect.centerx = comprimento/2
        self.rect.bottom = altura - 5
        self.speedx = 0
        self.grupos = grupos
        self.recursos = recursos
        self.direcao = 1  #Começa olhando pra direita

        #Só será possível atirar a cada 0,5 segundos
        self.ultimo_tiro = pygame.time.get_ticks()
        self.lancamento_aviao = 500
    
    def update(self):
        #Atualiza posição do aluno 
        self.rect.x += self.speedx
        # Não deixa o jogador sair da tela.
        if self.rect.right > comprimento:
            self.rect.right = comprimento

        if self.rect.left < 0:
            self.rect.left = 0
        if self.speedx > 0:
            self.pos = (self.pos+1)%len(self.recursos['corridad']) #faz as imagens formarem um loop
            self.image = self.recursos['corridad'][self.pos]
        if self.speedx < 0:
            self.pos = (self.pos+1)%len(self.recursos['corridae']) #faz as imagens formarem um loop
            self.image = self.recursos['corridae'][self.pos]
        
    def lancamento(self):
        #Verifica se pode jogar o avião
        agora  = pygame.time.get_ticks()
        #Verifica quantos ticks se passaram desde o último lançamento
        colapso_aviao = agora - self.ultimo_tiro
        #Se já pode lançar novamente...
        if colapso_aviao > self.lancamento_aviao:
            #Marca o tick da nova imagem
            self.ultimo_tiro = agora
            #O novo avião vai ser criado do lado em que o jogador estiver virado
            if self.direcao == 1:
                #Sai da direita do jogador
                novo_aviao = Aviao(self.recursos, self.rect.centery,  self.rect.right - 10)
            else:
                #Sai da esquerda do jogador
                novo_aviao = Aviao(self.recursos, self.rect.centery,  (self.rect.left-comprimento_letras + 10))
            self.grupos['todos_elementos'].add(novo_aviao)
            self.grupos['todos_avioes'].add(novo_aviao)
            self.recursos['lancamento_aviao'].play()

#Cria a classe avião            
class Aviao(pygame.sprite.Sprite):
    #Construtor da classe mãe(Sprite)
    def __init__(self, recursos, posicao_y, posicao_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = recursos['aviao_imagem']
        self.mask = pygame.mask.from_surface(self.image)   #Melhora colisão
        self.rect = self.image.get_rect()
        #Coloca no local inical definidi em x, y do construtor
        self.rect.y = posicao_y  #Define posição do eixo y
        self.rect.x = posicao_x   #Define posição do eixo x
        self.speedy = -5  #Velocidade fixa para cima
    
    def update(self):
        #O avião só se move no eixo y
        self.rect.y += self.speedy
        #Se o avião passar do início da tela, morre.
        if self.rect.y < 0:
            self.kill()

#Cria a classe estrela
class Estrela(pygame.sprite.Sprite):
    def __init__(self, recursos, grupos):
         #Construtor da classe mãe(Sprite)
        pygame.sprite.Sprite.__init__(self)
        self.image = recursos['estrela_imagem']
        self.mask = pygame.mask.from_surface(self.image)   #Melhora colisão
        self.rect = self.image.get_rect()
        self.rect.bottom = altura - 25
        self.rect.centerx = random.randint(comprimento_estrela/2, (comprimento - comprimento_estrela/2))
        self.grupos = grupos
        self.recursos = recursos