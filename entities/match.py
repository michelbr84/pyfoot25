# Simulação de Partidas e Relatório de Jogo
import random
from entities.player import Player

class Match:
    def __init__(self, clube_casa, clube_fora):
        self.clube_casa = clube_casa
        self.clube_fora = clube_fora
        self.gols_casa = 0
        self.gols_fora = 0
        self.eventos = []
        self.goleadores = []  # lista de tuplas (Player, Club)

    def simular(self):
        forca_casa = sum(j.forca for j in self.clube_casa.elenco if j.status == "apto")
        forca_fora = sum(j.forca for j in self.clube_fora.elenco if j.status == "apto")
        # Vantagem de jogar em casa
        forca_casa += 5

        # Sorteio de gols
        self.gols_casa = self._sortear_gols(forca_casa, forca_fora)
        self.gols_fora = self._sortear_gols(forca_fora, forca_casa)

        # Sorteio dos autores dos gols
        aptos_casa = [j for j in self.clube_casa.elenco if j.status == "apto"]
        aptos_fora = [j for j in self.clube_fora.elenco if j.status == "apto"]
        for _ in range(self.gols_casa):
            if aptos_casa:
                artilheiro = random.choice(aptos_casa)
                self.goleadores.append((artilheiro, self.clube_casa))
                self.eventos.append(f"Gol de {artilheiro.nome} ({self.clube_casa.nome})!")
        for _ in range(self.gols_fora):
            if aptos_fora:
                artilheiro = random.choice(aptos_fora)
                self.goleadores.append((artilheiro, self.clube_fora))
                self.eventos.append(f"Gol de {artilheiro.nome} ({self.clube_fora.nome})!")

        # Eventos: cartões, lesões
        self._sortear_eventos(self.clube_casa, "casa")
        self._sortear_eventos(self.clube_fora, "fora")

    def _sortear_gols(self, ataque, defesa):
        # Algoritmo simples: mais força, mais chance de gols
        base = max(1, ataque // 100)
        variacao = random.randint(0, base)
        return variacao

    def _sortear_eventos(self, clube, lado):
        for jogador in clube.elenco:
            if jogador.injury_duration > 0:
                continue  # Pular jogadores lesionados

            # Cartão amarelo: 10% de chance
            if random.random() < 0.10:
                jogador.add_yellow_card()
                self.eventos.append(f"{jogador.nome} ({clube.nome}) recebeu cartão amarelo.")
                # Verificar suspensão por cartões amarelos acumulados
                if jogador.yellow_cards >= 2:
                    jogador.give_red_card()
                    self.eventos.append(f"{jogador.nome} ({clube.nome}) está suspenso devido a cartões amarelos acumulados.")

            # Cartão vermelho: 2% de chance
            if random.random() < 0.02:
                jogador.give_red_card()
                self.eventos.append(f"{jogador.nome} ({clube.nome}) foi expulso com cartão vermelho.")

            # Lesão: 3% de chance
            if random.random() < 0.03:
                injury_duration = random.randint(1, 4)
                jogador.set_injury(injury_duration)
                self.eventos.append(f"{jogador.nome} ({clube.nome}) está lesionado por {injury_duration} partidas.")

            # Ajustar moral com base nos eventos
            if jogador.red_card:
                jogador.adjust_morale(-20)  # Diminuir moral por cartão vermelho
            elif jogador.yellow_cards > 0:
                jogador.adjust_morale(-5)  # Pequena diminuição da moral por cartão amarelo
            else:
                jogador.adjust_morale(5)  # Aumentar moral por ausência de eventos negativos

    def relatorio(self):
        texto = [
            f"{self.clube_casa.nome} {self.gols_casa} x {self.gols_fora} {self.clube_fora.nome}",
            "Eventos do jogo:"
        ]
        if self.eventos:
            texto.extend(self.eventos)
        else:
            texto.append("Sem grandes acontecimentos.")
        return "\n".join(texto)
