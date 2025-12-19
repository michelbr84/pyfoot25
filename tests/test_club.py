# Testes para Club
import unittest
from entities.club import Club
from entities.player import Player

class TestClub(unittest.TestCase):
    def test_criacao(self):
        c = Club("Flamengo", "Rio")
        self.assertEqual(c.nome, "Flamengo")
        self.assertEqual(c.cidade, "Rio")
        self.assertTrue(isinstance(c.elenco, list))

    def test_adicionar_remover_jogador(self):
        c = Club("Flamengo", "Rio")
        p = Player("Pedro", "Atacante", 85)
        c.adicionar_jogador(p)
        self.assertIn(p, c.elenco)
        c.remover_jogador(p)
        self.assertNotIn(p, c.elenco)

    def test_movimentar_caixa(self):
        c = Club("Flamengo", "Rio", caixa=1000)
        c.movimentar_caixa(500)
        self.assertEqual(c.caixa, 1500)
        c.movimentar_caixa(-200)
        self.assertEqual(c.caixa, 1300)

if __name__ == "__main__":
    unittest.main()
