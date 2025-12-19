# Entidade Jogador (Player)

class Player:
    def contrato_expirado(self):
        """Retorna True se o contrato do jogador está expirado (0 anos)."""
        return getattr(self, 'contrato_restante', 1) <= 0
    def __init__(self, nome, posicao, forca, status="apto", salario=None, contrato_restante=None):
        self.nome = nome
        self.posicao = posicao
        self.forca = forca
        self.status = status  # "apto", "lesionado", "suspenso"
        self.cartoes_amarelos = 0
        self.cartoes_vermelhos = 0
        self.tempo_lesao = 0  # rodadas
        self.tempo_suspensao = 0  # rodadas
        self.morale = 100  # Morale starts at 100 (max value)
        self.injury_duration = 0  # Number of matches the player is injured
        self.yellow_cards = 0  # Number of yellow cards
        self.red_card = False  # Whether the player has a red card
        # Novos atributos para Elifoot-like
        self.salario = salario if salario is not None else max(1000, forca * 50)  # Exemplo: 50 por ponto de forca
        self.contrato_restante = contrato_restante if contrato_restante is not None else 3  # 3 temporadas padrão

    def lesionar(self, rodadas):
        self.status = "lesionado"
        self.tempo_lesao = rodadas

    def suspender(self, rodadas):
        self.status = "suspenso"
        self.tempo_suspensao = rodadas

    def aplicar_cartao_amarelo(self):
        self.cartoes_amarelos += 1
        if self.cartoes_amarelos >= 3:
            self.suspender(1)
            self.cartoes_amarelos = 0

    def aplicar_cartao_vermelho(self):
        self.cartoes_vermelhos += 1
        self.suspender(2)

    def recuperar(self):
        self.status = "apto"
        self.tempo_lesao = 0
        self.tempo_suspensao = 0

    def avancar_turno(self):
        if self.status == "lesionado":
            self.tempo_lesao -= 1
            if self.tempo_lesao <= 0:
                self.recuperar()
        elif self.status == "suspenso":
            self.tempo_suspensao -= 1
            if self.tempo_suspensao <= 0:
                self.recuperar()

    def adjust_morale(self, change):
        """Adjust the player's morale by a given amount."""
        self.morale = max(0, min(100, self.morale + change))

    def set_injury(self, duration):
        """Set the player as injured for a given number of matches."""
        self.injury_duration = duration

    def recover_from_injury(self):
        """Reduce injury duration by one match."""
        if self.injury_duration > 0:
            self.injury_duration -= 1

    def add_yellow_card(self):
        """Add a yellow card to the player."""
        self.yellow_cards += 1

    def reset_yellow_cards(self):
        """Reset the player's yellow cards."""
        self.yellow_cards = 0

    def give_red_card(self):
        """Give the player a red card."""
        self.red_card = True

    def reset_red_card(self):
        """Reset the player's red card status."""
        self.red_card = False

    def info(self):
        return f"{self.nome} ({self.posicao}) - Força: {self.forca} - Status: {self.status} - Salário: R${self.salario}/semana - Contrato: {self.contrato_restante} anos"
