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

def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

    return msg

def send(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def handle_client(conn,nJogadores):
    if len(connections) < nJogadores:
        connections.append(conn)
        send(conn,'Você é o jogador número {}\nAguardando novos jogadores...\n'.format(len(connections)))
    else:
        send(conn,'Erro: o jogo já está lotado!')
        send(conn,'refused_connection')
        conn.close()
    

def start_server(nJogadores):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}, port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn,nJogadores))
        thread.start()



def jogo(dim, nJogadores):


    ##
    # Funcoes de manipulacao do tabuleiro
    ##

    # Imprime estado atual do tabuleiro
    def imprimeTabuleiro(tabuleiro):
        for con in connections:
            send(con,'limpa_tela')

        # Imprime coordenadas horizontais
        dim = len(tabuleiro)
        for con in connections:
            send(con,"     ")
            for i in range(0, dim):
                send(con,"{0:2d} ".format(i))

            send(con,"\n")

            # Imprime separador horizontal
            send(con,"-----")
            for i in range(0, dim):
                send(con,"---")

            send(con,"\n")

            for i in range(0, dim):

                # Imprime coordenadas verticais
                send(con,"{0:2d} | ".format(i))

                # Imprime conteudo da linha 'i'
                for j in range(0, dim):

                    # Peca ja foi removida?
                    if tabuleiro[i][j] == '-':

                        # Sim.
                        send(con," - ")

                    # Peca esta levantada?
                    elif tabuleiro[i][j] >= 0:

                        # Sim, imprime valor.
                        send(con,"{0:2d} ".format(tabuleiro[i][j]))
                    else:

                        # Nao, imprime '?'
                        send(con," ? ")

                send(con,"\n")

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
            send(con,"Placar:\n")
            send(con,"---------------------\n")
            for i in range(0, nJogadores):
                send(con,"Jogador {0}: {1:2d}\n".format(i + 1, placar[i]))

    ##
    # Funcoes de interacao com o usuario
    #

    # Imprime informacoes basicas sobre o estado atual da partida.
    def imprimeStatus(tabuleiro, placar, vez):

            imprimeTabuleiro(tabuleiro)
            send(connections[vez],'\n')

            imprimePlacar(placar)
            send(connections[vez],'\n')

            send(connections[vez],"Sua vez!\n")
            for i in range(0,len(connections)):
                if i != vez:
                    send(connections[i],"Vez do Jogador {0}.\n".format(vez + 1))

    # Le um coordenadas de uma peca. Retorna uma tupla do tipo (i, j)
    # em caso de sucesso, ou False em caso de erro.
    def leCoordenada(dim,vez):

        send(connections[vez],"Especifique uma peça:\n")
        inp = receive(connections[vez])
        try:
            i = int(inp.split(' ')[0])
            j = int(inp.split(' ')[1])
        except:
            send(connections[vez],"Coordenadas invalidas! Use o formato \"i j\" (sem aspas),\n")
            send(connections[vez],"onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}\n".format(dim))
            send(connections[vez],"Pressione <enter> para continuar...\n")
            return False
        
        

        if i < 0 or i >= dim:

            send(connections[vez],"Coordenada i deve ser maior ou igual a zero e menor que {0}\n".format(dim))
            send(connections[vez],"Pressione <enter> para continuar...\n")
            return False

        if j < 0 or j >= dim:

            send(connections[vez],"Coordenada j deve ser maior ou igual a zero e menor que {0}\n".format(dim))
            send(connections[vez],"Pressione <enter> para continuar...\n")
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

            send(connections[vez],"your_turn")
            # Solicita coordenadas da primeira peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                receive(connections[vez])
                continue

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i1, j1) == False:

                send(connections[vez],"Escolha uma peca ainda fechada! (Pressione <enter> para continuar)\n")
                receive(connections[vez])
                continue

            break 

        # Requisita segunda peca do proximo jogador
        while True:
            # Imprime status do jogo
            imprimeStatus(tabuleiro, placar, vez)

            # Solicita coordenadas da segunda peca.
            coordenadas = leCoordenada(dim,vez)
            if coordenadas == False:
                receive(connections[vez])
                continue

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if abrePeca(tabuleiro, i2, j2) == False:

                send(connections[vez],"Escolha uma peca ainda fechada! (Pressione <enter> para continuar)\n")
                receive(connections[vez])
                continue
            
            break 

        # Imprime status do jogo
        imprimeStatus(tabuleiro, placar, vez)

        send(connections[vez],"Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))

        # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:

            for con in connections:
                send(con,"Pecas casam! Ponto para o jogador {0}.\n".format(vez + 1))
            
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)

            time.sleep(3)
        else:
            for con in connections:
                send(con,"Pecas nao casam!\n")
            
            time.sleep(3)

            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            send(connections[vez],"end_of_your_turn")
            vez = (vez + 1) % nJogadores


    # Verificar o vencedor e imprimir
    pontuacaoMaxima = max(placar)
    vencedores = []
    for i in range(0, nJogadores):

        if placar[i] == pontuacaoMaxima:
            vencedores.append(i)

    if len(vencedores) > 1:

        for con in connections:
            send(con,"\n\nHouve empate entre os jogadores ")
            for i in vencedores:
                send(con,(str(i + 1) + ' '))

            send(con,"\n")
            send(con,'game_over')

    else:

        for con in connections:
            send(con,"\n\nJogador {0} foi o vencedor!\n".format(vencedores[0] + 1))
            send(con,'game_over')
        
        connections.clear()
        print('Aguardando conexões para novo jogo...')



# inicializa o jogo quando houver ao menos 2 jogadores conectados
def start_game(dim,nJogadores):
    start = True
    while start:
        if len(connections) == nJogadores:
            time.sleep(2)
            for con in connections:
                send(con,'Iniciando em 3...\n')
            time.sleep(1)
            for con in connections:
                send(con,'Iniciando em 2...\n')
            time.sleep(1)
            for con in connections:
                send(con,'Iniciando em 1...\n')
            time.sleep(1)
            jogo(dim,nJogadores)

dim = int(input('Informe a dimensão do tabuleiro (número par e menor do que 10): '))
while dim % 2 == 1 or dim >= 10 or dim < 2:
    dim = input('Valor inválido. Informe um um número par menor do que 10: ')
nJogadores = int(input('Informe a quantidade de jogadores: '))
while nJogadores < 2:
    nJogadores = input('Valor inválido. Informe um número maior ou igual a 2: ')

# Inicialização do servidor
server_thread = threading.Thread(target=start_server, args=[nJogadores])
server_thread.start()

# inicializa a espera por 2 jogadores 
start_game_thread = threading.Thread(target=start_game, args=(dim, nJogadores))
start_game_thread.start()