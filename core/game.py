from entities.club import Club
from entities.match import Match
from data.database import get_divisoes, get_clubes
from data.save_load import salvar_jogo, carregar_jogo
from scenes.squad_scene import SquadScene
from scenes.transfer_scene import TransferScene
from scenes.finance_scene import FinanceScene
from scenes.match_scene import mostrar_relatorio_partida, mostrar_tabela_campeonato_pygame
import random

class Campeonato:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes  # lista de Club
        self.tabela = {clube.nome: {"pontos": 0, "v": 0, "e": 0, "d": 0, "gp": 0, "gc": 0} for clube in clubes}
        self.rodada = 1
        self.jogos_restantes = self._gerar_jogos_ida_e_volta()
        self.gols_jogadores = {}  # (nome, clube) -> gols

    def _gerar_jogos_ida_e_volta(self):
        jogos = []
        for i, clube1 in enumerate(self.clubes):
            for j, clube2 in enumerate(self.clubes):
                if i != j:
                    jogos.append((clube1, clube2))
        random.shuffle(jogos)
        return jogos

    def proxima_rodada(self):
        if not self.jogos_restantes:
            return False
        print(f"\nRodada {self.rodada} - {self.nome}")
        jogos_rodada = []
        clubes_usados = set()
        for jogo in self.jogos_restantes:
            c1, c2 = jogo
            if c1 not in clubes_usados and c2 not in clubes_usados:
                jogos_rodada.append(jogo)
                clubes_usados.add(c1)
                clubes_usados.add(c2)
        for jogo in jogos_rodada:
            partida = Match(jogo[0], jogo[1])
            partida.simular()
            print(partida.relatorio())
            self._atualizar_tabela(jogo[0], jogo[1], partida.gols_casa, partida.gols_fora)
            self.jogos_restantes.remove(jogo)
        self.rodada += 1
        return True

    def _atualizar_tabela(self, clube1, clube2, gols1, gols2):
        self.tabela[clube1.nome]["gp"] += gols1
        self.tabela[clube1.nome]["gc"] += gols2
        self.tabela[clube2.nome]["gp"] += gols2
        self.tabela[clube2.nome]["gc"] += gols1
        if gols1 > gols2:
            self.tabela[clube1.nome]["pontos"] += 3
            self.tabela[clube1.nome]["v"] += 1
            self.tabela[clube2.nome]["d"] += 1
        elif gols2 > gols1:
            self.tabela[clube2.nome]["pontos"] += 3
            self.tabela[clube2.nome]["v"] += 1
            self.tabela[clube1.nome]["d"] += 1
        else:
            self.tabela[clube1.nome]["pontos"] += 1
            self.tabela[clube2.nome]["pontos"] += 1
            self.tabela[clube1.nome]["e"] += 1
            self.tabela[clube2.nome]["e"] += 1

    def mostrar_tabela(self):
        print(f"\nTabela do {self.nome}:")
        tabela_ordenada = sorted(self.tabela.items(), key=lambda x: (-x[1]["pontos"], -(x[1]["gp"]-x[1]["gc"]), -x[1]["gp"]))
        print("Pos  Clube         P  V  E  D  GP  GC  SG")
        for i, (clube, stats) in enumerate(tabela_ordenada, 1):
            sg = stats["gp"] - stats["gc"]
            print(f"{i:>2}  {clube:<12} {stats['pontos']:>2} {stats['v']:>2} {stats['e']:>2} {stats['d']:>2}  {stats['gp']:>2}  {stats['gc']:>2}  {sg:>2}")

    def promocoes_rebaixamentos(self, n_promove=2, n_rebaixa=2):
        tabela_ordenada = sorted(self.tabela.items(), key=lambda x: (-x[1]["pontos"], -(x[1]["gp"]-x[1]["gc"]), -x[1]["gp"]))
        promovidos = [clube for clube, _ in tabela_ordenada[:n_promove]]
        rebaixados = [clube for clube, _ in tabela_ordenada[-n_rebaixa:]]
        print(f"\nPromovidos: {', '.join(promovidos)}")
        print(f"Rebaixados: {', '.join(rebaixados)}")
        return promovidos, rebaixados

class Copa:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes[:]
        random.shuffle(self.clubes)
        self.fase = 1
        self.gols_jogadores = {}  # Track goals for copa competitions
        self.fase_nomes = {1: "Primeira Fase", 2: "Oitavas de Final", 3: "Quartas de Final", 4: "Semifinal", 5: "Final"}

    def jogar_fase(self):
        print(f"\nCopa {self.nome} - {self.fase_nomes.get(self.fase, f'Fase {self.fase}')}")
        classificados = []
        for i in range(0, len(self.clubes), 2):
            if i+1 >= len(self.clubes):
                classificados.append(self.clubes[i])
                print(f"{self.clubes[i].nome} avançou por WO!")
                continue
            
            partida = Match(self.clubes[i], self.clubes[i+1])
            partida.simular()
            print(partida.relatorio())
            
            # Track goals in copa
            for artilheiro, clube in partida.goleadores:
                chave = (artilheiro.nome, clube.nome)
                self.gols_jogadores[chave] = self.gols_jogadores.get(chave, 0) + 1
            
            if partida.gols_casa > partida.gols_fora:
                classificados.append(self.clubes[i])
            elif partida.gols_fora > partida.gols_casa:
                classificados.append(self.clubes[i+1])
            else:
                vencedor = random.choice([self.clubes[i], self.clubes[i+1]])
                classificados.append(vencedor)
                print(f"Decisão nos pênaltis: {vencedor.nome} classificado!")
        
        self.clubes = classificados
        self.fase += 1
        return len(self.clubes) > 1

    def mostrar_classificados(self):
        print(f"Classificados para a próxima fase: {', '.join([c.nome for c in self.clubes])}")
        
    def mostrar_artilheiros(self, modo_grafico=False):
        from utils.helpers import mostrar_ranking_artilheiros
        ranking = sorted(self.gols_jogadores.items(), key=lambda x: -x[1])
        print(f"\nArtilheiros da {self.nome}:")
        mostrar_ranking_artilheiros(ranking, modo_grafico=modo_grafico)
# Núcleo do Jogo: Loop Principal
from core.state_manager import StateManager


from utils.drawer import menu_titulo, menu_pygame

def input_int(msg, minv=None, maxv=None, modo_grafico=False):
    if modo_grafico:
        # Não usado diretamente, menus são gráficos
        return None
    while True:
        try:
            v = int(input(msg))
            if (minv is not None and v < minv) or (maxv is not None and v > maxv):
                print(f"Valor deve ser entre {minv} e {maxv}.")
                continue
            return v
        except ValueError:
            print("Digite um número válido.")


def main_loop(modo_grafico=False):
    # Ensure pygame.quit() is only called when the application exits completely
    if modo_grafico:
        import pygame
        pygame.init()
    try:
        if modo_grafico:
            menu = menu_pygame
        else:
            menu = menu_titulo

        print("Bem-vindo ao PyFoot25!")
        # Seleção de modo de jogo
        opcoes_modo = ["Um jogador", "Multijogador local (turnos)"]
        modo = menu("Seleção de Modo", opcoes_modo)
        jogadores = []
        clubes_disponiveis = list(get_clubes().keys())
        clubes_jogadores = {}
        treinador_nome = "Treinador"
        if modo == "2":
            n = 2
            if not modo_grafico:
                n = input_int("Quantos jogadores? (2-4): ", 2, 4)
            for i in range(n):
                if not modo_grafico:
                    nome = input(f"Nome do jogador {i+1}: ")
                else:
                    nome = f"Jogador {i+1}"
                opcoes_clubes = [c for c in clubes_disponiveis]
                idx_clube = int(menu(f"{nome} - Escolha seu clube", opcoes_clubes)) - 1
                clubes_jogadores[nome] = clubes_disponiveis.pop(idx_clube)
                jogadores.append(nome)
        else:
            nome = "Jogador 1"
            opcoes_clubes = [c for c in clubes_disponiveis]
            idx_clube = int(menu(f"{nome} - Escolha seu clube", opcoes_clubes)) - 1
            clubes_jogadores[nome] = clubes_disponiveis.pop(idx_clube)
            jogadores = [nome]
            # Solicita nome do treinador
            if not modo_grafico:
                treinador_nome = input("Digite seu nome de treinador: ")
            else:
                import pygame
                pygame.init()
                largura, altura = 500, 200
                tela = pygame.display.set_mode((largura, altura))
                pygame.display.set_caption("Nome do Treinador")
                fonte = pygame.font.SysFont(None, 36)
                nome_input = ""
                ativo = True
                while ativo:
                    tela.fill((30,30,30))
                    txt = fonte.render("Digite seu nome de treinador:", True, (255,255,255))
                    tela.blit(txt, (30, 40))
                    box = pygame.Rect(30, 90, 440, 40)
                    pygame.draw.rect(tela, (200,200,200), box, 2)
                    nome_txt = fonte.render(nome_input, True, (255,0,0))
                    tela.blit(nome_txt, (box.x+10, box.y+5))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                if nome_input.strip():
                                    ativo = False
                                    break
                            elif event.key == pygame.K_BACKSPACE:
                                nome_input = nome_input[:-1]
                            elif len(nome_input) < 20 and event.unicode.isprintable():
                                nome_input += event.unicode
                    pygame.display.flip()
                    pygame.time.delay(100)  # Prevent high CPU usage
                treinador_nome = nome_input.strip() or "Treinador"
                pygame.quit()
            # Exibe tela principal do time
            from scenes.main_team_scene import MainTeamScene
            div_usuario = 3
            clubes_data = get_clubes()
            clubes_obj = {}
            for nomec, dados in clubes_data.items():
                from entities.player import Player
                elenco = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in dados["jogadores"]]
                clubes_obj[nomec] = Club(nomec, dados["cidade"], elenco)
            clube_nome = clubes_jogadores[nome]
            clube = clubes_obj[clube_nome]
            cena = MainTeamScene(clube, treinador_nome, divisao="4", adversario="Clube1", caixa=clube.caixa, moral=0.7)
            cena.run()
        state_manager = StateManager(jogadores)

        clubes_data = get_clubes()
        clubes_obj = {}
        for nome, dados in clubes_data.items():
            from entities.player import Player
            elenco = [Player(j["nome"], j["posicao"], j["forca"], j.get("status", "apto"), j.get("salario"), j.get("contrato_restante")) for j in dados["jogadores"]]
            clubes_obj[nome] = Club(nome, dados["cidade"], elenco)

        # Usuário sempre começa na 4ª divisão
        div_usuario = 3  # 0-index: 3 = 4ª divisão
        clubes_divisao = [clubes_obj[nome] for nome in get_divisoes()[div_usuario]["clubes"] if nome in clubes_obj]
        campeonato = Campeonato(get_divisoes()[div_usuario]["nome"], clubes_divisao)
        relatorios_ultima_rodada = []
        nome_divisao_usuario = get_divisoes()[div_usuario]["nome"]

        while state_manager.running:
            state = state_manager.get_state()
            if state == "main_menu":
                opcoes_menu = ["Iniciar novo jogo", "Carregar jogo", "Sair"]
                escolha = menu("Menu Principal", opcoes_menu)
                if escolha == "1":
                    state_manager.set_state("gameplay")
                elif escolha == "2":
                    from data.save_load import carregar_jogo_completo
                    save_data = carregar_jogo_completo()
                    if save_data:
                        state_manager = save_data["state_manager"]
                        campeonato = save_data["campeonato"]
                        relatorios_ultima_rodada = save_data["relatorios_ultima_rodada"]
                elif escolha == "3":
                    state_manager.stop()
            elif state == "gameplay":
                jogador_atual = state_manager.get_jogador_atual()
                clube_nome = clubes_jogadores[jogador_atual]
                clube = clubes_obj[clube_nome]
                opcoes_jogo = [
                    "Jogar rodada",
                    "Ver elenco e escalação",
                    "Transferências",
                    "Finanças",
                    "Relatórios da última rodada",
                    "Tabela do campeonato",
                    "Salvar jogo",
                    "Sair para o menu"
                ]
                opcoes_jogo.insert(6, "Ranking de artilheiros")
                escolha = menu(f"Rodada {state_manager.turn} - Vez de {jogador_atual} ({clube_nome}) - {nome_divisao_usuario}", opcoes_jogo)
                if escolha == "1":
                    # Avança turno dos jogadores do clube do usuário
                    for jogador in clube.elenco:
                        jogador.avancar_turno()
                    # Simula a rodada completa do campeonato
                    relatorios_ultima_rodada = []
                    jogos_rodada = []
                    clubes_usados = set()
                    # Seleciona os jogos da rodada (mesma lógica do Campeonato.proxima_rodada)
                    for jogo in campeonato.jogos_restantes:
                        c1, c2 = jogo
                        if c1 not in clubes_usados and c2 not in clubes_usados:
                            jogos_rodada.append(jogo)
                            clubes_usados.add(c1)
                            clubes_usados.add(c2)
                    for jogo in jogos_rodada:
                        partida = Match(jogo[0], jogo[1])
                        partida.simular()
                        relatorios_ultima_rodada.append(partida.relatorio())
                        # Atualiza artilharia
                        for artilheiro, clube_ in getattr(partida, "goleadores", []):
                            chave = (artilheiro.nome, clube_.nome)
                            campeonato.gols_jogadores[chave] = campeonato.gols_jogadores.get(chave, 0) + 1
                        campeonato._atualizar_tabela(jogo[0], jogo[1], partida.gols_casa, partida.gols_fora)
                        campeonato.jogos_restantes.remove(jogo)
                    campeonato.rodada += 1
                    # Deduz salários dos jogadores de todos os clubes e avança contratos
                    for clube_sal in campeonato.clubes:
                        total_salarios = 0
                        jogadores_a_remover = []
                        for j in clube_sal.elenco:
                            total_salarios += j.salario
                            # Reduz contrato_restante se for maior que 0
                            if hasattr(j, 'contrato_restante') and j.contrato_restante > 0:
                                j.contrato_restante -= 1
                                # Se contrato chegou a 0, marca para remoção
                                if j.contrato_restante == 0:
                                    jogadores_a_remover.append(j)
                        clube_sal.caixa -= total_salarios
                        if hasattr(clube_sal, "financas"):
                            clube_sal.financas.registrar_despesa(total_salarios, "Salários dos jogadores")
                        # Remove jogadores com contrato expirado (libera para "mercado livre")
                        for j in jogadores_a_remover:
                            if j in clube_sal.elenco:
                                clube_sal.elenco.remove(j)
                                # Opcional: adicionar a um mercado livre global
                                print(f"{j.nome} ({clube_sal.nome}) teve o contrato encerrado e foi liberado.")
                    # Exibe todos os relatórios da rodada
                    if not modo_grafico:
                        print("\nRelatórios da rodada:")
                        for rel in relatorios_ultima_rodada:
                            print(rel)
                            print("-"*40)
                    else:
                        for rel in relatorios_ultima_rodada:
                            mostrar_relatorio_partida(rel, modo_grafico=True)
                    # Exibe a tabela real após a rodada
                    tabela_ordenada = sorted(campeonato.tabela.items(), key=lambda x: (-x[1]["pontos"], -(x[1]["gp"]-x[1]["gc"]), -x[1]["gp"]))
                    tabela = [(clube, stats) for clube, stats in tabela_ordenada]
                    if modo_grafico:
                        mostrar_tabela_campeonato_pygame(tabela, nome_campeonato=campeonato.nome)
                    else:
                        from utils.drawer import mostrar_tabela_campeonato
                        mostrar_tabela_campeonato(tabela)
                    # Checa fim do campeonato
                    if not campeonato.jogos_restantes:
                        # Promoção/rebaixamento
                        tabela_ordenada = sorted(campeonato.tabela.items(), key=lambda x: (-x[1]["pontos"], -(x[1]["gp"]-x[1]["gc"]), -x[1]["gp"]))
                        promovidos = [clube for clube, _ in tabela_ordenada[:2]]
                        rebaixados = [clube for clube, _ in tabela_ordenada[-2:]]
                        print(f"\nPromovidos: {', '.join(promovidos)}")
                        print(f"Rebaixados: {', '.join(rebaixados)}")
                        # Usuário foi promovido?
                        if clube_nome in promovidos and div_usuario > 0:
                            div_usuario -= 1
                            nome_divisao_usuario = get_divisoes()[div_usuario]["nome"]
                            print(f"Parabéns! Você subiu para a {nome_divisao_usuario}!")
                        # Usuário foi rebaixado?
                        elif clube_nome in rebaixados:
                            if div_usuario == 3:
                                print("Você foi rebaixado na 4ª divisão. Game Over!")
                                state_manager.set_state("season_over")
                                continue
                            else:
                                div_usuario += 1
                                nome_divisao_usuario = get_divisoes()[div_usuario]["nome"]
                                print(f"Você foi rebaixado para a {nome_divisao_usuario}.")
                        # Novo campeonato para próxima temporada
                        clubes_divisao = [clubes_obj[nome] for nome in get_divisoes()[div_usuario]["clubes"] if nome in clubes_obj]
                        campeonato = Campeonato(get_divisoes()[div_usuario]["nome"], clubes_divisao)
                        relatorios_ultima_rodada = []
                        state_manager.turn = 1
                    state_manager.next_turn()
                elif escolha == "2":
                    SquadScene(clube).mostrar_escalacao(modo_grafico=modo_grafico)
                elif escolha == "3":
                    TransferScene(clubes_obj, clube).menu(modo_grafico=modo_grafico)
                elif escolha == "4":
                    FinanceScene(clube).menu(modo_grafico=modo_grafico)
                elif escolha == "5":
                    # Exibe os relatórios da última rodada
                    if not relatorios_ultima_rodada:
                        if not modo_grafico:
                            print("Nenhuma rodada simulada ainda.")
                        else:
                            mostrar_relatorio_partida("Nenhuma rodada simulada ainda.", modo_grafico=True)
                    else:
                        if not modo_grafico:
                            print("\nRelatórios da última rodada:")
                            for rel in relatorios_ultima_rodada:
                                print(rel)
                                print("-"*40)
                        else:
                            for rel in relatorios_ultima_rodada:
                                mostrar_relatorio_partida(rel, modo_grafico=True)
                elif escolha == "7":
                    # Exibe ranking de artilheiros (função utilitária)
                    from utils.helpers import mostrar_ranking_artilheiros
                    ranking = sorted(campeonato.gols_jogadores.items(), key=lambda x: -x[1])
                    mostrar_ranking_artilheiros(ranking, modo_grafico=modo_grafico)
                elif escolha == "8":
                    # Exibe a tabela real do campeonato
                    tabela_ordenada = sorted(campeonato.tabela.items(), key=lambda x: (-x[1]["pontos"], -(x[1]["gp"]-x[1]["gc"]), -x[1]["gp"]))
                    tabela = [(clube, stats) for clube, stats in tabela_ordenada]
                    if modo_grafico:
                        mostrar_tabela_campeonato_pygame(tabela, nome_campeonato=campeonato.nome)
                    else:
                        from utils.drawer import mostrar_tabela_campeonato
                        mostrar_tabela_campeonato(tabela)
                    from data.save_load import salvar_jogo_completo
                    salvar_jogo_completo(state_manager, campeonato, relatorios_ultima_rodada)
                elif escolha == "9":
                    state_manager.set_state("main_menu")
            elif state == "season_over":
                opcoes_fim = ["Voltar ao menu principal"]
                escolha = menu("Temporada Encerrada", opcoes_fim)
                if escolha == "1":
                    state_manager.reset()
            else:
                if not modo_grafico:
                    print(f"[Estado desconhecido: {state}]")
                state_manager.stop()
    finally:
        if modo_grafico:
            import pygame
            pygame.quit()
