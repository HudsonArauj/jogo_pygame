import pygame
import random

pygame.init()

comprimento = 500
altura = 450

comprimento_fundo = 568
altura_fundo = 513

comprimento_letras = 40
altura_letras = 40

posicao_x_letra = 225
posicao_y_letra = 0

comprimento_jogador = 90
altura_jogador = 90

window = pygame.display.set_mode((comprimento, altura))
pygame.display.set_caption('Diploma Battle')

background = pygame.image.load('imagens/fachada_insper.jpg').convert()
background = pygame.transform.scale(background, (comprimento_fundo, altura_fundo))
letra_I_imagem = pygame.image.load('imagens/letra_i.png').convert_alpha()
letra_D_imagem = pygame.image.load('imagens/letra_d.png').convert_alpha()
letra_I_imagem = pygame.transform.scale(letra_I_imagem, (comprimento_letras, altura_letras))
letra_D_imagem = pygame.transform.scale(letra_D_imagem, (comprimento_letras, altura_letras))
jogador_imagem = pygame.image.load('imagens/player2.png').convert_alpha()
jogador_imagem = pygame.transform.scale(jogador_imagem, (comprimento_jogador, altura_jogador))

class Letra(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = posicao_x_letra
        self.rect.y = posicao_y_letra
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > comprimento:
            self.rect.x =posicao_x_letra
            self.rect.y = posicao_y_letra
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

class Aluno(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = comprimento/2
        self.rect.bottom = altura - 5
        self.speedx = 0
    
    def update(self):
        self.rect.x += self.speedx
        # Não deixa o jogador sair da tela.
        if self.rect.right > comprimento:
            self.rect.right = comprimento

        if self.rect.left < 0:
            self.rect.left = 0




todos_elementos = pygame.sprite.Group()
todas_letras = pygame.sprite.Group()
jogador = Aluno(jogador_imagem)
todos_elementos.add(jogador)

for a in range(4):
    letra_I = Letra(letra_I_imagem)
    letra_D = Letra(letra_D_imagem)
    todos_elementos.add(letra_I)
    todos_elementos.add(letra_D)
    todas_letras.add(letra_I)
    todas_letras.add(letra_D)

game = True
clock = pygame.time.Clock() #Ajustando a velocidade
FPS = 30
v = 8

#Loop principal
while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jogador.speedx -= v
            if event.key == pygame.K_RIGHT:
                jogador.speedx += v
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                jogador.speedx += v
            if event.key == pygame.K_RIGHT:
                jogador.speedx -= v

    
    todos_elementos.update()
    #verifica se tem colisões com as letras
    colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True)
    if len(colisoes)>0:
        game = False
        
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (-20, 0))

    todos_elementos.draw(window)

    #Atualiza jogo
    pygame.display.update()  

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
