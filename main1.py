import pygame
import time
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Configurações do jogo ----------------------------------------------------------------------
largura, altura = 800, 600
tamanho_celula = 20
velocidade = 5
pontos_por_nivel = 100
#---------------------------------------------------------------------------------------------
# Cores----------------------------------------------------------------------------------------
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
#----------------------------------------------------------------------------------------------
# Inicialização da tela -----------------------------------------------------------------------
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("snake Dev Joel")
#----------------------------------------------------------------------------------------------
# Inicialização do Tkinter---------------------------------------------------------------------
root = tk.Tk()
root.withdraw()  # Oculta a janela principal do Tkinter
#----------------------------------------------------------------------------------------------
# Função que desenha a cobra na tela ----------------------------------------------------------
def desenha_cobra(cobra, tamanho_celula):
    for segmento in cobra:
        pygame.draw.rect(tela, verde, [segmento[0], segmento[1], tamanho_celula, tamanho_celula])
#-----------------------------------------------------------------------------------------------
# Função para exibir a pontuação e o nível na tela -------------------------------------------------
def exibir_pontuacao(pontuacao, nivel):
    fonte_pontuacao = pygame.font.SysFont(None, 30)
    texto_pontuacao = fonte_pontuacao.render(f'Pontuação: {pontuacao} | Nível: {nivel}', True, verde)
    tela.blit(texto_pontuacao, (10, 10))
#---------------------------------------------------------------------------------------------------
# Função principal do jogo -------------------------------------------------------------------------
def jogo():
    global velocidade
    jogo_ativo = True
    game_over = False
    nivel_alcancado = False
    pygame_encerrado = False  # Adicionada a variável para verificar se o pygame foi encerrado

    # Inicialização da cobra -----------------------------------------------------------------------
    cobra = [[largura // 2, altura // 2]]
    cobra_comprimento = 1
    #-----------------------------------------------------------------------------------------------
    # Inicialização da comida ---------------------------------------------------------------------
    comida = [random.randrange(1, (largura // tamanho_celula)) * tamanho_celula,
              random.randrange(1, (altura // tamanho_celula)) * tamanho_celula]
    #---------------------------------------------------------------------------------------------
    # Inicialização da direção da cobra ----------------------------------------------------------
    direcao = 'DIREITA'
    mudar_direcao = direcao
    #---------------------------------------------------------------------------------------------
    # Pontuação ----------------------------------------------------------------------------------
    pontuacao = 0
    nivel = 1
    #---------------------------------------------------------------------------------------------
    # Loop principal do jogo ---------------------------------------------------------------------
    while jogo_ativo:
        while game_over:
            tela.fill(branco)
            fonte = pygame.font.SysFont(None, 55)

            # Renderiza três linhas separadas
            linha1 = fonte.render(f"Fim do Jogo! Pontuação: {pontuacao}. Nível: {nivel}", True, vermelho)
            linha2 = fonte.render("Pressione Q para sair", True, vermelho)
            linha3 = fonte.render("Pressione C para jogar novamente", True, vermelho)

            # Calcula a posição para centralizar a mensagem na tela
            pos_x1 = (largura - linha1.get_width()) // 2
            pos_y1 = (altura - linha1.get_height() - linha2.get_height() - linha3.get_height()) // 2

            pos_x2 = (largura - linha2.get_width()) // 2
            pos_y2 = pos_y1 + linha1.get_height()

            pos_x3 = (largura - linha3.get_width()) // 2
            pos_y3 = pos_y2 + linha2.get_height()

            tela.blit(linha1, [pos_x1, pos_y1])
            tela.blit(linha2, [pos_x2, pos_y2])
            tela.blit(linha3, [pos_x3, pos_y3])

            pygame.display.update()
    
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        jogo_ativo = False
                        game_over = False
                    elif event.key == pygame.K_c:
                        jogo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_ativo = False
                pygame_encerrado = True  # Defina a variável como True antes de sair do loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not direcao == 'DIREITA':
                    mudar_direcao = 'ESQUERDA'
                elif event.key == pygame.K_RIGHT and not direcao == 'ESQUERDA':
                    mudar_direcao = 'DIREITA'
                elif event.key == pygame.K_UP and not direcao == 'BAIXO':
                    mudar_direcao = 'CIMA'
                elif event.key == pygame.K_DOWN and not direcao == 'CIMA':
                    mudar_direcao = 'BAIXO'

        # Atualiza a direção da cobra --------------------------------------------------------------------
        direcao = mudar_direcao

        # Move a cobra na direção atual
        if direcao == 'DIREITA':
            cobra[0][0] += tamanho_celula
        elif direcao == 'ESQUERDA':
            cobra[0][0] -= tamanho_celula
        elif direcao == 'CIMA':
            cobra[0][1] -= tamanho_celula
        elif direcao == 'BAIXO':
            cobra[0][1] += tamanho_celula

        # Verifica as colisões com a parede
        if cobra[0][0] >= largura or cobra[0][0] < 0 or cobra[0][1] >= altura or cobra[0][1] < 0:
            game_over = True

        # Verifica a colisão com a própria cobra
        for segmento in cobra[1:]:
            if cobra[0][0] == segmento[0] and cobra[0][1] == segmento[1]:
                game_over = True

        # Verifica a colisão com a comida
        if cobra[0][0] == comida[0] and cobra[0][1] == comida[1]:
            comida = [random.randrange(1, (largura // tamanho_celula)) * tamanho_celula,
                      random.randrange(1, (altura // tamanho_celula)) * tamanho_celula]
            cobra.append([0, 0])
            cobra_comprimento += 1
            pontuacao += 10  # Incrementa a pontuação ao comer a comida

            # Verifica se atingiu 100 pontos para passar de nível
            if pontuacao % pontos_por_nivel == 0 and not nivel_alcancado:
                nivel_alcancado = True
                tela.fill(branco)
                fonte = pygame.font.SysFont(None, 55)
                linha1 = fonte.render(f"Parabéns! Você alcançou o Nível {nivel}.", True, vermelho)
                linha2 = fonte.render("Pressione C para continuar", True, vermelho)
                pos_x1 = (largura - linha1.get_width()) // 2
                pos_y1 = (altura - linha1.get_height() - linha2.get_height()) // 2
                pos_x2 = (largura - linha2.get_width()) // 2
                pos_y2 = pos_y1 + linha1.get_height()
                tela.blit(linha1, [pos_x1, pos_y1])
                tela.blit(linha2, [pos_x2, pos_y2])
                pygame.display.update()

                # Aguarda o jogador pressionar "C" para continuar
                espera_continuar = True
                while espera_continuar:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                            espera_continuar = False
                            nivel_alcancado = False
                nivel += 1
                velocidade += 5  # Aumenta a velocidade a cada novo nível

        # Atualiza o fundo da tela
        tela.fill(branco)

        # Desenha a comida
        pygame.draw.rect(tela, vermelho, [comida[0], comida[1], tamanho_celula, tamanho_celula])

        # Atualiza a posição da cobra
        for i in range(cobra_comprimento - 1, 0, -1):
            cobra[i] = [cobra[i - 1][0], cobra[i - 1][1]]

        # Desenha a cobra na tela
        desenha_cobra(cobra, tamanho_celula)

        # Exibe a pontuação e o nível na tela
        exibir_pontuacao(pontuacao, nivel)

        # Atualiza a tela
        pygame.display.update()

        # Controle de velocidade
        pygame.time.Clock().tick(velocidade)

    # Verifica se o pygame foi encerrado antes de chamar pygame.quit()
    if not pygame_encerrado:
        pygame.quit()

# Inicia o jogo ----------------------------------------------------------------------------------------
jogo()
#-------------------------------------------------------------------------------------------------------
