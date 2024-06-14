from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome, self.data_nascimento, self.cpf = nome, data_nascimento, cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo, self._numero, self._agencia, self._cliente = 0, numero, "0001", cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero): return cls(numero, cliente)

    @property
    def saldo(self): return self._saldo
    @property
    def numero(self): return self._numero
    @property
    def agencia(self): return self._agencia
    @property
    def cliente(self): return self._cliente
    @property
    def historico(self): return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print("\nTá sem saldo, vá depositar e me alimente!!")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado, obrigado :)")
            return True
        else:
            print("\nTem algo errado aí, acho que tá invalido!")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nObrigado pela grana!")
            return True
        else:
            print("\nValor invalido, meu nobre")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite, self.limite_saques = limite, limite_saques

    def sacar(self, valor):
        saques_realizados = len([t for t in self.historico.transacoes if t['tipo'] == 'Saque'])
        if valor > (self.saldo + self.limite):
            print("\nTem saldo nãi irmãozinho...")
        elif saques_realizados >= self.limite_saques:
            print("\nJá sacou demais hoje, não?")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

    def __str__(self):
        return "\n".join([f"{t['tipo']}:\tR$ {t['valor']:.2f}\t{t['data']}" for t in self.transacoes])

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self): pass

    @abstractmethod
    def registrar(self, conta): pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self): return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

import textwrap

def menu():
    return input(textwrap.dedent("""\n
    ================ MENU ================
    [1]  Depositar
    [2]  Sacar
    [3]  Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [0]  Sair
    => """))

def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nO cliente não tem conta, Crie uma agora! Isso é uma ordem")
        return None
    return cliente.contas[0]

def depositar(clientes):
    cliente = filtrar_cliente(input("Informe o CPF do cliente: "), clientes)
    if not cliente:
        print("\nNão encontrei, tente outro")
        return

    valor = float(input("Informe o valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))

def sacar(clientes):
    cliente = filtrar_cliente(input("Informe o CPF do cliente: "), clientes)
    if not cliente:
        print("\nNão achei :(")
        return

    valor = float(input("Informe o valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))

def exibir_extrato(clientes):
    cliente = filtrar_cliente(input("Informe o CPF do cliente: "), clientes)
    if not cliente:
        print("\nMano, tu colocou o bagulho certo?")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        print("\n============== EXTRATO ==============")
        print("Sem movimentações." if not conta.historico.transacoes else conta.historico)
        print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    if filtrar_cliente((cpf := input("Informe o CPF (somente número): ")), clientes):
        print("\nQuer clonar, é???")
        return

    cliente = PessoaFisica(
        nome=input("Informe o nome completo: "),
        data_nascimento=input("Informe a data de nascimento (dd-mm-aaaa): "),
        cpf=cpf,
        endereco=input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    )
    clientes.append(cliente)
    print("\nCRIADO!!!!")

def criar_conta(numero_conta, clientes, contas):
    cliente = filtrar_cliente(input("Informe o CPF do cliente: "), clientes)
    if not cliente:
        print("\nCliente demasiado extinto")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\nCRIOUUUU")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes, contas = [], []
    while (opcao := menu()) != "0":
        if opcao == "1": depositar(clientes)
        elif opcao == "2": sacar(clientes)
        elif opcao == "3": exibir_extrato(clientes)
        elif opcao == "4": criar_cliente(clientes)
        elif opcao == "5": criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "6": listar_contas(contas)
        else: print("\nImbecil")

main()
