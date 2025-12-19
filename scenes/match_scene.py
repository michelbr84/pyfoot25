# Cena de Relatório de Partida/Tabela em Pygame
import pygame

def mostrar_relatorio_partida(relatorio, modo_grafico=False):
    if not modo_grafico:
        print(relatorio)
        input("Pressione Enter para voltar...")
        return
    pygame.init()
    largura, altura = 700, 500
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Relatório da Partida")
    fonte = pygame.font.SysFont(None, 28)
    fonte_titulo = pygame.font.SysFont(None, 36)
    cor_fundo = (40, 40, 40)
    cor_texto = (255, 255, 255)
    clock = pygame.time.Clock()
    rodando = True
    linhas = relatorio.split("\n")
    while rodando:
        tela.fill(cor_fundo)
        titulo = fonte_titulo.render("Relatório da Partida", True, cor_texto)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 20))
        y = 80
        for linha in linhas:
            txt = fonte.render(linha, True, cor_texto)
            tela.blit(txt, (60, y))
            y += 30
        # Botão voltar
        botao_voltar = pygame.Rect(largura//2 - 60, altura - 60, 120, 40)
        pygame.draw.rect(tela, (80, 80, 200), botao_voltar)
        botao_txt = fonte.render("Voltar", True, (255,255,255))
        tela.blit(botao_txt, (botao_voltar.x + 20, botao_voltar.y + 8))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    rodando = False
        pygame.display.flip()
        clock.tick(30)
    return

def mostrar_tabela_campeonato_pygame(tabela, nome_campeonato="Campeonato"):
    pygame.init()
    largura, altura = 700, 500
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(f"Tabela - {nome_campeonato}")
    fonte = pygame.font.SysFont(None, 28)
    fonte_titulo = pygame.font.SysFont(None, 36)
    cor_fundo = (30, 30, 60)
    cor_texto = (255, 255, 255)
    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        tela.fill(cor_fundo)
        titulo = fonte_titulo.render(f"Tabela - {nome_campeonato}", True, cor_texto)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 20))
        y = 80
        cabecalho = fonte.render("Pos  Clube         P  V  E  D  GP  GC  SG", True, cor_texto)
        tela.blit(cabecalho, (60, y))
        y += 30
        for i, (clube, stats) in enumerate(tabela, 1):
            sg = stats["gp"] - stats["gc"]
            linha = f"{i:>2}  {clube:<12} {stats['pontos']:>2} {stats['v']:>2} {stats['e']:>2} {stats['d']:>2}  {stats['gp']:>2}  {stats['gc']:>2}  {sg:>2}"
            txt = fonte.render(linha, True, cor_texto)
            tela.blit(txt, (60, y))
            y += 28
        # Botão voltar
        botao_voltar = pygame.Rect(largura//2 - 60, altura - 60, 120, 40)
        pygame.draw.rect(tela, (80, 80, 200), botao_voltar)
        botao_txt = fonte.render("Voltar", True, (255,255,255))
        tela.blit(botao_txt, (botao_voltar.x + 20, botao_voltar.y + 8))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    rodando = False
        pygame.display.flip()
        clock.tick(30)
    return
