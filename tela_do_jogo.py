import pygame 
from constantes import *
from recursos import *
from vilao import *
from jogador import *
from desenha import*

def tela_jogo(tela):
    clock = pygame.time.Clock() #Variável para ajuste da velocidade
    
    recurso = carrega_recurso()

    todos_elementos = pygame.sprite.Group()  #Criando grupo com todos os elementos do jogo
    todas_letras = pygame.sprite.Group()     #Criando grupo com as letras do jogo
    todos_avioes = pygame.sprite.Group()     #Criando grupo com os aviões do jogo
    todas_estrelas = pygame.sprite.Group()   #Criando grupo com as estrelas do jogo

    grupos = {}
    grupos['todos_elementos'] = todos_elementos
    grupos['todas_letras'] = todas_letras
    grupos['todos_avioes'] = todos_avioes
    grupos['todas_estrelas'] = todas_estrelas

    chefe = Professor(recurso, grupos) #Criando o professor
    todos_elementos.add(chefe)     
    jogador = Aluno(recurso, grupos)  #Criando o jogador
    todos_elementos.add(jogador)
    tempo_estrela = random.randint(1, 600)
    
    #Criando as letras
    for a in range(3):
        letra_I = Letra(recurso['letra_I_imagem'])
        letra_D = Letra(recurso['letra_D_imagem'])
        todos_elementos.add(letra_I)
        todos_elementos.add(letra_D)
        todas_letras.add(letra_I)
        todas_letras.add(letra_D)

    pygame.mixer.music.play(loops=-1) #Toca música de fundo
    #Cria variáveis de estado
    ACABOU = 5
    JOGANDO = 6
    COLIDINDO = 7
    estado = JOGANDO

    tecla_apertada = {}
    placar = 0
    vidas = 5
    vida_prof = 50

    tempo_ref = pygame.time.get_ticks()
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
                    if event.key in tecla_apertada:
                        if event.key == pygame.K_LEFT:
                            jogador.speedx += v
                        if event.key == pygame.K_RIGHT:
                            jogador.speedx -= v
        tempo_estrela -= 1
        if tempo_estrela == 0: #Quando chega a 0, ele cria a letra
            estrelas = Estrela(recurso, grupos)
            todos_elementos.add(estrelas)
            todas_estrelas.add(estrelas)

        #Atualiza a posição dos elementos do jogo
        todos_elementos.update()

        if estado == JOGANDO:
            colisao_est = pygame.sprite.spritecollide(jogador, todas_estrelas, True, pygame.sprite.collide_mask)
            if len(colisao_est) > 0:
                estrelas.kill()
                tempo_estrela = random.randint(1, 600)
                jogador.lancamento_aviao = 250
                tempo_ref = pygame.time.get_ticks()
            agora = pygame.time.get_ticks()
            duracao = agora - tempo_ref
            if duracao >= 3000:
                jogador.lancamento_aviao = 500
            #Verifica se houve colisão entre o avião e o professor
            colisao_avi = pygame.sprite.spritecollide(chefe, todos_avioes, True, pygame.sprite.collide_mask)
            if len(colisao_avi)>0:  #Se houver colisão, o professor perde vida e o aluno ganha pontos
                vida_prof -= 1
                recurso['hit_professor'].play()  #Som se o professor for atingido
                placar += 10
                estado = COLIDINDO
            #Verifica se houve colisão entre o jogador e as letras                
            colisoes = pygame.sprite.spritecollide(jogador, todas_letras, True, pygame.sprite.collide_mask)
            letras = [recurso['letra_D_imagem'], recurso['letra_I_imagem']]
            for a in colisoes: # As chaves são os elementos do primeiro grupo (jogador) que colidiram com alguma letra
                # A letra destruida precisa ser recriada
                random.shuffle(letras)
                imagem = Letra(letras[0])
                todos_elementos.add(imagem)
                todas_letras.add(imagem)
            if len(colisoes)>0:  #Se houver colisão, o aluno perde vida
                recurso['hit_aluno'].play()  #Som se o aluno for atingido
                jogador.kill()
                for s in todos_avioes.sprites():
                    s.kill()
                vidas -= 1
                estado = COLIDINDO
                tecla_apertada = {}
                if vidas > 0:
                    jogador = Aluno(recurso, grupos)
                    todos_elementos.add(jogador)
                else:
                    estado = ACABOU
        elif estado == COLIDINDO:
            if vidas == 0:  #Se acabarem as vidas o jogo acaba
                estado = ACABOU
            if vida_prof == 0:
                estado = ACABOU
            else:
                estado = JOGANDO

        tela.fill((0, 0, 0))  # Preenche com a cor branca
        tela.blit(recurso['background'], (-20, 0))
        todos_elementos.draw(tela)  #Desenha os elementos do jogo

        #Desenha o placar 
        texto_superficie = recurso['fonte_placar'].render("{:05d}".format(placar), True, (255, 255, 0))
        desenha_placar(texto_superficie,tela)

        #Desenha as vidas
        texto_superficie = recurso['fonte_placar'].render(chr(9829) * vidas, True, (255, 0, 0))
        desenha_vidas(texto_superficie,tela)
        
        pygame.display.update()  #Mostra o novo frame para o jogador
    if vidas == 0:
        estado = FINAL_RUIM
    if vida_prof == 0:
        estado = FINAL_BOM
    return estado