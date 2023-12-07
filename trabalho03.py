import json
import random

melhorIndividuo = []
melhorFitness = -999
seed = 15346278912
random = random.Random(seed)

def menu():
    print('1 - Treinar com os parâmetros padrão')
    print('2 - Bloco 1 (Taxa de Elitismo)')
    print('3 - Bloco 2 (Tamanho da População)')
    print('4 - Sair')

def matrizString(matriz):
    string = ""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            string += str(matriz[i][j])
    return string

def StringMatriz(string, enfermeiras, turnos):
    matriz = []
    for i in range(enfermeiras):
        matriz.append([])
        for j in range(turnos):
            matriz[i].append(int(string[i*turnos+j]))
    return matriz

def composicaoInicial(enfermeiras, turnos):
    individuoInicial = []
    for i in range(enfermeiras):
        individuoInicial.append([])
        for j in range(turnos):
            individuoInicial[i].append(random.randint(0, 1))
    return individuoInicial

def avalia(individuo, enfermeiras, turnos, TurnosDTN):
    violacoes = 0
    #individual = matriz
    # – r1: É necessário haver no mínimo 1 enfermeiro e no máximo 3 enfermeiras em cada turno.
    # – r2: Cada enfermeiro deve ser alocado em 5 turnos por semana.
    # – r3: Nenhum enfermeiro pode trabalhar mais que 3 dias seguidos sem folga.
    # – r4: Enfermeiras preferem consistência em seus horários, ou seja, eles preferem trabalhar todos os dias da semana no mesmo turno (dia, noite, ou madrugada).

    # r1
    for i in range(turnos):
        soma = 0
        for j in range(enfermeiras):
            soma += individuo[j][i]
        if soma < 1 or soma > 3:
            violacoes -= 1
        # print ("Linha: ", i, "Soma: ", soma, "Violacoes: ", violacoes)

    # r2
    for i in range(enfermeiras):
        soma = 0
        for j in range(turnos):
            soma += individuo[i][j]
        if soma != 5:
            violacoes -= 1
        # print ("Linha: ", i, "Soma: ", soma, "Violacoes: ", violacoes)

    # r3
    for i in range(enfermeiras):
        soma = 0
        for j in range(turnos):
            if individuo[i][j] == 1:
                soma += individuo[i][j]
            else :
                soma = 0
            if soma > 3:
                violacoes -= 1
                break

    #r4
    for i in range(enfermeiras):
        dia = 0
        tarde = 0
        noite = 0
        for j in range(turnos):
            if individuo[i][j] == 1:
                if TurnosDTN[j] == 'D':
                    dia += 1
                elif TurnosDTN[j] == 'T':
                    tarde += 1
                else:
                    noite += 1

        if dia > 0 and tarde > 0:
            violacoes -= 1
        elif dia > 0 and noite > 0:
            violacoes -= 1
        elif tarde > 0 and noite > 0:
            violacoes -= 1
           
    global melhorIndividuo
    global melhorFitness
    if violacoes > melhorFitness:
        melhorFitness = violacoes
        melhorIndividuo = individuo

    return violacoes

def cruzar(individuo1, individuo2, enfermeiras, turnos):
    individuo1 = matrizString(individuo1)
    individuo2 = matrizString(individuo2)

    pontoDeCorte = range(len(individuo1))
    pontoDeCorte = random.choice(pontoDeCorte)

    individuo1Backup = individuo1
    individuo1 = individuo1[:pontoDeCorte] + individuo2[pontoDeCorte:]
    individuo2 = individuo2[:pontoDeCorte] + individuo1Backup[pontoDeCorte:]

    individuo1 = StringMatriz(individuo1, enfermeiras, turnos)
    individuo2 = StringMatriz(individuo2, enfermeiras, turnos)

    return individuo1 , individuo2

def mutar(individuo):
    stringIndividuo = matrizString(individuo)
    #altera um caracter aleatorio de 0 para 1 ou de 1 para 0
    posicao = random.randint(0, len(stringIndividuo)-1)
    if stringIndividuo[posicao] == "0":
        stringIndividuo = stringIndividuo[:posicao] + "1" + stringIndividuo[posicao+1:]
    else:
        stringIndividuo = stringIndividuo[:posicao] + "0" + stringIndividuo[posicao+1:]
    
    individuo = StringMatriz(stringIndividuo, len(individuo), len(individuo[0]))
    return individuo

def gerarNovaPopulacao(populacao, taxaMutacao, taxaElitismo, enfermeiras, turnos):
    isPar = len(populacao) % 2 == 0
    elitistas = []
    novaPopulacao = []
    for i in range(int(len(populacao) * taxaElitismo)):
        elitistas.append(populacao[i])

    #pega 2 individuos aleatorios da populacao, cruza, adiciona na nova populacao e apaga da populacao
    for i in range(int(len(populacao)/2)):
        individuo1 = random.choice(populacao)
        populacao.remove(individuo1)
        individuo2 = random.choice(populacao)
        populacao.remove(individuo2)
        individuo1, individuo2 = cruzar(individuo1, individuo2, enfermeiras, turnos)
        
        if random.random() < taxaMutacao:
            novaPopulacao.append(mutar(individuo1))
            novaPopulacao.append(mutar(individuo2))
            
        else:    
            novaPopulacao.append(individuo1)
            novaPopulacao.append(individuo2)

    #taxa de elitismo, apaga os piores individuos da nova populacao e adiciona os melhores da populacao antiga de acordo com a taxa de elitismo
    #taxa de elitismo vai de 0 a 1, se for 0.1, 10% da populacao nova vai ser apagada e 10% da populacao antiga vai ser adicionada na nova populacao

    #apagando os piores
    for i in range(int(len(novaPopulacao)*taxaElitismo)):
        novaPopulacao.pop()

    #adicionando os melhores
    for i in range(len(elitistas)):
        novaPopulacao.append(elitistas[i])
    
    if not isPar:
        novaPopulacao.append(cruzar(random.choice(populacao), random.choice(populacao), enfermeiras, turnos)[0])

    return novaPopulacao

def ordenarPopulacao(populacao, enfermeiras, turnos, tamanhoPopulacao, TurnosDTN):
    for i in range(tamanhoPopulacao):
        ordem = []
    for j in range(tamanhoPopulacao):
        ordem.append(avalia(populacao[j], enfermeiras, turnos, TurnosDTN))
    for j in range(tamanhoPopulacao):
        for k in range(tamanhoPopulacao):
            if ordem[j] > ordem[k]:
                aux = ordem[j]
                ordem[j] = ordem[k]
                ordem[k] = aux
                aux = populacao[j]
                populacao[j] = populacao[k]
                populacao[k] = aux
    return populacao

def excluiPioresDobraMelhores(populacao, tamanhoPopulacao):
    isPar = tamanhoPopulacao % 2 == 0

    # apaga os piores
    for i in range(int(tamanhoPopulacao/2), tamanhoPopulacao):
        populacao.pop()
    
    # duplica
    for i in range(int(tamanhoPopulacao/2)):
        populacao.append(populacao[i])
    
    if not isPar:
        populacao.append(populacao[0])

    random.shuffle(populacao)
    return populacao


def treinar(enfermeiras, turnos, tamanhoPopulacao, numeroIteracoes, taxaMutacao, taxaElitismo):
    global melhorIndividuo
    global melhorFitness
    melhorIndividuo = []
    melhorFitness = -999
    TurnosDTN = []

    for i in range(turnos):
        if i % 3 == 0:
            TurnosDTN.append('D')
        elif i % 3 == 1:
            TurnosDTN.append('T')
        else:
            TurnosDTN.append('N')

    populacao = []
    for i in range(tamanhoPopulacao):
        populacao.append(composicaoInicial(enfermeiras, turnos))

    melhoresFitness = []
    for i in range(numeroIteracoes): #IMPRIME O FITNESS DA POPULACAO
        print(f"\rIteração: ({i+1}/{numeroIteracoes})   ", end="")
        populacao = ordenarPopulacao(populacao, enfermeiras, turnos, tamanhoPopulacao, TurnosDTN)

        for i in range(tamanhoPopulacao):
            avalia(populacao[i], enfermeiras, turnos, TurnosDTN)

        populacao = excluiPioresDobraMelhores(populacao, tamanhoPopulacao)
        populacao = gerarNovaPopulacao(populacao, taxaMutacao, taxaElitismo, enfermeiras, turnos)
        populacao = ordenarPopulacao(populacao, enfermeiras, turnos, tamanhoPopulacao, TurnosDTN)

        melhoresFitness.append(melhorFitness)
    
    print()
    return melhoresFitness



def bloco_1():
    enfermeiras = 10
    turnos = 21
    tamanhoPopulacao = 100
    numeroIteracoes = 1000
    taxaMutacao = 0.1
    taxasElitismo = [0, 0.1, 0.25, 0.5, 0.75]

    with open('bloco_1.csv', 'w') as f:
        f.write("taxaElitismo,iteracao,melhorFitness\n")
        for taxaElitismo in taxasElitismo:
            print(f"Taxa de elitismo: {taxaElitismo}")
            melhoresFitness = treinar(enfermeiras, turnos, tamanhoPopulacao, numeroIteracoes, taxaMutacao, taxaElitismo)

            for i in range(numeroIteracoes):
                f.write(str(taxaElitismo) + "," + str(i) + "," + str(melhoresFitness[i]) + "\n")

    with open('bloco_1.json', 'w') as f:
        f.write(json.dumps({
            "seed": seed,
            "enfermeiras": enfermeiras,
            "turnos": turnos,
            "tamanhoPopulacao": tamanhoPopulacao,
            "numeroIteracoes": numeroIteracoes,
            "taxaMutacao": taxaMutacao,
            "taxasElitismo": taxasElitismo,
            "melhorFitness": melhorFitness,
            "melhorIndividuo": melhorIndividuo
        }))

def bloco_2():
    enfermeiras = 10
    turnos = 21
    tamanhosPopulacao = [10, 25, 50, 100, 500, 1000]
    numeroIteracoes = 1000
    taxaMutacao = 0.1
    taxaElitismo = 0.1

    with open('bloco_2.csv', 'w') as f:
        f.write("tamanhoPopulacao,iteracao,melhorFitness\n")
        for tamanhoPopulacao in tamanhosPopulacao:
            print(f"População: {tamanhoPopulacao}")
            melhoresFitness = treinar(enfermeiras, turnos, tamanhoPopulacao, numeroIteracoes, taxaMutacao, taxaElitismo)

            for i in range(numeroIteracoes):
                f.write(str(tamanhoPopulacao) + "," + str(i) + "," + str(melhoresFitness[i]) + "\n")

    with open('bloco_2.json', 'w') as f:
        f.write(json.dumps({
            "seed": seed,
            "enfermeiras": enfermeiras,
            "turnos": turnos,
            "tamanhosPopulacao": tamanhosPopulacao,
            "numeroIteracoes": numeroIteracoes,
            "taxaMutacao": taxaMutacao,
            "taxaElitismo": taxaElitismo,
            "melhorFitness": melhorFitness,
            "melhorIndividuo": melhorIndividuo
        }))

def tratarDadosInput(texto, tipo):
    while True:
        try:
            return tipo(input(texto))
        except:
            print("Valor inválido! Tente novamente.")
            continue

def main():
    while True:
        menu()
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            enfermeiras = tratarDadosInput("Quantas enfermeiras temos disponíveis? ", int)
            turnos = tratarDadosInput("Quantos turnos temos disponíveis? (Sempre múltiplo de 3) ", int)
            tamanhoPopulacao = tratarDadosInput("Qual o tamanho da população? (Preferencialmente um número par) ", int)
            numeroIteracoes = tratarDadosInput("Quantas iterações devemos fazer? (Quanto mais, melhor!) ", int)
            taxaMutacao = tratarDadosInput("Qual a taxa de mutação? (0 - 1) ", float)
            taxaElitismo = tratarDadosInput("Qual a taxa de elitismo? (0 - 1) ", float)
            melhoresFitness = treinar(enfermeiras, turnos, tamanhoPopulacao, numeroIteracoes, taxaMutacao, taxaElitismo)
            for i in range(numeroIteracoes):
                print(f"Fitness da iteração {i+1}: {melhoresFitness[i]}")
            continue
        elif opcao == 2:
            bloco_1()
            print("Bloco 1 concluído! Utilize o arquivo bloco_1.csv para visualizar os resultados.")
            continue
        elif opcao == 3:
            bloco_2()
            print("Bloco 2 concluído! Utilize o arquivo bloco_2.csv para visualizar os resultados.")
            continue
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
            time.sleep(1)
            continue
main()
