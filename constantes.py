from os import path
#Contém as figuras e sons do jogo
IMG_DIR = path.join(path.dirname(__file__), 'recursos', 'imagens')
SND_DIR = path.join(path.dirname(__file__), 'recursos', 'sons')
FNT_DIR = path.join(path.dirname(__file__), 'recursos', 'fonte')

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
comprimento_tela = 450
altura_tela = 450
comprimento_estrela = 34
altura_estrela = 33

#Cor preta
BLACK = (0,0,0)
#Estado para controle do fluxo de aplicação
INIT = 0
GAME = 1
FINAL_BOM = 2
FINAL_RUIM = 3
QUIT = 4
