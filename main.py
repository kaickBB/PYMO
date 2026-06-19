"""
╔════════════════════╗
║  Projeto PYMO©!!!  ║
╚════════════════════╝

"""
#auto-py-to-exe utilizadao para poder converter para exe


#----Importando e iniciando Módulos----
import pygame
import random
import os
import sys

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funcionando no PyInstaller """
    try:
        # Quando rodando como executável, o PyInstaller extrai para a pasta _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Quando rodando via script .py normal, usa a pasta atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()


#----Configuaração de janela base (resolução de referência do layout original)----
BASE_LARGURA, BASE_ALTURA = 600, 750

#----Janela inicia redimensionável para o botão maximizar do Windows funcionar----
tela = pygame.display.set_mode((BASE_LARGURA, BASE_ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Pymo©")

# ----Upload de imagens----
lampadaApagada = pygame.image.load(resource_path("pic/lamp.png"))
lampadaAcessa  = pygame.image.load(resource_path("pic/lampHover.png"))
send           = pygame.image.load(resource_path("pic/send.png"))
sendHover      = pygame.image.load(resource_path("pic/sendHover.png"))
delete         = pygame.image.load(resource_path("pic/delete.png"))
deleteHover    = pygame.image.load(resource_path("pic/deleteHover.png"))

# ----Paleta de Cores----
CORLETRAS  = (230, 230, 230)
CORBOX     = (131, 129, 170)
CORVERDE   = (83,  182, 105)
CORERRADA  = (70,  70,  85 )
CORAMARELO = (230, 185, 90 )
CORPLAYAGAIN       = (90,  130, 215)
CORTECLA           = (137, 147, 167)
CORBORDA           = (255, 255, 255)
CORTECLAHOVER      = (150, 180, 240)
#----cores novas para botões especiais e degradê----
CORENVIAR          = (72,  160, 110)
CORENVIARHOVER     = (95,  200, 135)
CORAPAGAR          = (180, 80,  90 )
CORAPAGARHOVER     = (215, 105, 115)
CORTECLAESPECIALTEXTO = (240, 240, 240)

#----Dicionário de palavras e dicks----
PALAVRAS = {
    "false":    "Tudo parece verdadeiro, porem eu não sou tudo",
    "none":     "Sou nada, mas indico o vazio.",
    "true":     "Sou o oposto de mentira.",
    "and":      "Precisa de duas condições? Eu sou o cara!",
    "as":       "Dou outro nome, como um apelido.",
    "break":    "Interrompo o fluxo.",
    "class":    "Sou o modelo para criar algo novo.",
    "continue": "Pulo para a próxima rodada.",
    "def":      "Define blocos de código a serem chamados.",
    "del":      "Apago o que não serve mais.",
    "elif":     "Sou o 'senão, se', a segunda chance.",
    "else":     "Sou a opção quando tudo falha.",
    "except":   "Lido com erros quando algo dá errado.",
    "finally":  "Garante que algo sempre será feito.",
    "for":      "Guio de item em item até o fim.",
    "from":     "Trago algo de fora para perto.",
    "global":   "Escapo das funções, sendo acessível.",
    "if":       "Me questiono: 'Isso é verdadeiro ou não?'",
    "import":   "Sou a porta para o que é externo.",
    "in":       "Verifico se algo está dentro de algo.",
    "is":       "Pergunto: 'Isso é realmente isso?'",
    "nonlocal": "Busco algo mais acima, mas não sou global.",
}

#----Não presica nem de titulo----
TECLAS = [
    list("qwertyuiop"),
    list("asdfghjkl"),
    list("zxcvbnm")
]

#----Função que cria e reseta todas as variáveis globais----
def variaveisDeJogo():
    global palavra, dica, tentativas, atentativa, mtentativas, showDica, vitoria, derrota, numRodada
    palavra     = random.choice(list(PALAVRAS.keys()))
    dica        = PALAVRAS[palavra]
    tentativas  = []
    atentativa  = ""
    mtentativas = 4
    showDica    = False
    vitoria     = False
    derrota     = False
    numRodada  += 1


#----Retorna o fator de escala atual com base no tamanho real da janela----
def escala():
    W, H = tela.get_size()
    return min(W / BASE_LARGURA, H / BASE_ALTURA)

#----Converte uma medida do layout base para o tamanho escalado----
def s(valor):
    return int(valor * escala())

#----Converte coordenada X do layout base para a tela real (com margem centralizada)----
def tx(x):
    W = tela.get_width()
    margem = (W - s(BASE_LARGURA)) // 2
    return margem + s(x)

#----Converte coordenada Y do layout base para a tela real (com margem centralizada)----
def ty(y):
    H = tela.get_height()
    margem = (H - s(BASE_ALTURA)) // 2
    return margem + s(y)

#----Cache de fontes para evitar recriar a cada frame----
_cache_fontes = {}
def fonte(tamanhoBase, bold=False):
    e = escala()
    chave = (tamanhoBase, bold, round(e, 2))
    if chave not in _cache_fontes:
        _cache_fontes[chave] = pygame.font.SysFont("Arial", max(8, s(tamanhoBase)), bold=bold)
    return _cache_fontes[chave]

#----Função que gera a superfície do degradê azul→magenta para o fundo----
def gerarDegradeFundo(largura, altura):
    surf    = pygame.Surface((largura, altura))
    corTopo = (30, 30, 100)
    corBase = (130, 30, 120)
    for y in range(altura):
        t = y / max(altura - 1, 1)
        r = int(corTopo[0] + (corBase[0] - corTopo[0]) * t)
        g = int(corTopo[1] + (corBase[1] - corTopo[1]) * t)
        b = int(corTopo[2] + (corBase[2] - corTopo[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (largura, y))
    return surf

#----Função que desenha textos de acordo com os parâmetros recebidos----
def escreverTexto(texto, tamanhoFonte, cor, bx, by, bold=False):
    f   = fonte(tamanhoFonte, bold)
    txt = f.render(texto, True, cor)
    base = txt.get_rect(center=(tx(bx), ty(by)))
    tela.blit(txt, base)

#----funçao que desenha a imagem do botão de dica (escalonada)----
def botaoDica(posicaoMouse):
    tam  = s(40)
    rect = pygame.Rect(tx(550), ty(10), tam, tam)
    img  = lampadaAcessa if rect.collidepoint(posicaoMouse) or showDica else lampadaApagada
    tela.blit(pygame.transform.scale(img, (tam, tam)), rect.topleft)
    return rect

#----função que desenha o retangulo com a dica----
def escreverDica():
    if showDica:
        rw = s(BASE_LARGURA - 40)
        rh = s(60)
        pygame.draw.rect(tela, (40, 40, 60), (tx(20), ty(410), rw, rh), border_radius=s(10))
        escreverTexto(f"Dica: {dica}", 20, CORLETRAS, BASE_LARGURA // 2, 440)

#----função que desenha na tela os quadros com uma tentativa e os quadros vazios sem nenhuma tentativa----
def desenharQuadros():
    tam = s(50)
    passo = s(60)
    for i in range(mtentativas):
        tentativa = tentativas[i] if i < len(tentativas) else ""
        for L in range(len(palavra)):
            x = tx(50 + L * 60)
            y = ty(170 + i * 60)
            letra = tentativa[L] if L < len(tentativa) else ""                                                                                        #toFicandoMaliuko
            cor   = CORBOX
            if i < len(tentativas):
                if letra == palavra[L]:
                    cor = CORVERDE
                elif letra in palavra:
                    cor = CORAMARELO
                else:
                    cor = CORERRADA
            pygame.draw.rect(tela, cor, (x, y, tam, tam), border_radius=s(8))
            if letra:
                f   = fonte(36, bold=True)
                txt = f.render(letra.upper(), True, CORLETRAS)
                tela.blit(txt, txt.get_rect(center=(x + tam // 2, y + tam // 2)))
    #----Aqui calcula a largura e posição x e y dos quadrados onde mostra oque ojogador está digitando agora----
    if len(tentativas) < mtentativas:
        larguraTotal  = len(palavra) * 60 - 10
        posicaoInicialX = (BASE_LARGURA - larguraTotal) // 2
        by = 230 + mtentativas * 60 + 10
    #----Agora vai imprimir os quadrados que indicam oque o jogador está digitando agora em tempo real dfoknaff----
        for L in range(len(palavra)):
            x = tx(posicaoInicialX + L * 60)
            y = ty(by)
            corBorda = CORBORDA if L == len(atentativa) else CORBOX
            pygame.draw.rect(tela, CORBOX,    (x, y, tam, tam), border_radius=s(8))                             #SOCORRROOO
            pygame.draw.rect(tela, corBorda,  (x, y, tam, tam), max(1, s(3)), border_radius=s(8))
            if L < len(atentativa):
                f   = fonte(36, bold=True)
                txt = f.render(atentativa[L].upper(), True, CORLETRAS)
                tela.blit(txt, txt.get_rect(center=(x + tam // 2, y + tam // 2)))

#----Função responsável por imprimir na tela o teclado virtual----
#----Inclui os botões de Enviar (Enter) e Apagar (Backspace) ao lado da última linha----
def printTeclado():
    largura = s(45)
    altura  = s(45)
    vao     = s(5)
    mousex, mousey = pygame.mouse.get_pos()

    for i, linha in enumerate(TECLAS):
        larguraLinhaTeclas = len(linha) * largura + (len(linha) - 1) * vao
        centralizacao = (tela.get_width() - larguraLinhaTeclas) // 2
        for j, tecla in enumerate(linha):
            x = centralizacao + j * (largura + vao)
            y = ty(550) + i * (altura + vao)
            cor = CORTECLAHOVER if x <= mousex <= x + largura and y <= mousey <= y + altura else CORTECLA
            pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=s(8))
            f   = fonte(24)
            txt = f.render(tecla, True, CORLETRAS)
            tela.blit(txt, txt.get_rect(center=(x + largura // 2, y + altura // 2)))

    #----Botões Apagar e Enviar ao lado da última linha do teclado----
    botaoTamanho   = int(altura * 1.2)  # 20% maior que as teclas, e quadrado
    yBotaoExtra    = ty(550) + 2 * (altura + vao)  # Mesma altura da última linha (índice 2)
    larguraLinhaTeclas = len(TECLAS[2]) * largura + (len(TECLAS[2]) - 1) * vao
    centralizacao = (tela.get_width() - larguraLinhaTeclas) // 2
    
    # Botão Apagar à esquerda
    xApagar = centralizacao - botaoTamanho - s(10)
    hoverApagar = xApagar <= mousex <= xApagar + botaoTamanho and yBotaoExtra <= mousey <= yBotaoExtra + botaoTamanho
    imgApagar = deleteHover if hoverApagar else delete
    imgApagarEscalada = pygame.transform.scale(imgApagar, (botaoTamanho, botaoTamanho))
    tela.blit(imgApagarEscalada, (xApagar, yBotaoExtra))

    # Botão Enviar à direita
    xEnviar = centralizacao + larguraLinhaTeclas + s(10)
    hoverEnviar = xEnviar <= mousex <= xEnviar + botaoTamanho and yBotaoExtra <= mousey <= yBotaoExtra + botaoTamanho
    imgEnviar = sendHover if hoverEnviar else send
    imgEnviarEscalada = pygame.transform.scale(imgEnviar, (botaoTamanho, botaoTamanho))
    tela.blit(imgEnviarEscalada, (xEnviar, yBotaoExtra))

#----Função que verifica qual tecla o jogador clicou com o mouse----
#----Agora também detecta clique nos botões Enviar e Apagar ao lado da última linha----
def clickTecla(pos):
    largura = s(36)
    altura  = s(45)
    vao     = s(5)
    for i, linha in enumerate(TECLAS):
        larguraTotal = len(linha) * largura + (len(linha) - 1) * vao
        inicioX = (tela.get_width() - larguraTotal) // 2
        for j, tecla in enumerate(linha):
            x = inicioX + j * (largura + vao)
            y = ty(550) + i * (altura + vao)
            if x <= pos[0] <= x + largura and y <= pos[1] <= y + altura:
                return tecla.lower()

    #----Verificação dos botões especiais Apagar e Enviar ao lado da última linha----
    altura = s(45)
    botaoTamanho = int(altura * 1.2)  # 20% maior que as teclas, e quadrado
    larguraLinhaTeclas = len(TECLAS[2]) * largura + (len(TECLAS[2]) - 1) * vao
    centralizacao = (tela.get_width() - larguraLinhaTeclas) // 2
    yBotaoExtra  = ty(550) + 2 * (altura + vao)
    xApagar      = centralizacao - botaoTamanho - s(10)
    xEnviar      = centralizacao + larguraLinhaTeclas + s(10)
    
    if xApagar <= pos[0] <= xApagar + botaoTamanho and yBotaoExtra <= pos[1] <= yBotaoExtra + botaoTamanho:
        return "__apagar__"
    if xEnviar <= pos[0] <= xEnviar + botaoTamanho and yBotaoExtra <= pos[1] <= yBotaoExtra + botaoTamanho:
        return "__enviar__"

#----função que Processa a tentativa atual(atentativa)-----
def verificarTentativa():
    global atentativa, vitoria, derrota
    tentativas.append(atentativa)
    if atentativa == palavra:
        vitoria = True
    elif len(tentativas) >= mtentativas:
        derrota = True
    atentativa = ""

#----Função que mostra uma mensagem na tela quando o jogo termina----
def desenhar_mensagem_final():
    if vitoria:
        mensagem, cor = f"Acertou ({len(tentativas)}/{mtentativas})", CORVERDE
    elif derrota:
        mensagem, cor = f"Palavra: {palavra.upper()}", CORAMARELO
    else:
        return
    rw = s(BASE_LARGURA - 100)
    rh = s(100)
    pygame.draw.rect(tela, (40, 40, 60), (tx(50), ty(BASE_ALTURA // 2 - 50), rw, rh), border_radius=s(15))
    escreverTexto(mensagem, 32, cor, BASE_LARGURA // 2, BASE_ALTURA // 2, bold=True)
    bw = s(200)
    bh = s(40)
    bx = tx(BASE_LARGURA // 2 - 100)
    by = ty(BASE_ALTURA // 2 + 30)
    pygame.draw.rect(tela, CORPLAYAGAIN, (bx, by, bw, bh), border_radius=s(10))
    f   = fonte(20)
    txt = f.render("Jogar Novamente", True, CORLETRAS)
    tela.blit(txt, txt.get_rect(center=(bx + bw // 2, by + bh // 2)))

#----Função que retorna o caminho da imagem de fundo baseado na rodada----
def carregarFundoPorRodada():
    if numRodada % 2 == 0:
        return "pic/backDoisFullscreen.jpg"
    else:
        return "pic/backFullscreen.jpg"

#----Função que escala a imagem de fundo para cobrir a tela inteira mantendo proporção (com recorte centralizado)----
def escalarFundoParaCobrir(imagem, largura_tela, altura_tela):
    """Escala a imagem para cobrir a tela inteira mantendo proporção e recortando o excesso"""
    larg_img, alt_img = imagem.get_size()
    
    # Calcula a escala necessária para cobrir a tela
    escala_x = largura_tela / larg_img
    escala_y = altura_tela / alt_img
    escala = max(escala_x, escala_y)  # Usa a maior escala para cobrir toda a tela
    
    # Escala a imagem mantendo a proporção
    nova_larg = int(larg_img * escala)
    nova_alt = int(alt_img * escala)
    imagem_escalada = pygame.transform.scale(imagem, (nova_larg, nova_alt))
    
    # Recorta a parte central para ajustar ao tamanho exato da tela
    offset_x = (nova_larg - largura_tela) // 2
    offset_y = (nova_alt - altura_tela) // 2
    rect_recorte = pygame.Rect(offset_x, offset_y, largura_tela, altura_tela)
    imagem_recortada = imagem_escalada.subsurface(rect_recorte).copy()
    
    return imagem_recortada

#----Função que verifica se o jogador clicou em jogar novamente----
def verificarClickJogarDenovo(pos):
    bx = tx(BASE_LARGURA // 2 - 100)
    by = ty(BASE_ALTURA  // 2 + 30)
    bw = s(200)
    bh = s(40)
    if (vitoria or derrota) and bx <= pos[0] <= bx + bw and by <= pos[1] <= by + bh:
        variaveisDeJogo()
        return True
    return False


global atentativa, showDica, numRodada
numRodada = 0
variaveisDeJogo()
rodando    = True
BACKGROUND = pygame.image.load(carregarFundoPorRodada())

#----Gera degradê de fundo inicial----
fundoDegrade   = gerarDegradeFundo(BASE_LARGURA, BASE_ALTURA)
tamanhoAnterior = tela.get_size()

while rodando:
    W, H = tela.get_size()

    #----Regera degradê somente quando a janela muda de tamanho----
    if (W, H) != tamanhoAnterior:
        fundoDegrade    = gerarDegradeFundo(W, H)
        tamanhoAnterior = (W, H)

    #----Fundo: degradê cobrindo toda a janela + background escalado e recortado para cobrir----
    BACKGROUND = pygame.image.load(carregarFundoPorRodada())
    tela.blit(fundoDegrade, (0, 0))
    bgFinal = escalarFundoParaCobrir(BACKGROUND, W, H)
    tela.blit(bgFinal, (0, 0))

    posicaoMouse = pygame.mouse.get_pos()
    escreverTexto(f"{len(palavra)} letras", 20, CORLETRAS, 90, 130)
    dicaBotao = botaoDica(posicaoMouse)
    escreverDica()
    desenharQuadros()
    printTeclado()
    desenhar_mensagem_final()

    #---- definindo oque irá acontencer cada evento que o jogador realizr----
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        #--defininco os eventos de teclas--
        elif evento.type == pygame.KEYDOWN:
        #/*--Mudar o plano de fundo se ele clicar nos teclados numéricos--*/
            if evento.key == pygame.K_0:
                BACKGROUND = pygame.image.load("pic/back.jpg")
            elif evento.key == pygame.K_1:
                BACKGROUND = pygame.image.load("pic/back1.jpg")
            elif evento.key == pygame.K_2:
                BACKGROUND = pygame.image.load("pic/back2.jpg")
            elif evento.key == pygame.K_3:
                BACKGROUND = pygame.image.load("pic/manoel.jpg")
            #/*----agora definindo a tecla de apagar, enter e os caracterees (teclado real pessoal do jogador)----*/
            elif not (vitoria or derrota):
                if evento.key == pygame.K_RETURN and len(atentativa) == len(palavra):
                    verificarTentativa()
                elif evento.key == pygame.K_BACKSPACE:
                    atentativa = atentativa[:-1]
                elif evento.unicode.isalpha() and len(atentativa) < len(palavra):
                    atentativa += evento.unicode.lower()
        #/*----Agora definindo onde o jogador clicou com o mouse(Se foi no botão de jogar novamente, botão de dica ou foi no teclado virtual)----*/
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if verificarClickJogarDenovo((x, y)):
                continue
            if dicaBotao.collidepoint(x, y):
                showDica = not showDica
            tecla = clickTecla((x, y))
            if tecla and not (vitoria or derrota):
                #----Processar botões especiais Apagar e Enviar do teclado virtual----
                if tecla == "__apagar__":
                    atentativa = atentativa[:-1]
                elif tecla == "__enviar__":
                    if len(atentativa) == len(palavra):
                        verificarTentativa()
                elif tecla.isalpha() and len(atentativa) < len(palavra):
                    atentativa += tecla

    pygame.display.update()

#AAAAAAACCCCAAAAABBBOUUUUUUUU!!!!!!!!!!!!!!