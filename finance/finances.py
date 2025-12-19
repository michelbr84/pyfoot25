# Gestão Financeira do Clube

class Finances:
    def __init__(self, saldo_inicial=10000000):
        self.saldo = saldo_inicial
        self.receitas = []
        self.despesas = []

    def registrar_receita(self, valor, descricao=""):
        self.saldo += valor
        self.receitas.append((valor, descricao))

    def registrar_despesa(self, valor, descricao=""):
        self.saldo -= valor
        self.despesas.append((valor, descricao))

    def relatorio(self):
        texto = [f"Saldo atual: R${self.saldo}"]
        texto.append("Receitas:")
        for valor, desc in self.receitas:
            texto.append(f"  +R${valor} - {desc}")
        texto.append("Despesas:")
        for valor, desc in self.despesas:
            texto.append(f"  -R${valor} - {desc}")
        return "\n".join(texto)
