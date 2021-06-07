import pygame
import os 
from constantes import *

def carrega_recurso():
    recursos = {}   #Cria dicionário recursos e armazena as imagens e os sons 
    recursos['background'] = pygame.image.load(os.path.join(IMG_DIR,'fachada_insper.jpg')).convert()
    recursos['background'] = pygame.transform.scale(recursos['background'], (comprimento_fundo, altura_fundo))
    recursos['letra_I_imagem'] = pygame.image.load(os.path.join(IMG_DIR,'letra_i.png')).convert_alpha()
    recursos['letra_D_imagem'] = pygame.image.load(os.path.join(IMG_DIR,'letra_d.png')).convert_alpha()
    recursos['letra_I_imagem'] = pygame.transform.scale(recursos['letra_I_imagem'], (comprimento_letras, altura_letras))
    recursos['letra_D_imagem'] = pygame.transform.scale(recursos['letra_D_imagem'], (comprimento_letras, altura_letras))
    recursos['aviao_imagem'] = pygame.image.load(os.path.join(IMG_DIR,'aviao.png')).convert_alpha()
    recursos['aviao_imagem'] = pygame.transform.scale(recursos['aviao_imagem'], (comprimento_aviao, altura_aviao))
    
    corridad = []
    corridae = []
    professor = []

    for i in range(1,11):
        #Armazena as imagens para a animação do jogador
        nome_arquivod = os.path.join(IMG_DIR,'mov{}-d.png'.format(i))
        nome_arquivoe = os.path.join(IMG_DIR,'mov{}-e.png'.format(i))
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
            nome_arquivo2 = os.path.join(IMG_DIR,'prof1.png')
            professor_imagem = pygame.image.load(nome_arquivo2).convert_alpha()
            professor_imagem = pygame.transform.scale(professor_imagem, (comprimento_professor, altura_professor))
            professor.append(professor_imagem)
        else:
            nome_arquivo2 = os.path.join(IMG_DIR,'prof2.png')
            professor_imagem = pygame.image.load(nome_arquivo2).convert_alpha()
            professor_imagem = pygame.transform.scale(professor_imagem, (comprimento_professor, altura_professor))
            professor.append(professor_imagem)
        i += 1
    recursos['professor_imagem'] = professor

    #Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR,'fundodojogo.mp3'))
    pygame.mixer.music.set_volume(0.2)
    recursos['hit_professor'] = pygame.mixer.Sound(os.path.join(SND_DIR,'atingeprof.wav'))
    recursos['lancamento_aviao'] = pygame.mixer.Sound(os.path.join(SND_DIR,'lançamento.wav'))
    recursos['hit_aluno'] = pygame.mixer.Sound(os.path.join(SND_DIR,'atingealuno.wav'))

    recursos["fonte_placar"] = pygame.font.Font(os.path.join(FNT_DIR,'PressStart2P.ttf'), 18)
    return recursos