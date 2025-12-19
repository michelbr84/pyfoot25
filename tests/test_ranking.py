# Teste para ranking de artilheiros
import unittest
from entities.player import Player
from entities.club import Club
from entities.match import Match
from core.game import Campeonato

class TestRankingArtilheiros(unittest.TestCase):
    def test_ranking_artilheiros(self):
        # Cria clubes e jogadores
        p1 = Player("Pedro", "Atacante", 85)
        p2 = Player("Arrascaeta", "Meia", 87)
        p3 = Player("Endrick", "Atacante", 82)
        c1 = Club("Flamengo", "Rio", [p1, p2])
        c2 = Club("Palmeiras", "SP", [p3])
        campeonato = Campeonato("Teste", [c1, c2])
        # Simula partida com gols
        partida = Match(c1, c2)
        partida.gols_casa = 2
        partida.gols_fora = 1
        partida.goleadores = [(p1, c1), (p2, c1), (p3, c2)]
        for artilheiro, clube in partida.goleadores:
            chave = (artilheiro.nome, clube.nome)
            campeonato.gols_jogadores[chave] = campeonato.gols_jogadores.get(chave, 0) + 1
        ranking = sorted(campeonato.gols_jogadores.items(), key=lambda x: -x[1])
        self.assertEqual(ranking[0][0][0], "Pedro")
        self.assertEqual(ranking[0][1], 1)
        self.assertEqual(len(ranking), 3)

if __name__ == "__main__":
    unittest.main()
