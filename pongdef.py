import pyxel 
from time import sleep

#constantes (geralmente declaradas em MAIUSCULO)
RAIO = 2
ALTURA = 12 #DA PÁ
LARGURA = 2 #DA PÁ
P1_X = 3
P2_X = 120 - 3
FPS = 30
dt = 1/FPS
#variaveis que descrevem o estado do game
x, y = 116 / 2, 80 / 2 #posiçao da bola
vx, vy = 33, 33 
p1_y = 80/ 2 #altura do player
p2_y = 80 / 2
p1_pontos = 0
p2_pontos = 0
pausado_f = True
pausado_m = True
pausado_d = True
comecar = True
facil = False
medio = False
dificil = False

#===================================================================
# Lógica do game
#===================================================================
def update():
    global p1_y, p2_y, x, y, vx, vy, pausado_f, pausado_m, pausado_d, p1_pontos, p2_pontos, comecar, facil, dificil, medio

    #JOGABILIDADE NAS DIFICULDADES
    if facil:
        x = x + vx * dt
        y = y + vy * dt
        #colisaooooo
        ##NA MARGEM
        if y <= RAIO + 1 or y >= 80 - (RAIO + 1): 
            vy *= -1

        ##NO JOGADOR
        vx_mul = 1.0
        if x <= P1_X + LARGURA / 2  + RAIO and  abs(y - p1_y) < RAIO + ALTURA / 2: 
            vx_mul = -1
        if  x >= P2_X - LARGURA / 2 - RAIO and  abs(y - p2_y) < RAIO + ALTURA / 2:
            vx_mul = -1
        
        vx *= vx_mul
        comecar = False
        
    if medio:
        x = x + 1.5 * vx * dt #aumentar a velocidade da bolinha
        y = y + 1.5 * vy * dt #aumentar a velocidade da bolinha
        #colisaooooo
        ##NA MARGEM
        if y <= RAIO + 1 or y >= 80 - (RAIO + 1): 
            vy *= -1

        ##NO JOGADOR
        vx_mul = 1.0
        if x <= P1_X + LARGURA / 2  + RAIO and  abs(y - p1_y) < RAIO + ALTURA / 2: 
            vx_mul = -1
        if  x >= P2_X - LARGURA / 2 - RAIO and  abs(y - p2_y) < RAIO + ALTURA / 2:
            vx_mul = -1
        
        vx *= vx_mul
        comecar = False

    if dificil:
        x = x + 1.5 * vx * dt #aumentar a velocidade da bolinha
        y = y + 1.5 * vy * dt #aumentar a velocidade da bolinha

        #colisaooo
        ##NA MARGEM
        if y <= RAIO + 1 or y >= 80 - (RAIO + 1): 
            vy *= -1

        ##NO JOGADOR
        vx_mul = 1.0
        if x <= P1_X + LARGURA / 2  + RAIO and  abs(y - p1_y) < RAIO + ALTURA / 2: 
            vx_mul = -1.2 #ACELERAR A BOLINHA DPS DE BATER NO JOGADOR
        if  x >= P2_X - LARGURA / 2 - RAIO and  abs(y - p2_y) < RAIO + ALTURA / 2:
            vx_mul = -1.2 #ACELERAR A BOLINHA DPS DE BATER NO JOGADOR
        
        vx *= vx_mul
        comecar = False

    #selecionar a dificuldade
    if comecar:
        pausado_f,pausado_m, pausado_d = False, False, False #para nao ficar o texto do pause aparecendo

    if comecar and pyxel.btnp(pyxel.KEY_F): #apertar F para escolher o  modo facil
        facil = True

    if comecar and pyxel.btnp(pyxel.KEY_N): #escolhi o N pq o M parecia um H
        medio = True
  
    if comecar and pyxel.btnp(pyxel.KEY_D): #apertar D para escolher o  modo dificil
        dificil = True
        
    #pause no facil
    if pausado_f and facil:
        facil = False
    elif pausado_f and pyxel.btnp(pyxel.KEY_SPACE): #sair do pause apertando espaço
        pausado_f = False 
        facil = True

    #pause no medio
    if pausado_m and medio:
        medio = False
    elif pausado_m and pyxel.btnp(pyxel.KEY_SPACE): #sair do pause apertando espaço
        pausado_m = False 
        medio = True

    #pause no dificil
    if pausado_d and dificil:
       dificil = False
    elif pausado_d and pyxel.btnp(pyxel.KEY_SPACE): #sair do pause apertando espaço
        pausado_d = False
        dificil = True
    
    # mexe os jogadores
    p1_y = move_jogador(p1_y, pyxel.KEY_S, pyxel.KEY_W)
    p2_y = move_jogador(p2_y, pyxel.KEY_DOWN, pyxel.KEY_UP)

    

    #Verifica se p1 perdeu
    if x < 0: #passou da borda lateral esquerda
        p2_pontos += 1
        sleep(0.2) #dar um tempinho para a animaçao do jogo voltar
        x, y = 120/2, 80/2 #reiniciar a bola
        p1_y, p2_y = 80/ 2, 80/2 #reiniciar a altura do player

        #quando perder, voltar o jogo pausado na dificuldade escolhida antes
        if facil:
            pausado_f = True 
        if medio:
            pausado_m = True
        if dificil:
            vx = 33 # reiniciar a velocidade da bolinha 
            pausado_d = True
            
    

    #Verifica se p2 perdeu    
    if x > 120: #passou da borda lateral direita
        p1_pontos += 1
        sleep(0.2) #dar um tempinho para a animaçao do jogo voltar
        x, y = 120/2, 80/2 #reiniciar a bola
        p1_y, p2_y = 80/ 2, 80/2 #reiniciar a altura do player

        #quando perder, voltar o jogo pausado na dificuldade escolhida antes
        if facil:
            pausado_f = True 
        if medio:
            pausado_m = True
        if dificil:
            vx = 33 #reiniciar a velocidade da bolinha
            pausado_d = True
            
    
     
        



def move_jogador(y, cima, baixo):
    if pyxel.btn(cima): 
        y += 1
    elif pyxel.btn(baixo):
        y -= 1
    y = max(y, ALTURA/2 - 4) # travar na margem de cima
    y = min(y, 80 - ALTURA / 2 - 5) #travar na margem de baixo
    return y





#===================================================================
# Desenha elementos na tela
#===================================================================
def draw():
    pyxel.cls(pyxel.COLOR_NAVY) #cor do fundo

    #desenhar o texto das dificuldades
    if comecar:
        pyxel.text(20, 16, "Escolha a Dificuldade", pyxel.COLOR_WHITE)
        pyxel.text(28, 34,"Facil->  aperte F", pyxel.COLOR_YELLOW)     #cada letra ocupa dois espaços
        pyxel.text(28, 42,"Normal-> aperte N", pyxel.COLOR_YELLOW)     #escolhi o N pq o M parecia um H
        pyxel.text(26, 50,"Dificil-> aperte D", pyxel.COLOR_YELLOW)    #cada letra ocupa dois espaços


    #desenha os elementos do jogo
    desenha_jogador(P1_X, p1_y, p1_pontos, "esquerda")
    desenha_jogador(P2_X, p2_y, p2_pontos, "direita")
    pyxel.circ(x, y, RAIO, pyxel.COLOR_RED) #bola

    #FAZER A MARGEM
    pyxel.line(0, 0, 120, 0, pyxel.COLOR_LIGHTBLUE) 
    pyxel.line(0, 79, 120, 79, pyxel.COLOR_LIGHTBLUE)

    #Aparecer o texto quando o jogo tiver pausado
    if pausado_f:
        pyxel.text(34, 36,"Aperte espaco\npara continuar!", pyxel.COLOR_YELLOW)
    if pausado_m:
        pyxel.text(34, 36,"Aperte espaco\npara continuar!", pyxel.COLOR_YELLOW)
    if pausado_d:
        pyxel.text(34, 36,"Aperte espaco\npara continuar!", pyxel.COLOR_YELLOW)
    
    

def desenha_jogador(pos_x, pos_y, pontos, alinhamento): #posiçao do centro
    x = pos_x - LARGURA / 2 #posiçao no lado esquerdo
    y = pos_y - LARGURA / 2

    pyxel.rect(x, y, LARGURA, ALTURA, pyxel.COLOR_CYAN) #rect = retangulo

    #desenha o placar
    txt = str(pontos)
    x = pos_x
    y = 3
    if alinhamento == "direita":
        x -= len(txt) * pyxel.FONT_WIDTH   #tamanho do texto menos a largura de cada letra
    pyxel.text(x, y, txt, pyxel.COLOR_WHITE)

    


#===================================================================
# Inicializar o pyxel
#===================================================================
pyxel.init(120,80, caption="PONG do LOPAO", fps=FPS)  #resolução da tela e nome do jogo
pyxel.mouse(True) #aparecer o mouse(tem q vir depois do init)
pyxel.run(update, draw)

