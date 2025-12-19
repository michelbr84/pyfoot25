# Cena de Finanças do Clube
from finance.finances import Finances
from finance.stadium import Stadium


class FinanceScene:
    def __init__(self, clube):
        self.clube = clube
        if not hasattr(clube, "financas"):
            self.clube.financas = Finances(clube.caixa)
        if not hasattr(clube, "estadio_obj"):
            self.clube.estadio_obj = Stadium(clube.estadio["nome"], clube.estadio["capacidade"])

    def menu(self, modo_grafico=False):
        if not modo_grafico:
            while True:
                print("\n[Finanças]")
                print("1. Ver saldo e relatório")
                print("2. Melhorar estádio")
                print("3. Voltar")
                escolha = input("Escolha uma opção: ")
                if escolha == "1":
                    print(self.clube.financas.relatorio())
                elif escolha == "2":
                    self.clube.estadio_obj.upgrade()
                    self.clube.financas.registrar_despesa(5000000, "Upgrade do estádio")
                elif escolha == "3":
                    break
                else:
                    print("Opção inválida!")
        else:
            import pygame
            pygame.init()
            largura, altura = 700, 500
            tela = pygame.display.set_mode((largura, altura))
            pygame.display.set_caption("Finanças")
            fonte = pygame.font.SysFont(None, 30)
            fonte_titulo = pygame.font.SysFont(None, 38)
            cor_fundo = (30, 60, 30)
            cor_texto = (255, 255, 255)
            cor_botao = (60, 120, 60)
            cor_botao_hover = (100, 180, 100)
            clock = pygame.time.Clock()
            rodando = True
            while rodando:
                tela.fill(cor_fundo)
                titulo = fonte_titulo.render(f"Finanças - {self.clube.nome}", True, cor_texto)
                tela.blit(titulo, (largura//2 - titulo.get_width()//2, 20))
                # Saldo
                saldo = fonte.render(f"Saldo atual: R${self.clube.financas.saldo}", True, cor_texto)
                tela.blit(saldo, (60, 80))
                # Relatório receitas/despesas
                y = 120
                tela.blit(fonte.render("Receitas:", True, (100,255,100)), (60, y))
                y += 28
                for valor, desc in self.clube.financas.receitas[-5:]:
                    tela.blit(fonte.render(f"+R${valor} - {desc}", True, (180,255,180)), (80, y))
                    y += 22
                y += 10
                tela.blit(fonte.render("Despesas:", True, (255,100,100)), (60, y))
                y += 28
                for valor, desc in self.clube.financas.despesas[-5:]:
                    tela.blit(fonte.render(f"-R${valor} - {desc}", True, (255,180,180)), (80, y))
                    y += 22
                # Botão melhorar estádio
                botao_estadio = pygame.Rect(60, altura-80, 220, 40)
                pygame.draw.rect(tela, cor_botao, botao_estadio)
                tela.blit(fonte.render("Melhorar Estádio", True, (255,255,255)), (botao_estadio.x+20, botao_estadio.y+8))
                # Botão voltar
                botao_voltar = pygame.Rect(largura-160, altura-80, 120, 40)
                pygame.draw.rect(tela, cor_botao, botao_voltar)
                tela.blit(fonte.render("Voltar", True, (255,255,255)), (botao_voltar.x+20, botao_voltar.y+8))
                # Info estádio
                estadio = self.clube.estadio_obj
                info_estadio = fonte.render(f"Estádio: {estadio.nome} | Capacidade: {estadio.capacidade}", True, (200,200,255))
                tela.blit(info_estadio, (60, altura-120))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if botao_voltar.collidepoint(event.pos):
                            rodando = False
                        if botao_estadio.collidepoint(event.pos):
                            estadio.upgrade()
                            self.clube.financas.registrar_despesa(5000000, "Upgrade do estádio")
                pygame.display.flip()
                clock.tick(30)
            return
