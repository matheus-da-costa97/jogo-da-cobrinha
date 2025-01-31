import pygame
from pygame.locals import *
from sys import exit 
from random import randint

#configurações gerais
LARGURA = 600
ALTURA = 450
TAMANHO_COBRA = 20
RAIO = 5
X_COBRA = (LARGURA // 2) - (TAMANHO_COBRA // 2)
Y_COBRA = (ALTURA // 2) - (TAMANHO_COBRA // 2)
VELOCIDADE = 10
X_CONTROLE = VELOCIDADE
Y_CONTROLE = 0

#cores
COR_COBRA = (255,255,0)
COR_FRUTA = (255,0,0)
COR_TELA = (0,100,150)
COR_TEXTO = (255,255,255)


class Cobra:
    def __init__(self):
        self.x = X_COBRA
        self.y = Y_COBRA
        self.corpo = []
        self.x_controle = X_CONTROLE
        self.y_controle = Y_CONTROLE
        self.pontos = 0
        self.comprimento = 5
        self.velocidade = 15
        
    def desenhar_cobra(self, tela):
        pygame.draw.rect(tela, COR_COBRA, (self.x, self.y, TAMANHO_COBRA, TAMANHO_COBRA))
        
    def mover(self):
        self.x += self.x_controle
        self.y += self.y_controle
        
    def aumentar(self, tela):
        cabeça = []
        cabeça.append(self.x)
        cabeça.append(self.y)
        self.corpo.append(cabeça)
        
        if len(self.corpo) > self.comprimento:
            del(self.corpo[0])
            
        for segmento in self.corpo:
            pygame.draw.rect(tela, COR_COBRA, (segmento[0], segmento[1], TAMANHO_COBRA, TAMANHO_COBRA))
    
    def verificar_colisao_corpo(self):
        return self.corpo.count([self.x, self.y]) > 1
    def verificar_colisao_borda(self):
        return self.x < 0 or self.x + TAMANHO_COBRA > LARGURA or self.y < 0 or self.y + TAMANHO_COBRA > ALTURA

class Fruta:
    def __init__(self):
        self.raio = RAIO
        self.x = randint(RAIO + 5, (LARGURA - RAIO))
        self.y = randint(RAIO + 5, (ALTURA - RAIO))
        
    def desenhar_fruta(self, tela):
        pygame.draw.circle(tela, COR_FRUTA, (self.x, self.y), RAIO)
        
    def reposicionar(self):
        self.x = randint(RAIO, (LARGURA - RAIO))
        self.y = randint(RAIO, (ALTURA - RAIO))
        
def reiniciar_jogo(cobra, fruta):
    global VELOCIDADE
    
    cobra.__init__()
    fruta.__init__()
    VELOCIDADE = 12
        
pygame.init()
# inicialização
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 20, True)

cobra = Cobra()
fruta = Fruta()

while True:
    clock.tick(VELOCIDADE)
    tela.fill(COR_TELA)
    mensagem = f"pontos: {cobra.pontos}"
    texto = fonte.render(mensagem, True, COR_TEXTO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and cobra.x_controle != -VELOCIDADE:
                cobra.x_controle = VELOCIDADE
                cobra.y_controle = 0
            if event.key == K_LEFT and cobra.x_controle != VELOCIDADE:
                cobra.x_controle = -VELOCIDADE
                cobra.y_controle = 0
            if event.key == K_UP and cobra.y_controle != VELOCIDADE:
                cobra.x_controle = 0
                cobra.y_controle = -VELOCIDADE
            if event.key == K_DOWN and cobra.y_controle != -VELOCIDADE:
                cobra.x_controle = 0
                cobra.y_controle = VELOCIDADE
    
    cobra.mover()
    cobra.aumentar(tela)
    
    #colisão com a fruta:
    cobra_rect = pygame.Rect(cobra.x, cobra.y, TAMANHO_COBRA, TAMANHO_COBRA)
    fruta_rect = pygame.Rect(fruta.x, fruta.y, RAIO*2, RAIO*2)
    
    if cobra_rect.colliderect(fruta_rect):
        fruta.reposicionar()
        cobra.comprimento += 1
        cobra.pontos += 1
        VELOCIDADE += 0.5
        
    #colisao com o proprio corpo
    if cobra.verificar_colisao_corpo() or cobra.verificar_colisao_borda():
        game_over = "GAME OVER. Pressione r para continuar"
        texto2 = fonte.render(game_over, True, (255,0,0))
        texto2_center = texto2.get_rect(center=(LARGURA // 2, ALTURA // 2))
        morreu = True
        
        while morreu:
            pygame.time.wait(1000)
            tela.fill((0,0,0))
            tela.blit(texto2, texto2_center)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    reiniciar_jogo(cobra, fruta)
                    morreu = False
                    
    cobra.desenhar_cobra(tela)
    fruta.desenhar_fruta(tela)
        
    tela.blit(texto, (400, 20))
    pygame.display.update()