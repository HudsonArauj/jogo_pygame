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
                novo_aviao = Aviao(self.recursos, self.rect.centery,  self.rect.right)
            else:
                #Sai da esquerda do jogador
                novo_aviao = Aviao(self.recursos, self.rect.centery,  (self.rect.left-comprimento_letras))
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
