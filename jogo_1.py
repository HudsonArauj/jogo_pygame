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

recursos = {}
recursos['background'] = pygame.image.load('imagens/fachada_insper.jpg').convert()
recursos['background'] = pygame.transform.scale(recursos['background'], (comprimento_fundo, altura_fundo))
recursos['letra_I_imagem'] = pygame.image.load('imagens/letra_i.png').convert_alpha()
recursos['letra_D_imagem'] = pygame.image.load('imagens/letra_d.png').convert_alpha()
recursos['letra_I_imagem'] = pygame.transform.scale(recursos['letra_I_imagem'], (comprimento_letras, altura_letras))
recursos['letra_D_imagem'] = pygame.transform.scale(recursos['letra_D_imagem'], (comprimento_letras, altura_letras))
recursos['aviao_imagem'] = pygame.image.load('imagens/aviao_branco.png').convert_alpha()
recursos['aviao_imagem'] = pygame.transform.scale(recursos['aviao_imagem'], (comprimento_letras, altura_letras))
pygame.mixer.music.load('sons/fundodojogo.mp3')
pygame.mixer.music.set_volume(0.4)
recursos['hit_professor'] = pygame.mixer.Sound('sons/atingeprof.wav')
recursos['lancamento_aviao'] = pygame.mixer.Sound('sons/lançamento.wav')
recursos['hit_aluno'] = pygame.mixer.Sound('sons/atingealuno.wav')

corrida = []
for i in range(1,11):
    nome_arquivo = 'imagens/mov{}.png'.format(i)
    jogador_imagem = pygame.image.load(nome_arquivo).convert_alpha()
    jogador_imagem = pygame.transform.scale(jogador_imagem, (comprimento_jogador, altura_jogador))
    corrida.append(jogador_imagem)
recursos['corrida'] = corrida


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
    def __init__(self, recursos, grupos):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = recursos['corrida']
        self.rect = self.image.get_rect()
        self.rect.centerx = comprimento/2
        self.rect.bottom = altura - 5
        self.speedx = 0
        self.grupos = grupos
        self.recursos = recursos
        self.direcao = 1  #Começa olhando pra direita
    
    def update(self):
        self.rect.x += self.speedx
        # Não deixa o jogador sair da tela.
        if self.rect.right > comprimento:
            self.rect.right = comprimento

        if self.rect.left < 0:
            self.rect.left = 0

    def lancamento(self):
        if self.direcao == 1:
            novo_aviao = Aviao(self.recursos, self.rect.centery,  self.rect.right)
        else:
            novo_aviao = Aviao(self.recursos, self.rect.centery,  (self.rect.left-comprimento_letras))
        self.grupos['todos_elementos'].add(novo_aviao) 
        self.grupos['todos_avioes'].add(novo_aviao)
        self.recursos['lancamento_aviao'].play()
            
class Aviao(pygame.sprite.Sprite):
    def __init__(self, recursos, posicao_y, posicao_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = recursos['aviao_imagem']
        self.rect = self.image.get_rect()
        self.rect.y = posicao_y
        self.rect.x = posicao_x
        self.speedy = -5  
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()

class Movimento(pygame.sprite.Sprite):
    # Construtor da classe.
    def _init_(self, center, recursos):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite._init_(self)

        # Armazena a animação da corrida
        self.corrida = recursos['corrida']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.corrida[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        # Quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        agora = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = agora - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = agora

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.corrida):
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.corrida[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

todos_elementos = pygame.sprite.Group()
todas_letras = pygame.sprite.Group()
todos_avioes = pygame.sprite.Group()

grupos = {}
grupos['todos_elementos'] = todos_elementos
grupos['todas_letras'] = todas_letras
grupos['todos_avioes'] = todos_avioes

jogador = Aluno(recursos, grupos)
todos_elementos.add(jogador)

for a in range(4):
    letra_I = Letra(recursos['letra_I_imagem'])
    letra_D = Letra(recursos['letra_D_imagem'])
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
    letras = [recursos['letra_D_imagem'], recursos['letra_I_imagem']]
    for a in colisoes: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
        # O meteoro e destruido e precisa ser recriado
        random.shuffle(letras)
        imagem = Letra(letras[0])
        todos_elementos.add(imagem)
        todas_letras.add(imagem)
    if len(colisoes)>0:
        #game = False
        print('colidiu')
        recursos['hit_aluno'].play()

    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(recursos['background'], (-20, 0))

    todos_elementos.draw(window)

    #Atualiza jogo
    pygame.display.update()  

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
