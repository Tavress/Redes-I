import time
import random
import services as svc

def jogo(dim, nJogadores,connections):


    ##
    # Funcoes de manipulacao do tabuleiro
    ##

    # Imprime estado atual do tabuleiro
    def imprimeTabuleiro(tabuleiro):
        svc.send_for_all(connections,'limpa_tela')

        # Imprime coordenadas horizontais
        dim = len(tabuleiro)
        for con in connections:
            svc.send(con,"     ")
            for i in range(0, dim):
                svc.send(con,"{0:2d} ".format(i))

            svc.send(con,"\n")

            # Imprime separador horizontal
            svc.send(con,"-----")
            for i in range(0, dim):
                svc.send(con,"---")

            svc.send(con,"\n")

            for i in range(0, dim):

                # Imprime coordenadas verticais
                svc.send(con,"{0:2d} | ".format(i))

                # Imprime conteudo da linha 'i'
                for j in range(0, dim):

                    # Peca ja foi removida?
                    if tabuleiro[i][j] == '-':

                        # Sim.
                        svc.send(con," - ")

                    # Peca esta levantada?
                    elif tabuleiro[i][j] >= 0:

                        # Sim, imprime valor.
                        svc.send(con,"{0:2d} ".format(tabuleiro[i][j]))
                    else:

                        # Nao, imprime '?'
                        svc.send(con," ? ")

                svc.send(con,"\n")

    # Cria um novo tabuleiro com pecas aleatorias. 
    # 'dim' eh a dimensao do tabuleiro, necessariamente
    # par.
    def novoTabuleiro(dim):

        # Cria um tabuleiro vazio.
        tabuleiro = []
        for i in range(0, dim):

            linha = []
            for j in range(0, dim):

                linha.append(0)

            tabuleiro.append(linha)

        # Cria uma lista de todas as posicoes do tabuleiro. Util para
        # sortearmos posicoes aleatoriamente para as pecas.
        posicoesDisponiveis = []
        for i in range(0, dim):

            for j in range(0, dim):

                posicoesDisponiveis.append((i, j))

        # Varre todas as pecas que serao colocadas no 
        # tabuleiro e posiciona cada par de pecas iguais
        # em posicoes aleatorias.
        for j in range(0, (int)(dim / 2)):
            for i in range(1, dim + 1):

                # Sorteio da posicao da segunda peca com valor 'i'
                maximo = len(posicoesDisponiveis)
                indiceAleatorio = random.randint(0, maximo - 1)
                rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

                tabuleiro[rI][rJ] = -i

                # Sorteio da posicao da segunda peca com valor 'i'
                maximo = len(posicoesDisponiveis)
                indiceAleatorio = random.randint(0, maximo - 1)
                rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

                tabuleiro[rI][rJ] = -i

        return tabuleiro

    # Abre (revela) peca na posicao (i, j). Se posicao ja esta
    # aberta ou se ja foi removida, retorna False. Retorna True
    # caso contrario.
    def abrePeca(tabuleiro, i, j):

        if tabuleiro[i][j] == '-':
            return False
        elif tabuleiro[i][j] < 0:
            tabuleiro[i][j] = -tabuleiro[i][j]
            return True

        return False

    # Fecha peca na posicao (i, j). Se posicao ja esta
    # fechada ou se ja foi removida, retorna False. Retorna True
    # caso contrario.
    def fechaPeca(tabuleiro, i, j):

        if tabuleiro[i][j] == '-':
            return False
        elif tabuleiro[i][j] > 0:
            tabuleiro[i][j] = -tabuleiro[i][j]
            return True

        return False

    # Remove peca na posicao (i, j). Se posicao ja esta
    # removida, retorna False. Retorna True
    # caso contrario.
    def removePeca(tabuleiro, i, j):

        if tabuleiro[i][j] == '-':
            return False
        else:
            tabuleiro[i][j] = "-"
            return True

    ## 
    # Funcoes de manipulacao do placar
    ##

    # Cria um novo placar zerado.
    def novoPlacar(nJogadores):

        return [0] * nJogadores

    # Adiciona um ponto no placar para o jogador especificado.
    def incrementaPlacar(placar, jogador):

        placar[jogador] = placar[jogador] + 1

    # Imprime o placar atual.
    def imprimePlacar(placar):

        nJogadores = len(placar)

        for con in connections:
            svc.send(con,"Placar:\n")
            svc.send(con,"---------------------\n")
            for i in range(0, nJogadores):
                svc.send(con,"Jogador {0}: {1:2d}\n".format(i + 1, placar[i]))

    ##
    # Funcoes de interacao com o usuario
    #

    # Imprime informacoes basicas sobre o estado atual da partida.
    def imprimeStatus(tabuleiro, placar, vez):

            imprimeTabuleiro(tabuleiro)
            svc.send(connections[vez],'\n')

            imprimePlacar(placar)
            svc.send(connections[vez],'\n')

            svc.send(connections[vez],"Sua vez!\n")
            for i in range(0,len(connections)):
                if i != vez:
                    svc.send(connections[i],"Vez do Jogador {0}.\n".format(vez + 1))

    # Le um coordenadas de uma peca. Retorna uma tupla do tipo (i, j)
    # em caso de sucesso, ou False em caso de erro.
    def leCoordenada(dim,vez):

        svc.send(connections[vez],"Especifique uma peça:\n")
        inp = svc.receive(connections[vez])
        try:
            i = int(inp.split(' ')[0])
            j = int(inp.split(' ')[1])
        except:
            svc.send(connections[vez],"Coordenadas invalidas! Use o formato \"i j\" (sem aspas),\n")
            svc.send(connections[vez],"onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}\n".format(dim))
            svc.send(connections[vez],"Pressione <enter> para continuar...\n")
            return False
        
        

        if i < 0 or i >= dim:

            svc.send(connections[vez],"Coordenada i deve ser maior ou igual a zero e menor que {0}\n".format(dim))
            svc.send(connections[vez],"Pressione <enter> para continuar...\n")
            return False

        if j < 0 or j >= dim:

            svc.send(connections[vez],"Coordenada j deve ser maior ou igual a zero e menor que {0}\n".format(dim))
            svc.send(connections[vez],"Pressione <enter> para continuar...\n")
            return False

        return (i, j)

    ##
    # Parametros da partida
    ##

    # Numero total de pares de pecas
    totalDePares = dim**2 / 2

    ##
    # Programa principal
    ##

    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)

    # Cria um novo placar zerado
    placar = novoPlacar(nJogadores)

    # Partida continua enquanto ainda ha pares de pecas a 
    # casar.
    paresEncontrados = 0
    vez = 0
    while paresEncontrados < int(totalDePares):

        # Requisita primeira peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            svc.send(connections[vez],"your_turn")
            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                svc.receive(connections[vez])
                continue

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                svc.send(connections[vez],"Escolha uma peca ainda fechada! (Pressione <enter> para continuar)\n")
                svc.receive(connections[vez])
                continue

            break 

        # Requisita segunda peca do proximo jogador
        while True:
            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                svc.receive(connections[vez])
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                svc.send(connections[vez],"Escolha uma peca ainda fechada! (Pressione <enter> para continuar)\n")
                svc.receive(connections[vez])
                continue
            
            break 

        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        svc.send(connections[vez],"Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))

        # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            for con in connections:
                svc.send(con,"Pecas casam! Ponto para o jogador {0}.\n".format(vez + 1))
            
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(3)
        else:
            for con in connections:
                svc.send(con,"Pecas nao casam!\n")
            
            time.sleep(3)

            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            svc.send(connections[vez],"end_of_your_turn")
            vez = (vez + 1) % nJogadores


    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = []
    for i in range(0, nJogadores):

        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        for con in connections:
            svc.send(con,"\n\nHouve empate entre os jogadores ")
            for i in vencedores:
                svc.send(con,(str(i + 1) + ' '))

            svc.send(con,"\n")
            svc.send(con,'game_over')

        connections.clear()
        print('Aguardando conexões para novo jogo...')
    

    else:
        svc.send_for_all(connections,"\n\nJogador {0} foi o vencedor!\n".format(vencedores[0] + 1))
        svc.send_for_all(connections,'game_over')
        connections.clear()
        print('Aguardando conexões para novo jogo...')


def handle_game(dim,nJogadores,connections):
    start = True
    while start:
        if len(connections) == nJogadores:
            time.sleep(2)
            for con in connections:
                svc.send(con,'Iniciando em 3...\n')
            time.sleep(1)
            for con in connections:
                svc.send(con,'Iniciando em 2...\n')
            time.sleep(1)
            for con in connections:
                svc.send(con,'Iniciando em 1...\n')
            time.sleep(1)
            jogo(dim,nJogadores,connections)