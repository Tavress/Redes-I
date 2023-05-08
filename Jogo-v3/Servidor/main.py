import threading
import socket_handler as sck
import jogo as jg

connections = []

# Solicita dimensão do tabuleiro e a quantidade de jogadores
# dim = int(input('Informe a dimensão do tabuleiro (número par e menor do que 10): '))
# while dim % 2 == 1 or dim >= 10 or dim < 2:
#    dim = input('Valor inválido. Informe um um número par menor do que 10: ')
# nJogadores = int(input('Informe a quantidade de jogadores: '))
# while nJogadores < 2:
#    nJogadores = input('Valor inválido. Informe um número maior ou igual a 2: ')
dim, nJogadores = 10, 2
# Inicialização do servidor
server_thread = threading.Thread(target=sck.start_server, args=[
                                 nJogadores, connections])
server_thread.start()

# Inicializa o jogo quando houver nJogadores
start_game_thread = threading.Thread(
    target=jg.handle_game, args=(dim, nJogadores, connections))
start_game_thread.start()
