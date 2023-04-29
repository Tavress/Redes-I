import os
import sys
import time
import random
import threading
import socket

HEADER = 64
PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

connections = []
choices_dict = {}


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connections.append(conn)
    print(f'[ACTIVE CONNECTIONS] {connections}')
   
    

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        thread.start()



def jogo():
    ##
    # Funcoes uteis
    ##

    # Limpa a tela.
    def limpaTela():
        
        os.system('cls' if os.name == 'nt' else 'clear')

    ##
    # Funcoes de manipulacao do tabuleiro
    ##

    # Imprime estado atual do tabuleiro
    def imprimeTabuleiro(tabuleiro):

        # Limpa a tela
        limpaTela()

        # Imprime coordenadas horizontais
        dim = len(tabuleiro)
        for con in connections:
            con.send("     ".encode(FORMAT))
            for i in range(0, dim):
                con.send("{0:2d} ".format(i).encode(FORMAT))

            con.send("\n".encode(FORMAT))

            # Imprime separador horizontal
            con.send("-----".encode(FORMAT))
            for i in range(0, dim):
                con.send("---".encode(FORMAT))

            con.send("\n".encode(FORMAT))

            for i in range(0, dim):

                # Imprime coordenadas verticais
                con.send("{0:2d} | ".format(i).encode(FORMAT))

                # Imprime conteudo da linha 'i'
                for j in range(0, dim):

                    # Peca ja foi removida?
                    if tabuleiro[i][j] == '-':

                        # Sim.
                        con.send(" - ".encode(FORMAT))

                    # Peca esta levantada?
                    elif tabuleiro[i][j] >= 0:

                        # Sim, imprime valor.
                        con.send("{0:2d} ".format(tabuleiro[i][j]).encode(FORMAT))
                    else:

                        # Nao, imprime '?'
                        con.send(" ? ".encode(FORMAT))

                con.send("\n".encode(FORMAT))

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
            con.send("Placar:".encode(FORMAT))
            con.send("---------------------".encode(FORMAT))
            for i in range(0, nJogadores):
                con.send("Jogador {0}: {1:2d}".format(i + 1, placar[i]).encode(FORMAT))

    ##
    # Funcoes de interacao com o usuario
    #

    # Imprime informacoes basicas sobre o estado atual da partida.
    def imprimeStatus(tabuleiro, placar, vez):

            imprimeTabuleiro(tabuleiro)
            connections[vez].send('\n'.encode(FORMAT))

            imprimePlacar(placar)
            connections[vez].send('\n'.encode(FORMAT))
            connections[vez].send('\n'.encode(FORMAT))

            connections[vez].send("Sua vez!".encode(FORMAT))
            for i in range(0,len(connections)):
                if i != vez:
                    connections[i].send("Vez do Jogador {0}.\n".format(vez + 1).encode(FORMAT))

    # Le um coordenadas de uma peca. Retorna uma tupla do tipo (i, j)
    # em caso de sucesso, ou False em caso de erro.
    def leCoordenada(dim,vez):

        connections[vez].send("Especifique uma peça: ".encode(FORMAT))
        inp = connections[vez].recv(1024).decode(FORMAT)
        try:
            i = int(inp.split(' ')[0])
            j = int(inp.split(' ')[1])
        except:
            connections[vez].send("Coordenadas invalidas! Use o formato \"i j\" (sem aspas),".encode(FORMAT))
            connections[vez].send("onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}".format(dim).encode(FORMAT))
            connections[vez].send("Pressione <enter> para continuar...".encode(FORMAT))
            return False
        
        

        if i < 0 or i >= dim:

            connections[vez].send("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim).encode(FORMAT))
            connections[vez].send("Pressione <enter> para continuar...".encode(FORMAT))
            inp_rec = connections[vez].recv(1024).decode(FORMAT)
            print(inp_rec)
            return False

        if j < 0 or j >= dim:

            connections[vez].send("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim).encode(FORMAT))
            connections[vez].send("Pressione <enter> para continuar...".encode(FORMAT))
            inp_rec = connections[vez].recv(1024).decode(FORMAT)
            print(inp_rec)
            return False

        return (i, j)

    ##
    # Parametros da partida
    ##

    # Tamanho (da lateral) do tabuleiro. NECESSARIAMENTE PAR E MENOR QUE 10!
    dim = 4

    # Numero de jogadores
    nJogadores = 2

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
    while paresEncontrados < totalDePares:

        # Requisita primeira peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                continue

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                connections[vez].send("Escolha uma peca ainda fechada!".encode(FORMAT))
                inp_rec = connections[vez].recv(1024).decode(FORMAT)
                print(inp_rec)
                continue

            break 

        # Requisita segunda peca do proximo jogador
        while True:

            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                connections[vez].send("Escolha uma peca ainda fechada!".encode(FORMAT))
                inp_rec = connections[vez].recv(1024).decode(FORMAT)
                continue

            break 

        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        connections[vez].send("Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2).encode(FORMAT))

        # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            for con in connections:
                con.send("Pecas casam! Ponto para o jogador {0}.".format(vez + 1).encode(FORMAT))
            
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(5)
        else:
            for con in connections:
                con.send("Pecas nao casam!".encode(FORMAT))
            
            time.sleep(3)

            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            vez = (vez + 1) % nJogadores

    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = []
    for i in range(0, nJogadores):

        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        for con in connections:
            con.send("Houve empate entre os jogadores ".encode(FORMAT))
            for i in vencedores:
                con.send((str(i + 1) + ' ').encode(FORMAT))

            con.send("\n".encode(FORMAT))

    else:

        for con in connections:
            con.send("Jogador {0} foi o vencedor!".format(vencedores[0] + 1).encode(FORMAT))


# inicializa o jogo quando houver ao menos 2 jogadores conectados
def start_game():

    while True:
        if len(connections) >= 2:
            jogo()


# Inicialização do servidor
server_thread = threading.Thread(target=start_server)
server_thread.start()

# inicializa a espera por 2 jogadores 
start_game_thread = threading.Thread(target=start_game)
start_game_thread.start()