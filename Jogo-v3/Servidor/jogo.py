import time
import random
import services as svc


def jogo(dim, nJogadores, connections):

    ##
    # Funcoes de manipulacao do tabuleiro
    ##

    # Imprime estado atual do tabuleiro
    def imprimeTabuleiro(tabuleiro):
        # Imprime coordenadas horizontais
        dim = len(tabuleiro)
        for con in connections:
            svc.send_matrix(con, dim, tabuleiro)

    # Cria um novo tabuleiro com peças aleatorias.
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
        # sortearmos posicoes aleatoriamente para as peças.
        posicoesDisponiveis = []
        for i in range(0, dim):

            for j in range(0, dim):

                posicoesDisponiveis.append((i, j))

        # Varre todas as peças que serao colocadas no
        # tabuleiro e posiciona cada par de peças iguais
        # em posicoes aleatorias.
        for j in range(0, (int)(dim / 2)):
            for i in range(1, dim + 1):

                # Sorteio da posicao da segunda peça com valor 'i'
                maximo = len(posicoesDisponiveis)
                indiceAleatorio = random.randint(0, maximo - 1)
                rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

                tabuleiro[rI][rJ] = -i

                # Sorteio da posicao da segunda peça com valor 'i'
                maximo = len(posicoesDisponiveis)
                indiceAleatorio = random.randint(0, maximo - 1)
                rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

                tabuleiro[rI][rJ] = -i

        return tabuleiro

    # Abre (revela) peça na posicao (i, j). Se posicao ja esta
    # aberta ou se ja foi removida, retorna False. Retorna True
    # caso contrario.
    def abrePeca(tabuleiro, i, j):

        if tabuleiro[i][j] == '-':
            return False
        elif tabuleiro[i][j] < 0:
            tabuleiro[i][j] = -tabuleiro[i][j]
            return True

        return False

    # Fecha peça na posicao (i, j). Se posicao ja esta
    # fechada ou se ja foi removida, retorna False. Retorna True
    # caso contrario.
    def fechaPeca(tabuleiro, i, j):

        if tabuleiro[i][j] == '-':
            return False
        elif tabuleiro[i][j] > 0:
            tabuleiro[i][j] = -tabuleiro[i][j]
            return True

        return False

    # Remove peça na posicao (i, j). Se posicao ja esta
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
            # svc.send(con, "Placar:")
            # svc.send(con, "---------------------")
            all_players = 'P='
            for i in range(0, nJogadores):
                all_players += "Jogador {0}: {1:2d}\n".format(
                    i + 1, placar[i])
            svc.send(con, all_players)

    ##
    # Funcoes de interacao com o usuario
    #

    # Imprime informacoes basicas sobre o estado atual da partida.
    def imprimeStatus(tabuleiro, placar, vez):

        imprimeTabuleiro(tabuleiro)
        # svc.send(connections[vez], '')

        imprimePlacar(placar)
        # svc.send(connections[vez], '')

        # svc.send(connections[vez], "Sua vez!")
        for i in range(0, len(connections)):
            if i != vez:
                svc.send(connections[i],
                         "Vez do Jogador {0}.".format(vez + 1))

    # Le um coordenadas de uma peça. Retorna uma tupla do tipo (i, j)
    # em caso de sucesso, ou False em caso de erro.
    def leCoordenada(dim, vez):

        svc.send(connections[vez], "Especifique uma peça")
        inp = svc.receive(connections[vez])
        try:
            i = int(inp.split(' ')[0])
            j = int(inp.split(' ')[1])
        except:
            return False

        if i < 0 or i >= dim:
            return False

        if j < 0 or j >= dim:
            return False

        return (i, j)

    ##
    # Parametros da partida
    ##

    # Numero total de pares de peças
    totalDePares = dim**2 / 2

    ##
    # Programa principal
    ##

    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)

    # Cria um novo placar zerado
    placar = novoPlacar(nJogadores)

    # Partida continua enquanto ainda ha pares de peças a
    # casar.
    paresEncontrados = 0
    vez = 0
    while paresEncontrados < int(totalDePares):

        # Requisita primeira peça do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            svc.send(connections[vez], "your_turn")
            # Solicita coordenadas da primeira peça.
            coordenadas = leCoordenada(dim, vez)
            if coordenadas == False:
                continue

            i1, j1 = coordenadas

            # Testa se peça ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                svc.send(
                    connections[vez], "Escolha uma peça ainda fechada! (Pressione <enter> para continuar)")
                msg = svc.receive(connections[vez])
                while msg != "":
                    msg = svc.receive(connections[vez])
                continue

            break

        # Requisita segunda peça do proximo jogador
        while True:
            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peça.
            coordenadas = leCoordenada(dim, vez)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            # Testa se peça ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                svc.send(
                    connections[vez], "Escolha uma peça ainda fechada! (Pressione <enter> para continuar)")
                msg = svc.receive(connections[vez])
                while msg != "":
                    msg = svc.receive(connections[vez])
                continue

            break

        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        svc.send(
            connections[vez], "Peças escolhidas --> ({0}, {1}) e ({2}, {3})".format(i1, j1, i2, j2))

        # Peças escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            for con in connections:
                svc.send(
                    con, "Peças casam! Ponto para o jogador {0}.".format(vez + 1))

            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(3)
        else:
            for con in connections:
                svc.send(con, "Peças não casam!")

            time.sleep(3)

            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            svc.send(connections[vez], "end_of_your_turn")
            vez = (vez + 1) % nJogadores

    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = []
    for i in range(0, nJogadores):

        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        for con in connections:
            svc.send(con, "Houve empate entre os jogadores ")
            for i in vencedores:
                svc.send(con, (str(i + 1) + ' '))

            svc.send(con, 'game_over')

        connections.clear()
        print('Aguardando conexões para novo jogo...')

    else:
        svc.send_for_all(
            connections, "Jogador {0} foi o vencedor!".format(vencedores[0] + 1))
        svc.send_for_all(connections, 'game_over')
        connections.clear()
        print('Aguardando conexões para novo jogo...')


def handle_game(dim, nJogadores, connections):
    start = True
    while start:
        if len(connections) == nJogadores:
            time.sleep(2)
            for con in connections:
                svc.send(con, 'Iniciando em 3...')
            time.sleep(1)
            for con in connections:
                svc.send(con, 'Iniciando em 2...')
            time.sleep(1)
            for con in connections:
                svc.send(con, 'Iniciando em 1...')
            time.sleep(1)
            jogo(dim, nJogadores, connections)
