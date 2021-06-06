import pygame
import random
import time

pygame.init()

comprimento = 500
altura = 450
comprimento_fundo = 568
altura_fundo = 513
comprimento_letras = 40
altura_letras = 40            #537 x 1369 professor
posicao_x_letra = 225
posicao_y_letra = 0
comprimento_jogador = 80       # 595 x 742 jogador
altura_jogador = 100
comprimento_professor = 55
altura_professor = 137

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
professor = []

for i in range(1,11):
    nome_arquivo = 'imagens/mov{}.png'.format(i)
    jogador_imagem = pygame.image.load(nome_arquivo).convert_alpha()
    jogador_imagem = pygame.transform.scale(jogador_imagem, (comprimento_jogador, altura_jogador))
    corrida.append(jogador_imagem)
recursos['corrida'] = corrida
i = 0
while i < 8:
    if i <= 3:
        nome_arquivo2 = 'imagens/prof1.png'
        professor_imagem = pygame.image.load(nome_arquivo2).convert_alpha()
        professor_imagem = pygame.transform.scale(professor_imagem, (comprimento_professor, altura_professor))
        professor.append(professor_imagem)
    else:
        nome_arquivo2 = 'imagens/prof2.png'
        professor_imagem = pygame.image.load(nome_arquivo2).convert_alpha()
        professor_imagem = pygame.transform.scale(professor_imagem, (comprimento_professor, altura_professor))
        professor.append(professor_imagem)
    i += 1
recursos['professor_imagem'] = professor

class Letra(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = posicao_x_letra + comprimento_professor/2
        self.rect.y = posicao_y_letra + altura_professor/2
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

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
            self.speedy = random.randint(2, 9)

class Aluno(pygame.sprite.Sprite):
    def __init__(self, recursos, grupos):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.pos = 2
        self.image = recursos['corrida'][self.pos]
        self.rect = self.image.get_rect()
        self.rect.centerx = comprimento/2
        self.rect.bottom = altura - 5
        self.speedx = 0
        self.grupos = grupos
        self.recursos = recursos
        self.direcao = 1  #Começa olhando pra direita

        self.ultimo_tiro = pygame.time.get_ticks()
        self.lancamento_aviao = 500
    
    def update(self):
        self.rect.x += self.speedx
        # Não deixa o jogador sair da tela.
        if self.rect.right > comprimento:
            self.rect.right = comprimento

        if self.rect.left < 0:
            self.rect.left = 0
        if self.speedx > 0:
            self.pos = (self.pos+1)%len(self.recursos['corrida']) #faz as imagens formarem um loop
            self.image = self.recursos['corrida'][self.pos]

    def lancamento(self):
        agora  = pygame.time.get_ticks()

        colapso_aviao = agora -self.ultimo_tiro
        if colapso_aviao > self.lancamento_aviao:
            self.lancamento_aviao = agora
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

class Professor(pygame.sprite.Sprite):
    def __init__(self, recursos, grupos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = 0
        self.image = recursos['professor_imagem'][self.pos]   #537 x 1369 professor
        self.rect = self.image.get_rect()     # 595 x 742 jogador
        self.rect.centerx = comprimento/2
        self.rect.top = 5
        self.grupos = grupos
        self.recursos = recursos
    def update(self):
        self.pos = (self.pos+1)%len(self.recursos['professor_imagem']) #faz as imagens formarem um loop
        self.image = self.recursos['professor_imagem'][self.pos]



todos_elementos = pygame.sprite.Group()
todas_letras = pygame.sprite.Group()
todos_avioes = pygame.sprite.Group()

grupos = {}
grupos['todos_elementos'] = todos_elementos
grupos['todas_letras'] = todas_letras
grupos['todos_avioes'] = todos_avioes

chefe = Professor(recursos, grupos)
todos_elementos.add(chefe)
jogador = Aluno(recursos, grupos)
todos_elementos.add(jogador)

for a in range(3):
    letra_I = Letra(recursos['letra_I_imagem'])
    letra_D = Letra(recursos['letra_D_imagem'])
    todos_elementos.add(letra_I)
    todos_elementos.add(letra_D)
    todas_letras.add(letra_I)
    todas_letras.add(letra_D)

pygame.mixer.music.play(loops=-1)

ACABOU = 0
JOGANDO = 1
COLIDINDO = 2
estado = JOGANDO

clock = pygame.time.Clock() #Ajustando a velocidade
FPS = 30
v = 8

#Loop principal
while estado != ACABOU:
    clock.tick(FPS)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            estado = ACABOU
        if estado == JOGANDO:
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

    if estado == JOGANDO:
        colisao_avi = pygame.sprite.spritecollide(chefe, todos_avioes, True)
        if len(colisao_avi)>0:
            recursos['hit_professor'].play()
            
        colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True)
        letras = [recursos['letra_D_imagem'], recursos['letra_I_imagem']]
        for a in colisoes: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
            # O meteoro e destruido e precisa ser recriado
            random.shuffle(letras)
            imagem = Letra(letras[0])
            todos_elementos.add(imagem)
            todas_letras.add(imagem)
        if len(colisoes)>0:
            recursos['hit_aluno'].play()
            # jogador.kill()
            # estado = COLIDINDO
    elif estado == COLIDINDO:
        state = ACABOU

    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(recursos['background'], (-20, 0))

    todos_elementos.draw(window)

    #Atualiza jogo
    pygame.display.update()  

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
