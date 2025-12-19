# Cena de Transferências/Leilão
from entities.transfer import TransferMarket


class TransferScene:
    def __init__(self, clubes, clube_usuario):
        self.market = TransferMarket(clubes)
        self.clube_usuario = clube_usuario

    def menu(self, modo_grafico=False):
        if not modo_grafico:
            while True:
                print("\n[Transferências]")
                print("1. Listar jogadores disponíveis")
                print("2. Comprar jogador")
                print("3. Sair")
                escolha = input("Escolha uma opção: ")
                if escolha == "1":
                    self.market.listar_jogadores()
                elif escolha == "2":
                    self.market.listar_jogadores()
                    idx = int(input("Digite o número do jogador a comprar: ")) - 1
                    preco = int(input("Digite o valor da oferta: "))
                    self.market.comprar_jogador(self.clube_usuario, idx, preco)
                elif escolha == "3":
                    break
                else:
                    print("Opção inválida!")
        else:
            import pygame
            pygame.init()
            largura, altura = 800, 600
            tela = pygame.display.set_mode((largura, altura))
            pygame.display.set_caption("Transferências")
            fonte = pygame.font.SysFont(None, 28)
            fonte_titulo = pygame.font.SysFont(None, 38)
            cor_fundo = (30, 30, 60)
            cor_texto = (255, 255, 255)
            cor_botao = (60, 120, 200)
            cor_botao_hover = (100, 180, 255)
            clock = pygame.time.Clock()
            rodando = True
            scroll = 0
            while rodando:
                tela.fill(cor_fundo)
                titulo = fonte_titulo.render("Transferências - Jogadores disponíveis", True, cor_texto)
                tela.blit(titulo, (largura//2 - titulo.get_width()//2, 20))
                # Lista de jogadores
                y = 80 - scroll
                botoes_jogadores = []
                for idx, (clube, jogador) in enumerate(self.market.jogadores_disponiveis):
                    rect = pygame.Rect(40, y, 600, 36)
                    pygame.draw.rect(tela, (50, 50, 100), rect)
                    txt = fonte.render(f"{idx+1}. {jogador.nome} ({jogador.posicao}) - Força: {jogador.forca} - Clube: {clube.nome}", True, cor_texto)
                    tela.blit(txt, (rect.x + 8, rect.y + 6))
                    botoes_jogadores.append((rect, idx, jogador, clube))
                    y += 40
                # Botão voltar
                botao_voltar = pygame.Rect(largura-160, altura-60, 120, 40)
                pygame.draw.rect(tela, cor_botao, botao_voltar)
                tela.blit(fonte.render("Voltar", True, (255,255,255)), (botao_voltar.x+20, botao_voltar.y+8))
                # Instrução
                tela.blit(fonte.render("Clique em um jogador para comprar", True, (200,200,200)), (40, altura-40))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if botao_voltar.collidepoint(event.pos):
                            rodando = False
                        for rect, idx, jogador, clube in botoes_jogadores:
                            if rect.collidepoint(event.pos):
                                # Caixa de oferta
                                preco = self._caixa_oferta_pygame(jogador, tela, fonte, largura, altura)
                                if preco is not None:
                                    self.market.comprar_jogador(self.clube_usuario, idx, preco)
                                    break
                    if event.type == pygame.MOUSEWHEEL:
                        scroll -= event.y * 40
                        scroll = max(0, scroll)
                pygame.display.flip()
                clock.tick(30)

    def _caixa_oferta_pygame(self, jogador, tela, fonte, largura, altura):
        import pygame
        input_ativo = True
        preco_str = ""
        clock = pygame.time.Clock()
        while input_ativo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if preco_str.isdigit():
                            return int(preco_str)
                        else:
                            return None
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        preco_str = preco_str[:-1]
                    elif event.unicode.isdigit():
                        preco_str += event.unicode
            tela.fill((40,40,80))
            msg = fonte.render(f"Oferta para {jogador.nome} (R$): {preco_str}", True, (255,255,255))
            tela.blit(msg, (largura//2 - msg.get_width()//2, altura//2 - 20))
            instr = fonte.render("Digite o valor e pressione Enter (ESC para cancelar)", True, (200,200,200))
            tela.blit(instr, (largura//2 - instr.get_width()//2, altura//2 + 20))
            pygame.display.flip()
            clock.tick(30)
