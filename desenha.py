import constantes

def desenha_placar(text,tela):
    text_rect = text.get_rect()
    text_rect.midtop = (50,  10)
    return tela.blit(text, text_rect)


def desenha_vidas(text,tela):
    text_rect = text.get_rect()
    text_rect.bottomleft = (10, constantes.altura - 10)
    return tela.blit(text, text_rect)