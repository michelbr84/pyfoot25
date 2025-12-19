# Sistema de Transferências e Leilão
from entities.player import Player

class TransferMarket:
    def __init__(self, clubes):
        self.clubes = clubes  # dict nome: Club
        self.jogadores_disponiveis = self._listar_jogadores_disponiveis()

    def _listar_jogadores_disponiveis(self):
        jogadores = []
        for clube in self.clubes.values():
            for jogador in clube.elenco:
                jogadores.append((clube, jogador))
        return jogadores

    def listar_jogadores(self):
        print("\nJogadores disponíveis para transferência:")
        for idx, (clube, jogador) in enumerate(self.jogadores_disponiveis):
            print(f"{idx+1}. {jogador.info()} - Clube: {clube.nome}")

    def comprar_jogador(self, comprador, idx_jogador, preco):
        if 0 <= idx_jogador < len(self.jogadores_disponiveis):
            clube_vendedor, jogador = self.jogadores_disponiveis[idx_jogador]
            if comprador.caixa >= preco:
                comprador.movimentar_caixa(-preco)
                clube_vendedor.movimentar_caixa(preco)
                clube_vendedor.remover_jogador(jogador)
                comprador.adicionar_jogador(jogador)
                print(f"{comprador.nome} comprou {jogador.nome} de {clube_vendedor.nome} por R${preco}!")
                self.jogadores_disponiveis.pop(idx_jogador)
            else:
                print("Saldo insuficiente!")
        else:
            print("Índice inválido!")

    def vender_jogador(self, vendedor, idx_jogador, comprador, preco):
        if 0 <= idx_jogador < len(vendedor.elenco):
            jogador = vendedor.elenco[idx_jogador]
            if comprador.caixa >= preco:
                comprador.movimentar_caixa(-preco)
                vendedor.movimentar_caixa(preco)
                vendedor.remover_jogador(jogador)
                comprador.adicionar_jogador(jogador)
                print(f"{vendedor.nome} vendeu {jogador.nome} para {comprador.nome} por R${preco}!")
            else:
                print("Comprador sem saldo!")
        else:
            print("Índice inválido!")
