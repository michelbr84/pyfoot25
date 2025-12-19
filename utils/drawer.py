# Drawer: Interface de Menus e Navegação (Texto)


# --- Modo Texto ---
def menu_titulo(titulo, opcoes):
    print("\n" + "="*40)
    print(f"{titulo:^40}")
    print("="*40)
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    print("="*40)
    escolha = input("Escolha uma opção: ")
    return escolha


def tela_mensagem(mensagem):
    print("\n" + "-"*40)
    print(mensagem)
    print("-"*40)
    input("Pressione Enter para continuar...")


def mostrar_tabela_campeonato(tabela):
    print("\nTabela do Campeonato:")
    print("Pos  Clube         P  V  E  D  GP  GC  SG")
    for i, (clube, stats) in enumerate(tabela, 1):
        sg = stats["gp"] - stats["gc"]
        print(f"{i:>2}  {clube:<12} {stats['pontos']:>2} {stats['v']:>2} {stats['e']:>2} {stats['d']:>2}  {stats['gp']:>2}  {stats['gc']:>2}  {sg:>2}")


# --- Modo Gráfico (Pygame) ---
def menu_pygame(titulo, opcoes):
    import pygame
    pygame.init()
    largura, altura = 600, 400
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption(titulo)
    fonte = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    cor_fundo = (30, 30, 30)
    cor_texto = (255, 255, 255)
    cor_botao = (60, 60, 200)
    cor_botao_hover = (100, 100, 255)
    botoes = []
    espacamento = 60
    for i, opcao in enumerate(opcoes):
        rect = pygame.Rect(150, 100 + i*espacamento, 300, 50)
        botoes.append((rect, opcao))
    escolha = None
    while escolha is None:
        tela.fill(cor_fundo)
        titulo_render = fonte.render(titulo, True, cor_texto)
        tela.blit(titulo_render, (largura//2 - titulo_render.get_width()//2, 30))
        mouse = pygame.mouse.get_pos()
        for i, (rect, opcao) in enumerate(botoes):
            if rect.collidepoint(mouse):
                pygame.draw.rect(tela, cor_botao_hover, rect)
            else:
                pygame.draw.rect(tela, cor_botao, rect)
            txt = fonte.render(f"{i+1}. {opcao}", True, cor_texto)
            tela.blit(txt, (rect.x + 20, rect.y + 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (rect, _) in enumerate(botoes):
                    if rect.collidepoint(event.pos):
                        escolha = str(i+1)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]: escolha = "1"
                if event.key in [pygame.K_2, pygame.K_KP2]: escolha = "2"
                if event.key in [pygame.K_3, pygame.K_KP3]: escolha = "3"
                if event.key in [pygame.K_4, pygame.K_KP4]: escolha = "4"
                if event.key in [pygame.K_5, pygame.K_KP5]: escolha = "5"
                if event.key in [pygame.K_6, pygame.K_KP6]: escolha = "6"
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return escolha
