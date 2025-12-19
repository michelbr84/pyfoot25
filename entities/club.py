# Entidade Clube (Club)
from entities.player import Player

class Club:
    def __init__(self, nome, cidade, jogadores=None, caixa=10000000, estadio=None):
        self.nome = nome
        self.cidade = cidade
        self.caixa = caixa  # Dinheiro em caixa
        self.estadio = estadio or {"nome": f"Estádio do {nome}", "capacidade": 20000}
        self.elenco = jogadores if jogadores is not None else []  # Lista de Player

    def adicionar_jogador(self, jogador):
        self.elenco.append(jogador)

    def remover_jogador(self, jogador):
        if jogador in self.elenco:
            self.elenco.remove(jogador)

    def movimentar_caixa(self, valor):
        self.caixa += valor

    def info(self):
        return f"{self.nome} ({self.cidade}) - Caixa: R${self.caixa} - Estádio: {self.estadio['nome']} ({self.estadio['capacidade']} lugares)"

    def mostrar_elenco(self):
        print(f"Elenco do {self.nome}:")
        for jogador in self.elenco:
            print("-", jogador.info())

    def atualizar_estadio(self, novo_nome=None, nova_capacidade=None):
        if novo_nome:
            self.estadio["nome"] = novo_nome
        if nova_capacidade:
            self.estadio["capacidade"] = nova_capacidade
