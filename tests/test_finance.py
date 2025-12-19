# Testes para Finances
import unittest
from finance.finances import Finances

class TestFinances(unittest.TestCase):
    def test_receita_despesa(self):
        f = Finances(1000)
        f.registrar_receita(500, "Patrocínio")
        f.registrar_despesa(200, "Salário")
        self.assertEqual(f.saldo, 1300)
        self.assertIn((500, "Patrocínio"), f.receitas)
        self.assertIn((200, "Salário"), f.despesas)

if __name__ == "__main__":
    unittest.main()
