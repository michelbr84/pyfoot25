# Testes para Player
import unittest
from entities.player import Player

class TestPlayer(unittest.TestCase):
    def test_criacao(self):
        p = Player("Pedro", "Atacante", 85)
        self.assertEqual(p.nome, "Pedro")
        self.assertEqual(p.posicao, "Atacante")
        self.assertEqual(p.forca, 85)
        self.assertEqual(p.status, "apto")

    def test_lesao_e_recuperacao(self):
        p = Player("Pedro", "Atacante", 85)
        p.lesionar(2)
        self.assertEqual(p.status, "lesionado")
        p.avancar_turno()
        p.avancar_turno()
        self.assertEqual(p.status, "apto")

    def test_cartoes(self):
        p = Player("Pedro", "Atacante", 85)
        for _ in range(3):
            p.aplicar_cartao_amarelo()
        self.assertEqual(p.status, "suspenso")
        p.recuperar()
        p.aplicar_cartao_vermelho()
        self.assertEqual(p.status, "suspenso")

if __name__ == "__main__":
    unittest.main()
