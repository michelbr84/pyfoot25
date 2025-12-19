# Testes para Match
import unittest
from entities.club import Club
from entities.player import Player
from entities.match import Match

class TestMatch(unittest.TestCase):
    def test_simulacao_basica(self):
        c1 = Club("Time A", "Cidade", [Player("A1", "Atacante", 80)])
        c2 = Club("Time B", "Cidade", [Player("B1", "Atacante", 70)])
        m = Match(c1, c2)
        m.simular()
        self.assertIn(m.gols_casa, [0, 1, 2, 3])
        self.assertIn(m.gols_fora, [0, 1, 2, 3])
        self.assertIsInstance(m.relatorio(), str)

if __name__ == "__main__":
    unittest.main()
