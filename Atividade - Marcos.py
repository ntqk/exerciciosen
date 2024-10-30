from datetime import datetime
import pytz
from random import randint

class ContaCorrente:
    def __init__(self, nome, cpf, agencia, num_conta):
        self.nome = nome
        self.cpf = cpf
        self.saldo = 0
        self.limite = -1000
        self.agencia = agencia
        self.num_conta = num_conta
        self.transacoes = []

    def consultar_saldo(self):
        print('Seu saldo atual é de R${:.2f}'.format(self.saldo))

    def depositar_dinheiro(self, valor):
        self.saldo += valor
        self.transacoes.append((valor, self.saldo, self._data_hora()))

    def _limite_conta(self):
        return self.limite

    def sacar_dinheiro(self, valor):
        if self.saldo - valor < self._limite_conta():
            print("Você não tem saldo suficiente para sacar esse valor")
            self.consultar_saldo()
        else:
            self.saldo -= valor
            self.transacoes.append((-valor, self.saldo, self._data_hora()))

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR.strftime('%d/%m/%Y %H:%M')

    def consultar_historico_transacoes(self):
        print('Histórico de Transações:')
        for i, transacao in enumerate(self.transacoes, start=1):
            valor, saldo, data_hora = transacao
            tipo_transacao = "Depósito" if valor > 0 else "Saque"
            print(f"Transação {i}: {tipo_transacao} de R${abs(valor):.2f} em {data_hora}. Saldo atual: R${saldo:.2f}")


class Agencia:
    def __init__(self, telefone, cnpj, numero):
        self.telefone = telefone
        self.cnpj = cnpj
        self.numero = numero
        self.clientes = []
        self.caixa = 0
        self.emprestimos = []

    def verificar_caixa(self):
        if self.caixa < 1000000:
            print("Caixa abaixo do nível recomendado. Caixa Atual: R${:.2f}".format(self.caixa))
        else:
            print("O valor de caixa está ok. Caixa Atual: R${:.2f}".format(self.caixa))

    def emprestar_dinheiro(self, valor, cpf, juros):
        if self.caixa > valor:
            self.emprestimos.append((valor, cpf, juros))
            self.caixa -= valor
            print("Empréstimo efetuado.")
        else:
            print("Empréstimo não é possível. Dinheiro insuficiente no caixa.")

    def adicionar_cliente(self, nome, cpf, patrimonio):
        self.clientes.append((nome, cpf, patrimonio))


class AgenciaVirtual(Agencia):
    def __init__(self, site, telefone, cnpj, numero=1888):
        self.site = site
        super().__init__(telefone, cnpj, numero)
        self.caixa_paypal = 0

    def depositar_paypal(self, valor):
        self.caixa += valor
        self.caixa_paypal += valor

    def sacar_paypal(self, valor):
        if self.caixa_paypal >= valor:
            self.caixa_paypal -= valor
            self.caixa += valor
        else:
            print("Saldo PayPal insuficiente.")


class AgenciaComum(Agencia):
    def __init__(self, telefone, cnpj):
        numero = randint(1001, 9999)
        super().__init__(telefone, cnpj, numero)
        self.caixa = 1000000


class AgenciaPremium(Agencia):
    def __init__(self, telefone, cnpj):
        numero = randint(1001, 9999)
        super().__init__(telefone, cnpj, numero)
        self.caixa = 10000000

    def adicionar_cliente(self, nome, cpf, patrimonio):
        if patrimonio > 1000000:
            super().adicionar_cliente(nome, cpf, patrimonio)
        else:
            print("Cliente não possui o patrimônio mínimo necessário.")


# Exemplos de uso:
conta_lira = ContaCorrente("Lira", "111.222.333-45", "1234", "56789")
conta_lira.depositar_dinheiro(10000)
conta_lira.sacar_dinheiro(1000)
conta_lira.consultar_historico_transacoes()

# Criação de agências
agencia_virtual = AgenciaVirtual("www.agenciavirtual.com.br", "22223333", "200000000")
agencia_virtual.caixa = 1000000
agencia_virtual.verificar_caixa()
agencia_virtual.depositar_paypal(20000)
print(agencia_virtual.caixa, agencia_virtual.caixa_paypal)

agencia_premium = AgenciaPremium("33333333", "3000000000000")
agencia_premium.adicionar_cliente("Lira", "11111111111", 1000000)
print(agencia_premium.clientes)