# Gerenciador de Estados do Jogo

class StateManager:
    def __init__(self, jogadores=None):
        self.state = "main_menu"  # Estado inicial
        self.running = True
        self.turn = 1
        self.max_turns = 38  # Exemplo: 38 rodadas
        self.jogadores = jogadores if jogadores else []  # Lista de nomes ou objetos dos jogadores
        self.jogador_atual_idx = 0 if self.jogadores else None

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

    def next_turn(self):
        # Avança para o próximo jogador no modo multiplayer
        if self.jogadores:
            self.jogador_atual_idx = (self.jogador_atual_idx + 1) % len(self.jogadores)
            # Só avança rodada se todos jogaram
            if self.jogador_atual_idx == 0:
                self.turn += 1
        else:
            self.turn += 1
        if self.turn > self.max_turns:
            self.set_state("season_over")

    def get_jogador_atual(self):
        if self.jogadores:
            return self.jogadores[self.jogador_atual_idx]
        return None

    def reset(self):
        self.state = "main_menu"
        self.turn = 1
        self.running = True
        self.jogador_atual_idx = 0 if self.jogadores else None

    def stop(self):
        self.running = False
