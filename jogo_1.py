import pygame
import random
import time

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
jogador_imagem = pygame.image.load('imagens/prof1.png').convert_alpha()
jogador_imagem = pygame.transform.scale(jogador_imagem, (comprimento_jogador, altura_jogador))
aviao_imagem = pygame.image.load('imagens/aviao_branco.png').convert_alpha()
aviao_imagem = pygame.transform.scale(aviao_imagem, (comprimento_letras, altura_letras))
pygame.mixer.music.load('sons/fundodojogo.mp3')
pygame.mixer.music.set_volume(0.4)
hit_professor = pygame.mixer.Sound('sons/atingeprof.wav')
lancamento_aviao = pygame.mixer.Sound('sons/lançamento.wav')
hit_aluno = pygame.mixer.Sound('sons/atingealuno.wav')


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
    def __init__(self, img, todos_elementos, todos_avioes, aviao_imagem, hit_aluno, lancamento_aviao):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = comprimento/2
        self.rect.bottom = altura - 5
        self.speedx = 0
        self.todos_elementos = todos_elementos
        self.todos_avioes = todos_avioes
        self.aviao_imagem = aviao_imagem
        self.direcao = 1  #Começa olhando pra direita
        self.hit_aluno = hit_aluno
        self.lancamento_aviao = lancamento_aviao
    
    def update(self):
        self.rect.x += self.speedx
        # Não deixa o jogador sair da tela.
        if self.rect.right > comprimento:
            self.rect.right = comprimento

        if self.rect.left < 0:
            self.rect.left = 0

    def lancamento(self):
        if self.direcao == 1:
            novo_aviao = Aviao(self.aviao_imagem, self.rect.centery,  self.rect.right)
        else:
            novo_aviao = Aviao(self.aviao_imagem, self.rect.centery,  (self.rect.left-comprimento_letras))
        self.todos_elementos.add(novo_aviao) 
        self.todos_avioes.add(novo_aviao)
        self.lancamento_aviao.play()
            
class Aviao(pygame.sprite.Sprite):
    def __init__(self, img, posicao_y, posicao_x, lancamento):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.y = posicao_y
        self.rect.x = posicao_x
        self.speedy = -5
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()


todos_elementos = pygame.sprite.Group()
todas_letras = pygame.sprite.Group()
todos_avioes = pygame.sprite.Group()

jogador = Aluno(jogador_imagem, todos_elementos, todos_avioes, aviao_imagem, hit_aluno, lancamento_aviao)
todos_elementos.add(jogador)

for a in range(4):
    letra_I = Letra(letra_I_imagem)
    letra_D = Letra(letra_D_imagem)
    todos_elementos.add(letra_I)
    todos_elementos.add(letra_D)
    todas_letras.add(letra_I)
    todas_letras.add(letra_D)

pygame.mixer.music.play(loops=-1)

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
                jogador.direcao = 0
            if event.key == pygame.K_RIGHT:
                jogador.speedx += v
                jogador.direcao = 1
            if event.key == pygame.K_SPACE:
                jogador.lancamento()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                jogador.speedx += v
            if event.key == pygame.K_RIGHT:
                jogador.speedx -= v

    
    todos_elementos.update()
    #verifica se tem colisões com as letras
    # colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True, True)
    
    colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True)
    letras = [letra_D_imagem, letra_I_imagem]
    for a in colisoes: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
        # O meteoro e destruido e precisa ser recriado
        random.shuffle(letras)
        imagem = Letra(letras[0])
        todos_elementos.add(imagem)
        todas_letras.add(imagem)
    if len(colisoes)>0:
        #game = False
        print('colidiu')
        hit_aluno.play()

    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (-20, 0))

    todos_elementos.draw(window)

    #Atualiza jogo
    pygame.display.update()  

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
