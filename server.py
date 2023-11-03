import alphaBetaPrunning
import copy
import game
import socket

HOST = ''
PORT = 8081

game.setMyColor('○','●')

def handle_client(conn):
    with conn:
        print('Connected by', conn.getpeername())
        board = game.create()
        game.printState(board)
        while not game.isFinished(board):
            data = conn.recv(10)
            if not data:
                conn.close()
                break
            try:
                move = int(data.decode())
                print('Received', move)
                if game.isLegal(move, board):
                    game.makeMove(move, board)
                    game.printState(board)
                    # Choose my move
                    my_move = 0
                    next_state = alphaBetaPrunning.go(board)
                    for move in game.legalMoves(board):
                        tmp=copy.deepcopy(board)
                        game.makeMove(move,tmp)
                        if tmp == next_state:
                            my_move = move
                            break
                    board = next_state
                    game.printState(board)
                    conn.sendall(str(my_move).encode())
                else:
                    conn.sendall(b'Invalid move')
                    conn.close()
                    break
            except ValueError:
                conn.sendall(b'Invalid input')
                conn.close()
                break
        game.printState(board)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Listening on', (HOST, PORT))
    conn, addr = s.accept()
    handle_client(conn)
