# Cena de Elenco e Escalação
from entities.club import Club
from entities.player import Player


class SquadScene:
    def __init__(self, clube):
        self.clube = clube
        # Exemplo de formação: 4-4-2 (4 def, 4 mei, 2 ata, 1 gol)
        self.formacao = ["Goleiro", "Zagueiro", "Zagueiro", "Lateral", "Lateral", "Meia", "Meia", "Meia", "Meia", "Atacante", "Atacante"]
        self.titulares = self._escalar_titulares()
        # Reservas: apenas jogadores com contrato > 0
        self.reservas = [j for j in self.clube.elenco if j not in self.titulares and not getattr(j, 'contrato_expirado', lambda: False)()]

    def _escalar_titulares(self):
        titulares = []
        usados = set()
        for pos in self.formacao:
            for jogador in self.clube.elenco:
                # Não escala jogadores com contrato zerado
                if jogador.posicao == pos and jogador not in usados and jogador.status == "apto" and getattr(jogador, 'contrato_restante', 1) > 0:
                    titulares.append(jogador)
                    usados.add(jogador)
                    break
            else:
                # Se não achar, pega qualquer apto com contrato
                for jogador in self.clube.elenco:
                    if jogador not in usados and jogador.status == "apto" and getattr(jogador, 'contrato_restante', 1) > 0:
                        titulares.append(jogador)
                        usados.add(jogador)
                        break
        return titulares

    def mostrar_escalacao(self, modo_grafico=False):
        if not modo_grafico:
            print(f"\n[Escalação do {self.clube.nome} - Formação: {self.formacao}]")
            for i, jogador in enumerate(self.titulares):
                print(f"{i+1}. {jogador.info()}" + (" [CONTRATO EXPIRADO]" if getattr(jogador, 'contrato_expirado', lambda: False)() else ""))
            print("\nReservas:")
            for i, jogador in enumerate(self.reservas):
                print(f"{i+1}. {jogador.info()}" + (" [CONTRATO EXPIRADO]" if getattr(jogador, 'contrato_expirado', lambda: False)() else ""))
            # Listar jogadores com contrato expirado
            expirados = [j for j in self.clube.elenco if getattr(j, 'contrato_expirado', lambda: False)()]
            if expirados:
                print("\nJogadores com contrato expirado (não podem jogar):")
                for j in expirados:
                    print(f"- {j.nome} ({j.posicao})")
            input("Pressione Enter para voltar...")
        else:
            import pygame
            pygame.init()
            largura, altura = 700, 600
            tela = pygame.display.set_mode((largura, altura))
            pygame.display.set_caption(f"Elenco - {self.clube.nome}")
            fonte = pygame.font.SysFont(None, 32)
            fonte_titulo = pygame.font.SysFont(None, 40)
            cor_fundo = (20, 40, 60)
            cor_texto = (255, 255, 255)
            cor_titular = (60, 180, 60)
            cor_reserva = (180, 60, 60)
            cor_editar = (255, 215, 0)
            clock = pygame.time.Clock()
            rodando = True
            editar_idx = None  # (tipo, idx) tipo: 'titular'/'reserva'
            input_salario = ''
            input_contrato = ''
            input_ativo = False
            while rodando:
                tela.fill(cor_fundo)
                titulo = fonte_titulo.render(f"Elenco do {self.clube.nome}", True, cor_texto)
                tela.blit(titulo, (largura//2 - titulo.get_width()//2, 20))
                # Titulares
                y = 80
                tela.blit(fonte.render("Titulares:", True, cor_titular), (60, y))
                y += 30
                cabecalho = fonte.render("#  Nome                 Força  Salário      Contrato", True, cor_texto)
                tela.blit(cabecalho, (80, y))
                y += 28
                btns_editar = []
                for i, jogador in enumerate(self.titulares):
                    # Destacar se contrato expirando
                    cor_nome = (255,80,80) if jogador.contrato_restante <= 1 else cor_texto
                    txt = fonte.render(f"{i+1:>2}. {jogador.nome:<18} {jogador.forca:>3}   R${jogador.salario:>6}   {jogador.contrato_restante} anos", True, cor_nome)
                    tela.blit(txt, (80, y))
                    # Aviso de expiração
                    if jogador.contrato_restante <= 1:
                        aviso = fonte.render("!", True, (255,80,80))
                        tela.blit(aviso, (520, y))
                    # Botão editar
                    btn_rect = pygame.Rect(540, y, 80, 24)
                    pygame.draw.rect(tela, cor_editar, btn_rect, border_radius=6)
                    txt_btn = fonte.render("Editar", True, (60,60,60))
                    tela.blit(txt_btn, (btn_rect.x+8, btn_rect.y+2))
                    btns_editar.append(('titular', i, btn_rect))
                    y += 28
                # Reservas
                y += 20
                tela.blit(fonte.render("Reservas:", True, cor_reserva), (60, y))
                y += 30
                cabecalho_res = fonte.render("#  Nome                 Força  Salário      Contrato", True, cor_texto)
                tela.blit(cabecalho_res, (80, y))
                y += 28
                for i, jogador in enumerate(self.reservas):
                    cor_nome = (255,80,80) if jogador.contrato_restante <= 1 else cor_texto
                    txt = fonte.render(f"{i+1:>2}. {jogador.nome:<18} {jogador.forca:>3}   R${jogador.salario:>6}   {jogador.contrato_restante} anos", True, cor_nome)
                    tela.blit(txt, (80, y))
                    if jogador.contrato_restante <= 1:
                        aviso = fonte.render("!", True, (255,80,80))
                        tela.blit(aviso, (520, y))
                    btn_rect = pygame.Rect(540, y, 80, 24)
                    pygame.draw.rect(tela, cor_editar, btn_rect, border_radius=6)
                    txt_btn = fonte.render("Editar", True, (60,60,60))
                    tela.blit(txt_btn, (btn_rect.x+8, btn_rect.y+2))
                    btns_editar.append(('reserva', i, btn_rect))
                    y += 28
                # Aviso geral de contratos expirando
                contratos_exp = [j for j in self.titulares+self.reservas if j.contrato_restante <= 1]
                if contratos_exp:
                    aviso_txt = fonte.render(f"Atenção: {len(contratos_exp)} contrato(s) expirando!", True, (255,80,80))
                    tela.blit(aviso_txt, (largura//2 - aviso_txt.get_width()//2, 60))
                # Botão voltar
                botao_rect = pygame.Rect(largura//2 - 60, altura - 70, 120, 40)
                pygame.draw.rect(tela, (80, 80, 200), botao_rect)
                botao_txt = fonte.render("Voltar", True, (255,255,255))
                tela.blit(botao_txt, (botao_rect.x + 20, botao_rect.y + 5))
                # Modal de edição
                if editar_idx is not None:
                    # Modal fundo
                    pygame.draw.rect(tela, (30,30,30), (largura//2-180, altura//2-100, 360, 180), border_radius=12)
                    pygame.draw.rect(tela, cor_editar, (largura//2-180, altura//2-100, 360, 180), 3, border_radius=12)
                    tipo, idx = editar_idx
                    jogador = self.titulares[idx] if tipo=='titular' else self.reservas[idx]
                    tela.blit(fonte_titulo.render("Editar Contrato", True, cor_editar), (largura//2-100, altura//2-90))
                    tela.blit(fonte.render(f"Nome: {jogador.nome}", True, cor_texto), (largura//2-160, altura//2-40))
                    # Salário
                    tela.blit(fonte.render("Salário (R$):", True, cor_texto), (largura//2-160, altura//2))
                    pygame.draw.rect(tela, (255,255,255), (largura//2-10, altura//2, 100, 32), border_radius=6)
                    salario_str = input_salario if input_ativo else str(jogador.salario)
                    tela.blit(fonte.render(salario_str, True, (0,0,0)), (largura//2, altura//2))
                    # Contrato
                    tela.blit(fonte.render("Contrato (anos):", True, cor_texto), (largura//2-160, altura//2+40))
                    pygame.draw.rect(tela, (255,255,255), (largura//2+60, altura//2+40, 40, 32), border_radius=6)
                    contrato_str = input_contrato if input_ativo else str(jogador.contrato_restante)
                    tela.blit(fonte.render(contrato_str, True, (0,0,0)), (largura//2+65, altura//2+40))
                    # Botões salvar/cancelar
                    btn_salvar = pygame.Rect(largura//2-60, altura//2+90, 80, 32)
                    btn_cancelar = pygame.Rect(largura//2+40, altura//2+90, 80, 32)
                    pygame.draw.rect(tela, (60,180,60), btn_salvar, border_radius=6)
                    pygame.draw.rect(tela, (180,60,60), btn_cancelar, border_radius=6)
                    tela.blit(fonte.render("Salvar", True, (255,255,255)), (btn_salvar.x+10, btn_salvar.y+4))
                    tela.blit(fonte.render("Cancelar", True, (255,255,255)), (btn_cancelar.x+4, btn_cancelar.y+4))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if editar_idx is not None:
                            # Modal ativo
                            if btn_salvar.collidepoint(event.pos):
                                # Salvar alterações
                                try:
                                    novo_salario = int(salario_str)
                                    novo_contrato = int(contrato_str)
                                    if novo_salario < 0 or novo_contrato < 1:
                                        raise ValueError
                                    if tipo=='titular':
                                        self.titulares[idx].salario = novo_salario
                                        self.titulares[idx].contrato_restante = novo_contrato
                                    else:
                                        self.reservas[idx].salario = novo_salario
                                        self.reservas[idx].contrato_restante = novo_contrato
                                    editar_idx = None
                                    input_ativo = False
                                except Exception:
                                    # Valor inválido, apenas ignore
                                    pass
                            elif btn_cancelar.collidepoint(event.pos):
                                editar_idx = None
                                input_ativo = False
                        else:
                            if botao_rect.collidepoint(event.pos):
                                rodando = False
                            for tipo, idx, btn_rect in btns_editar:
                                if btn_rect.collidepoint(event.pos):
                                    editar_idx = (tipo, idx)
                                    input_salario = ''
                                    input_contrato = ''
                                    input_ativo = True
                    if event.type == pygame.KEYDOWN and editar_idx is not None and input_ativo:
                        if event.key == pygame.K_TAB:
                            # Alternar campo
                            if input_salario == '':
                                input_salario = salario_str
                                input_contrato = ''
                            else:
                                input_contrato = contrato_str
                                input_salario = ''
                        elif event.key == pygame.K_RETURN:
                            # Tenta salvar
                            try:
                                novo_salario = int(salario_str)
                                novo_contrato = int(contrato_str)
                                if novo_salario < 0 or novo_contrato < 1:
                                    raise ValueError
                                tipo, idx = editar_idx
                                if tipo=='titular':
                                    self.titulares[idx].salario = novo_salario
                                    self.titulares[idx].contrato_restante = novo_contrato
                                else:
                                    self.reservas[idx].salario = novo_salario
                                    self.reservas[idx].contrato_restante = novo_contrato
                                editar_idx = None
                                input_ativo = False
                            except Exception:
                                pass
                        elif event.key == pygame.K_ESCAPE:
                            editar_idx = None
                            input_ativo = False
                        elif event.key == pygame.K_BACKSPACE:
                            if input_salario != '':
                                input_salario = input_salario[:-1]
                            elif input_contrato != '':
                                input_contrato = input_contrato[:-1]
                        elif event.unicode.isdigit():
                            if input_salario == '':
                                input_salario += event.unicode
                            else:
                                input_contrato += event.unicode
                pygame.display.flip()
                clock.tick(30)
            return

    def trocar_jogador(self, idx_titular, idx_reserva):
        if 0 <= idx_titular < len(self.titulares) and 0 <= idx_reserva < len(self.reservas):
            self.titulares[idx_titular], self.reservas[idx_reserva] = self.reservas[idx_reserva], self.titulares[idx_titular]
            print(f"Troca realizada: {self.titulares[idx_titular].nome} entrou como titular.")
        else:
            print("Índices inválidos para troca.")

    def definir_formacao(self, nova_formacao):
        self.formacao = nova_formacao
        self.titulares = self._escalar_titulares()
        self.reservas = [j for j in self.clube.elenco if j not in self.titulares]
