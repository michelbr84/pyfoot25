# Testes para TransferMarket
import unittest
from entities.club import Club
from entities.player import Player
from entities.transfer import TransferMarket

class TestTransferMarket(unittest.TestCase):
    def test_compra_jogador(self):
        c1 = Club("Vendedor", "Cidade", [Player("P1", "Atacante", 80)], caixa=1000)
        c2 = Club("Comprador", "Cidade", [], caixa=2000)
        clubes = {c1.nome: c1, c2.nome: c2}
        market = TransferMarket(clubes)
        market.comprar_jogador(c2, 0, 500)
        self.assertEqual(len(c1.elenco), 0)
        self.assertEqual(len(c2.elenco), 1)
        self.assertEqual(c1.caixa, 1500)
        self.assertEqual(c2.caixa, 1500)

if __name__ == "__main__":
    unittest.main()
