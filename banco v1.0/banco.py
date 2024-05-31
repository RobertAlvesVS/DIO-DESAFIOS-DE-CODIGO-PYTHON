#Implementar 3 operações Deposito, Saque, Extrato
#Deposito -> So valores positivos, todo deposito deve ser guardado em extrato
#Saque -> So pode realizar 3 saques e cada um com limite de 500 PILA, caso não tenha saldo em conta deve exibir uma mensagem que não tem dinheiro todos os saques, todo saque deve ir para extrato
#Extrato -> O Estrato deve ser mostrado como R$ xxx.xx

menu = """
Bem-Vindo ao Banco Digital DOS/CMD
Por favor entre com uma das opções abaixo

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair
"""
saldo = 0
limite = 500
extrato = []
numero_saques = 0
limite_saque = 3

while True:
   
    escolha = input(menu)

    if escolha == "1":

        print("Você escolheu a opção Depósito")
        deposito = input("Qual a quantidade que deseja depositar?\n")

        if deposito.isalpha() == False:

            if (float(deposito) > 0):
                deposito = float(deposito)
                saldo += deposito
                print(f"Deposito de R$ {deposito:.2f} efetuado com Sucesso!")
                extrato.append(f"Foi depósitado um valor de R$ {float(deposito):.2f}")
            else:
                print("Valor negativo? Quer tirar vá para o Saque, imbecil")

        else:
            print("Detectei uma letra, por favor repita a operação!")
            continue

    elif escolha == "2":

        if limite_saque <= 0:
            print("Você já sacou muitas vezes hoje!")
            continue

        print("Você escolheu a opção Saque")
        saque = input("Quanto deseja sacar? Lembre-se que tem o limite de R$ 500.00\n")
        
        if saque.isalpha() == False:
            if float(saque) < 500:
                if float(saque) > saldo:
                    print("Tá querendo me roubar? Você não tem esse saldo todo não, pode voltar!")
                    continue
                else:
                    if float(saque) <= 0:
                        print("Eu sei que eu falei que valor negativo é em saque, mas coloque um valor positivo aí!")
                    else:
                        saldo -= float(saque)
                        limite_saque -= 1
                        print("Saque efetuado com Sucesso!")
                        extrato.append(f"Foi sacado um valor de R$ {float(saque):.2f}")
            else:
                print("Você não leu não? Limite de R$ 500.00")
                continue
        else:
            print("Detectei uma letra, por favor repita a operação!")

    elif escolha == "3":
        for inf in extrato:
            print(inf)
        print(f"Seu saldo atual é de R$ {saldo:.2f}")
    elif escolha == "0":
        break

    else:
        print("Opção inválida seu cabaço")