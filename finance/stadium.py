# Gestão do Estádio

class Stadium:
    def __init__(self, nome, capacidade=20000, nivel=1):
        self.nome = nome
        self.capacidade = capacidade
        self.nivel = nivel

    def upgrade(self):
        self.nivel += 1
        self.capacidade += 5000
        print(f"Estádio {self.nome} melhorado para nível {self.nivel}! Capacidade: {self.capacidade}")

    def receita_bilheteria(self, ingressos_vendidos, preco_medio):
        receita = ingressos_vendidos * preco_medio
        return receita
# Gestão do Estádio

class Stadium:
    def __init__(self, nome, capacidade=20000, nivel=1):
        self.nome = nome
        self.capacidade = capacidade
        self.nivel = nivel

    def upgrade(self):
        self.nivel += 1
        self.capacidade += 5000
        print(f"Estádio {self.nome} melhorado para nível {self.nivel}! Capacidade: {self.capacidade}")

    def receita_bilheteria(self, ingressos_vendidos, preco_medio):
        receita = ingressos_vendidos * preco_medio
        return receita
