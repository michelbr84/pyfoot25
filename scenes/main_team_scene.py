# Cena principal do time: layout completo estilo Elifoot 98
import pygame

class MainTeamScene:
    def __init__(self, clube, treinador_nome, divisao, adversario=None, info_adversario=None, caixa=0, moral=0.7, pais="Brasil"):
        self.clube = clube
        self.treinador_nome = treinador_nome
        self.divisao = divisao
        self.adversario = adversario
        self.info_adversario = info_adversario or {}
        self.caixa = caixa
        self.moral = moral
        self.pais = pais
        # Paleta de cores (exemplo para Brasil)
        self.cores = {
            'dominante': (200, 30, 30),      # vermelho para listas/títulos
            'fundo': (245, 245, 245),        # fundo geral
            'destaque': (255, 215, 0),       # amarelo para barras/destaques
            'menu': (30, 30, 30),            # menus/bordas
            'borda': (80, 80, 80),
            'barra_moral': (30, 180, 60),
        }
        self.largura = 1080
        self.altura = 720
        self.scroll_jogadores = 0
        # Ensure titulares is initialized to avoid AttributeError
        self.titulares = self.clube.elenco[:11]  # Default to the first 11 players

    def desenhar_bandeira_brasil(self, tela, x, y):
        # Retângulo verde
        pygame.draw.rect(tela, (0, 156, 59), (x, y, 60, 40))
        # Losango amarelo
        pygame.draw.polygon(tela, (255, 223, 0), [(x+30, y+5), (x+55, y+20), (x+30, y+35), (x+5, y+20)])
        # Círculo azul
        pygame.draw.circle(tela, (33, 70, 139), (x+30, y+20), 10)

    def run(self):
        pygame.init()
        tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("PyFoot25 - Equipe")
        fonte_menu = pygame.font.SysFont(None, 22)
        fonte_titulo = pygame.font.SysFont(None, 32, bold=True)
        fonte_padrao = pygame.font.SysFont(None, 26)
        fonte_pequena = pygame.font.SysFont(None, 18)
        clock = pygame.time.Clock()
        rodando = True
        while rodando:
            tela.fill(self.cores['fundo'])
            largura, altura = tela.get_size()
            # Barra superior
            pygame.draw.rect(tela, self.cores['menu'], (0, 0, largura, 38))
            opcoes_menu = ["Pyfoot", "Selecionar", "Equipa", "Jogador", "Campeonato", "Treinador"]
            espacamento = largura // len(opcoes_menu)
            menu_botoes = []
            for i, opc in enumerate(opcoes_menu):
                btn_rect = pygame.Rect(i*espacamento+10, 4, espacamento-20, 30)
                cor_btn = self.cores['dominante'] if btn_rect.collidepoint(pygame.mouse.get_pos()) else self.cores['destaque']
                pygame.draw.rect(tela, cor_btn, btn_rect, border_radius=6)
                txt = fonte_menu.render(opc, True, (255,255,255))
                tela.blit(txt, (btn_rect.x+20, btn_rect.y+4))
                menu_botoes.append((opc, btn_rect))
            # Cabeçalho
            nome_treinador = fonte_titulo.render(self.treinador_nome, True, (200,0,0))
            tela.blit(nome_treinador, (20, 50))
            self.desenhar_bandeira_brasil(tela, 20, 90)
            tela.blit(fonte_padrao.render(self.pais, True, (0,0,0)), (90, 100))
            div_txt = fonte_pequena.render(f"{self.divisao}ª Divisão", True, (200,0,0))
            tela.blit(div_txt, (largura-160, 60))
            # Área esquerda (2/3): Lista de jogadores
            area_esq = pygame.Rect(0, 140, largura*2//3, altura-200)
            pygame.draw.rect(tela, self.cores['dominante'], area_esq, border_radius=8)
            # Tabela de jogadores
            y_jog = area_esq.y + 20 - self.scroll_jogadores
            for idx, jogador in enumerate(self.clube.elenco):
                cor_linha = (255,230,230) if idx%2==0 else (240,200,200)
                if idx == 0:
                    cor_linha = (255,255,255)
                linha_rect = pygame.Rect(area_esq.x+10, y_jog, area_esq.width-20, 36)
                pygame.draw.rect(tela, cor_linha, linha_rect, border_radius=6)
                # Posição
                letra = jogador.posicao[0].upper()
                txt_pos = fonte_padrao.render(letra, True, (80,0,0))
                tela.blit(txt_pos, (linha_rect.x+8, linha_rect.y+6))
                # Nome
                txt_nome = fonte_padrao.render(jogador.nome, True, (0,0,0))
                tela.blit(txt_nome, (linha_rect.x+40, linha_rect.y+6))
                # Força
                txt_forca = fonte_titulo.render(str(jogador.forca), True, (0,0,0))
                tela.blit(txt_forca, (linha_rect.x+220, linha_rect.y+2))
                # Valor
                valor = 100 + jogador.forca*10
                txt_valor = fonte_padrao.render(f"R${valor} mil", True, (0,0,0))
                tela.blit(txt_valor, (linha_rect.right-120, linha_rect.y+6))
                # Titular/reserva
                if jogador in self.titulares:
                    pygame.draw.circle(tela, (0,180,0), (linha_rect.right-30, linha_rect.y+18), 10)
                else:
                    pygame.draw.circle(tela, (180,180,180), (linha_rect.right-30, linha_rect.y+18), 10)
                y_jog += 40
            # Área direita (1/3): Info adversário, caixa, moral
            area_dir = pygame.Rect(largura*2//3+10, 140, largura//3-20, altura-200)
            pygame.draw.rect(tela, (230,230,255), area_dir, border_radius=8)
            y_dir = area_dir.y + 20
            if self.adversario:
                txt_adv = fonte_titulo.render(self.adversario, True, (0,0,120))
                tela.blit(txt_adv, (area_dir.x+10, y_dir))
                y_dir += 36
                tela.blit(fonte_padrao.render("CASA 4ª Jornada", True, (0,0,0)), (area_dir.x+10, y_dir))
                y_dir += 30
                # Resultados recentes (mock)
                tela.blit(fonte_pequena.render("SÃO PAULO 1-2", True, (0,0,0)), (area_dir.x+10, y_dir))
                y_dir += 22
                tela.blit(fonte_pequena.render("PALMEIRAS 2-1", True, (0,0,0)), (area_dir.x+10, y_dir))
                y_dir += 22
                # Árbitro
                tela.blit(fonte_pequena.render("Árbitro: Carlos (BRA)", True, self.cores['dominante']), (area_dir.x+10, y_dir))
                y_dir += 22
                # Último jogo
                tela.blit(fonte_titulo.render("D 1:2 (2025)", True, self.cores['dominante']), (area_dir.x+10, y_dir))
                y_dir += 40
            # Caixa
            tela.blit(fonte_padrao.render(f"Caixa: R${self.caixa//1000} mil", True, (0,120,0)), (area_dir.x+10, y_dir))
            y_dir += 30
            # Moral
            tela.blit(fonte_padrao.render("Moral:", True, (0,0,0)), (area_dir.x+10, y_dir))
            pygame.draw.rect(tela, (200,200,200), (area_dir.x+80, y_dir+8, 100, 16), border_radius=8)
            pygame.draw.rect(tela, self.cores['barra_moral'], (area_dir.x+80, y_dir+8, int(100*self.moral), 16), border_radius=8)
            # Barra inferior (menu)
            pygame.draw.rect(tela, self.cores['menu'], (0, altura-50, largura, 50))
            opcoes_rodape = ["Jogo", "Jogador", "Finanças", "Seleção", "Adversário"]
            espac_rodape = largura // len(opcoes_rodape)
            mouse = pygame.mouse.get_pos()
            botoes_rodape = []
            for i, opc in enumerate(opcoes_rodape):
                btn_rect = pygame.Rect(i*espac_rodape+10, altura-44, espac_rodape-20, 38)
                cor_btn = self.cores['dominante'] if btn_rect.collidepoint(mouse) else self.cores['destaque']
                pygame.draw.rect(tela, cor_btn, btn_rect, border_radius=8)
                txt = fonte_padrao.render(opc, True, (0,0,0))
                tela.blit(txt, (btn_rect.x+20, btn_rect.y+8))
                botoes_rodape.append((opc, btn_rect))
            # Scroll lista jogadores e botões
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scroll_jogadores = max(0, self.scroll_jogadores-40)
                    if event.button == 5:
                        self.scroll_jogadores += 40
                    if event.button == 1:
                        # Botoes superiores
                        for opc, btn_rect in menu_botoes:
                            if btn_rect.collidepoint(event.pos):
                                if opc == "Pyfoot":
                                    # Volta ao menu principal (simplesmente encerra a cena)
                                    rodando = False
                                elif opc == "Selecionar":
                                    # Seleção de elenco (abre SquadScene)
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(self.clube).mostrar_escalacao(modo_grafico=True)
                                elif opc == "Equipa":
                                    # Mostra elenco completo
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(self.clube).mostrar_escalacao(modo_grafico=True)
                                elif opc == "Jogador":
                                    # Mostra titulares
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(self.clube).mostrar_escalacao(modo_grafico=True)
                                elif opc == "Campeonato":
                                    # Mostra tabela do campeonato
                                    from data.database import get_divisoes
                                    from core.game import Campeonato
                                    from scenes.match_scene import mostrar_tabela_campeonato_pygame
                                    clubes_divisao = get_divisoes()[int(self.divisao)-1]["clubes"]
                                    from data.database import get_clubes
                                    from entities.player import Player
                                    from entities.club import Club
                                    clubes_objs = []
                                    clubes_data = get_clubes()
                                    for nome in clubes_divisao:
                                        dados = clubes_data[nome]
                                        elenco = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in dados["jogadores"]]
                                        clubes_objs.append(Club(nome, dados["cidade"], elenco))
                                    campeonato = Campeonato(f"Divisão {self.divisao}", clubes_objs)
                                    mostrar_tabela_campeonato_pygame([(c.nome, campeonato.tabela[c.nome]) for c in clubes_objs], nome_campeonato=f"Divisão {self.divisao}")
                                elif opc == "Treinador":
                                    # Mostra info do treinador
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(self.clube).mostrar_escalacao(modo_grafico=True)
                        # Botoes inferiores (rodapé)
                        for opc, btn_rect in botoes_rodape:
                            if btn_rect.collidepoint(event.pos):
                                if opc == "Jogador":
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(self.clube).mostrar_escalacao(modo_grafico=True)
                                elif opc == "Jogo":
                                    from data.database import get_divisoes, get_clubes
                                    clubes_divisao = get_divisoes()[int(self.divisao)-1]["clubes"]
                                    import random
                                    oponente_nome = random.choice([c for c in clubes_divisao if c != self.clube.nome])
                                    from entities.club import Club
                                    from entities.match import Match
                                    oponente_data = get_clubes()[oponente_nome]
                                    from entities.player import Player
                                    elenco_oponente = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in oponente_data["jogadores"]]
                                    oponente = Club(oponente_nome, oponente_data["cidade"], elenco_oponente)
                                    partida = Match(self.clube, oponente)
                                    partida.simular()
                                    from scenes.match_scene import mostrar_relatorio_partida
                                    mostrar_relatorio_partida(partida.relatorio(), modo_grafico=True)
                                elif opc == "Finanças":
                                    from scenes.finance_scene import FinanceScene
                                    FinanceScene(self.clube).menu(modo_grafico=True)
                                elif opc == "Seleção":
                                    from data.database import get_clubes
                                    from scenes.transfer_scene import TransferScene
                                    # Para transferências, passar todos os clubes (exceto None)
                                    clubes_data = get_clubes()
                                    from entities.player import Player
                                    from entities.club import Club
                                    clubes_objs = {}
                                    for nome, dados in clubes_data.items():
                                        elenco = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in dados["jogadores"]]
                                        clubes_objs[nome] = Club(nome, dados["cidade"], elenco)
                                    TransferScene(clubes_objs, self.clube).menu(modo_grafico=True)
                                elif opc == "Adversário":
                                    # Mostra elenco do adversário atual, se houver
                                    from data.database import get_divisoes, get_clubes
                                    clubes_divisao = get_divisoes()[int(self.divisao)-1]["clubes"]
                                    import random
                                    oponente_nome = random.choice([c for c in clubes_divisao if c != self.clube.nome])
                                    oponente_data = get_clubes()[oponente_nome]
                                    from entities.player import Player
                                    from entities.club import Club
                                    elenco_oponente = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in oponente_data["jogadores"]]
                                    oponente = Club(oponente_nome, oponente_data["cidade"], elenco_oponente)
                                    from scenes.squad_scene import SquadScene
                                    SquadScene(oponente).mostrar_escalacao(modo_grafico=True)
            pygame.display.flip()
            clock.tick(30)
