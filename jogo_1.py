import pygame
import random
import time

pygame.init()

# ------Declara variáveis
FPS = 30
v = 8
comprimento = 500
altura = 450
comprimento_fundo = 568
altura_fundo = 513
comprimento_letras = 40
altura_letras = 40            
posicao_x_letra = 225
posicao_y_letra = 0
comprimento_jogador = 80       
altura_jogador = 100
comprimento_professor = 55
altura_professor = 137
comprimento_aviao = 30
altura_aviao = 45

# ----Gera tela principal
window = pygame.display.set_mode((comprimento, altura))
pygame.display.set_caption('Diploma Battle')
def carrega_recurso():
    recursos = {}   #Cria dicionário recursos e armazena as imagens e os sons 
    recursos['background'] = pygame.image.load('imagens/fachada_insper.jpg').convert()
    recursos['background'] = pygame.transform.scale(recursos['background'], (comprimento_fundo, altura_fundo))
    recursos['letra_I_imagem'] = pygame.image.load('imagens/letra_i.png').convert_alpha()
    recursos['letra_D_imagem'] = pygame.image.load('imagens/letra_d.png').convert_alpha()
    recursos['letra_I_imagem'] = pygame.transform.scale(recursos['letra_I_imagem'], (comprimento_letras, altura_letras))
    recursos['letra_D_imagem'] = pygame.transform.scale(recursos['letra_D_imagem'], (comprimento_letras, altura_letras))
    recursos['aviao_imagem'] = pygame.image.load('imagens/aviao.png').convert_alpha()
    recursos['aviao_imagem'] = pygame.transform.scale(recursos['aviao_imagem'], (comprimento_aviao, altura_aviao))
    
    corridad = []
    corridae = []
    professor = []

    for i in range(1,11):
        #Armazena as imagens para a animação do jogador
        nome_arquivod = 'imagens/mov{}-d.png'.format(i)
        nome_arquivoe = 'imagens/mov{}-e.png'.format(i)
        jogador_imagemd = pygame.image.load(nome_arquivod).convert_alpha()
        jogador_imagemd = pygame.transform.scale(jogador_imagemd, (comprimento_jogador, altura_jogador))
        jogador_imageme = pygame.image.load(nome_arquivoe).convert_alpha()
        jogador_imageme = pygame.transform.scale(jogador_imageme, (comprimento_jogador, altura_jogador))
        corridad.append(jogador_imagemd)
        corridae.append(jogador_imageme)
    recursos['corridad'] = corridad
    recursos['corridae'] = corridae

    i = 0
    while i < 8:
        #Armazena as imagens para a animação do professor
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

    #Carrega os sons do jogo
    pygame.mixer.music.load('sons/fundodojogo.mp3')
    pygame.mixer.music.set_volume(0.2)
    recursos['hit_professor'] = pygame.mixer.Sound('sons/atingeprof.wav')
    recursos['lancamento_aviao'] = pygame.mixer.Sound('sons/lançamento.wav')
    recursos['hit_aluno'] = pygame.mixer.Sound('sons/atingealuno.wav')

    recursos["fonte_placar"] = pygame.font.Font('fonte/PressStart2P.ttf', 18)
    return recursos

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
            self.speedy = random.randint(2, 9)

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
        colapso_aviao = agora -self.ultimo_tiro

        #Se já pode lançar novamente...
        if colapso_aviao > self.lancamento_aviao:
            #Marca o tick da nova imagem
            self.lancamento_aviao = agora
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
def tela_jogo(window):
    clock = pygame.time.Clock() #Variável para ajuste da velocidade
    
    recursos = carrega_recurso()

    todos_elementos = pygame.sprite.Group()  #Criando grupo com todos os elementos do jogo
    todas_letras = pygame.sprite.Group()     #Criando grupo com as letras do jogo
    todos_avioes = pygame.sprite.Group()     #Criando grupo com os aviões do jogo

    grupos = {}
    grupos['todos_elementos'] = todos_elementos
    grupos['todas_letras'] = todas_letras
    grupos['todos_avioes'] = todos_avioes

    chefe = Professor(recursos, grupos) #Criando o professor
    todos_elementos.add(chefe)     
    jogador = Aluno(recursos, grupos)  #Criando o jogador
    todos_elementos.add(jogador)
    #Criando as letras
    for a in range(3):
        letra_I = Letra(recursos['letra_I_imagem'])
        letra_D = Letra(recursos['letra_D_imagem'])
        todos_elementos.add(letra_I)
        todos_elementos.add(letra_D)
        todas_letras.add(letra_I)
        todas_letras.add(letra_D)

    pygame.mixer.music.play(loops=-1)
    #Cria variáveis de estado
    ACABOU = 0
    JOGANDO = 1
    COLIDINDO = 2
    estado = JOGANDO

    tecla_apertada = {}
    placar = 0
    vidas = 5
    vida_prof = 30

    #Loop principal
    while estado != ACABOU:
        clock.tick(FPS)

        #Trata evento
        for event in pygame.event.get():
            #Verifica consequências
            if event.type == pygame.QUIT:
                estado = ACABOU
            #Só verifica teclado se ainda está no estado jogando
            if estado == JOGANDO:
                if event.type == pygame.KEYDOWN:
                    #Dependendo da tecla, altera a velocidade
                    tecla_apertada[event.key] = True
                    if event.key == pygame.K_LEFT:
                        jogador.speedx -= v
                        jogador.direcao = 0   #Vira o jogador para a esquerda
                    if event.key == pygame.K_RIGHT:
                        jogador.speedx += v
                        jogador.direcao = 1  #Vira o jogador para a direita
                    if event.key == pygame.K_SPACE:
                        jogador.lancamento()
                #Verifica se soltou alguma tecla
                if event.type == pygame.KEYUP:
                    #Dependendo da tecla, altera a velocidade
                    if event.key in tecla_apertada and tecla_apertada[event.key]:
                        if event.key == pygame.K_LEFT:
                            jogador.speedx += v
                        if event.key == pygame.K_RIGHT:
                            jogador.speedx -= v

        #Atualiza a posição dos elementos do jogo
        todos_elementos.update()

        
        if estado == JOGANDO:
            #Verifica se houve colisão entre o avião e o professor
            colisao_avi = pygame.sprite.spritecollide(chefe, todos_avioes, True, pygame.sprite.collide_mask)
            if len(colisao_avi)>0:  #Se houver colisão, o professor perde vida e o aluno ganha pontos
                vida_prof -= 1
                recursos['hit_professor'].play()  #Som se o professor for atingido
                placar += 10
            #Verifica se houve colisão entre o jogador e as letras                
            colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True, pygame.sprite.collide_mask)
            letras = [recursos['letra_D_imagem'], recursos['letra_I_imagem']]
            for a in colisoes: # As chaves são os elementos do primeiro grupo (jogador) que colidiram com alguma letra
                # A letra destruida precisa ser recriada
                random.shuffle(letras)
                imagem = Letra(letras[0])
                todos_elementos.add(imagem)
                todas_letras.add(imagem)

            if len(colisoes)>0:  #Se houver colisão, o aluno perde vida
                recursos['hit_aluno'].play()  #Som se o aluno for atingido
                jogador.kill()
                vidas -= 1
                estado = COLIDINDO
                tecla_apertada = {}
        elif estado == COLIDINDO:
            if vidas == 0:  #Se acabarem as vidas o jogo acaba
                estado = ACABOU
            else:
                estado = JOGANDO
                jogador = Aluno(recursos, grupos)
                todos_elementos.add(jogador)
    
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(recursos['background'], (-20, 0))
        todos_elementos.draw(window)  #Desenha os elementos do jogo

        #Desenha o placar 
        texto_superficie = recursos['fonte_placar'].render("{:05d}".format(placar), True, (255, 255, 0))
        text_rect = texto_superficie.get_rect()
        text_rect.midtop = (50,  10)
        window.blit(texto_superficie, text_rect)

        #Desenha as vidas
        texto_superficie = recursos['fonte_placar'].render(chr(9829) * vidas, True, (255, 0, 0))
        text_rect = texto_superficie.get_rect()
        text_rect.bottomleft = (10, altura - 10)
        window.blit(texto_superficie, text_rect)
        
        pygame.display.update()  #Mostra o novo frame para o jogador

tela_jogo(window)  #Inicia a tela do jogo?

pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
