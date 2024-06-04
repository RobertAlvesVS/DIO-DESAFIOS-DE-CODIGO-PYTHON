#Implementar 3 operações Deposito, Saque, Extrato
#Deposito -> So valores positivos, todo deposito deve ser guardado em extrato
#Saque -> So pode realizar 3 saques e cada um com limite de 500 PILA, caso não tenha saldo em conta deve exibir uma mensagem que não tem dinheiro todos os saques, todo saque deve ir para extrato
#Extrato -> O Estrato deve ser mostrado como R$ xxx.xx
#Criar_Usuario -> o programa deve amarzenar os usuarios em uma lista, um usuario e composto por nome, data de nascimento, cpf e endereço
#Logradouro, NRO - bairro - cidade/sigla estado deve ser amazenado somente os numeros do cpf não podendo ter o mesmo cpf


def menu():
    return input("""
    Bem-Vindo ao Banco Digital DOS/CMD
    Por favor entre com uma das opções abaixo

    [1] Depósito
    [2] Saque
    [3] Extrato
    [4] Criar Usuario
    [5] Criar Conta
    [0] Sair
    """)

def criar_usuario(usuarios):
    cpf = input("Informe o seu CPF apenas numeros")
    
    usuario = procura_usuario(cpf, usuarios)
    
    if usuario:
        return print("Já existe alguem com esse CPF, tá querendo clonar é?")
    
    nome = input("Digite seu nome: ")
    data_nascimento = input("Informe sua data de nascimento (dia/mês/ano): ")
    endereco = input("Informe seu endereço (logradouro, numero - bairro - cidade/sigla estado): ")
    
    usuarios.append({"CPF": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})
    
    print("Usuario criado com sucesso!")
    
def procura_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["CPF"] == cpf:
            return usuario
        
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Digite seu CPF apenas numero")
    
    usuario = procura_usuario(cpf, usuarios)
    if usuario:
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print(f"Conta {numero_conta} de {usuario['nome']} criada com sucesso!")
        numero_conta += 1
        return numero_conta
    else:
        print("Tu colocou o CPF errado, não?")
        
def deposito(saldo, extrato, /):
    print("Você escolheu a opção Depósito")
    deposito = input("Qual a quantidade que deseja depositar?\n")

    if deposito.isalpha() == False:
        deposito = float(deposito)

        if (deposito > 0):
            saldo += deposito
            print(f"Depósito de R$ {deposito:.2f} efetuado com Sucesso!")
            extrato.append(f"Foi depósitado um valor de R$ {deposito:.2f}")
        else:
            print("Valor negativo? Quer tirar, vá para o Saque, imbecil")
    else:
        print("Detectei uma letra, por favor repita a operação!")
    
    return saldo

def sacar(*, saldo, extrato, limite_saque):
    if limite_saque <= 0:
        print("Você já sacou muitas vezes hoje!")
    else:
        print("Você escolheu a opção Saque")
        saque = input("Quanto deseja sacar? Lembre-se que tem o limite de R$ 500.00\n")

        if saque.isalpha() == False:
            saque = float(saque)
            
            if saque > 500:
                print("Você não leu não? Limite de R$ 500.00")
            elif saque > saldo:
                print("Tá querendo me roubar? Você não tem esse saldo todo não, pode voltar!")
            elif saque <= 0:
                print("Eu sei que eu falei que valor negativo é em saque, mas coloque um valor positivo aí!")
            else:
                saldo -= saque
                limite_saque -= 1
                print("Saque efetuado com sucesso!")
                extrato.append(f"Foi sacado um valor de R$ {saque:.2f}")
        else:
            print("Detectei uma letra, por favor repita a operação!")
            
    return saldo, limite_saque

def historico(saldo, /, *, extrato):
    if not extrato:
        return print("Você ainda não mexeu na sua conta, vai lá depositar :) me alimente com seu capitalismo >:)")
    
    print("Extrato de transações:")
    for inf in extrato:
        print(inf)
    print(f"Seu saldo atual é de R$ {saldo:.2f}")
    


def main():
    
    saldo = 0
    extrato = []
    limite_saque = 3
    usuarios = []
    contas = []
    AGENCIA = "0001"
    numero_conta = 1
    
    while True:
    
        escolha = menu()

        if escolha == "1":
            saldo = deposito(saldo, extrato)
        elif escolha == "2":
            saldo, limite_saque = sacar(saldo=saldo, extrato=extrato, limite_saque=limite_saque)
        elif escolha == "3":
            historico(saldo, extrato=extrato)
        elif escolha == "4":
            criar_usuario(usuarios)
        elif escolha == "5":
            numero_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
        elif escolha == "0":
            print("Obrigado por utilizar nossos serviços! ")
            break
        else:
            print("Opção inválida seu cabaço")
            
main()
