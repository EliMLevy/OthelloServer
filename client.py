import alphaBetaPrunning
import copy
import game
import socket

HOST = input("Enter the host: ")  # The server's hostname or IP address
PORT = int(input("Enter the port:"))  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to", (HOST, PORT))
    board = game.create()
    game.setMyColor("●", "○")
    game.printState(board)
    while not game.isFinished(board):
        # Choose my move
        my_move = 0
        next_state = alphaBetaPrunning.go(board)
        for move in game.legalMoves(board):
            tmp = copy.deepcopy(board)
            game.makeMove(move, tmp)
            if tmp == next_state:
                my_move = move
                break
        board = next_state
        game.printState(board)
        s.sendall(str(my_move).encode())

        # receive the opponent's move
        data = s.recv(10)
        if not data:
            s.close()
            break
        move = int(data.decode())
        print("Received", move)
        if game.isLegal(move, board):
            game.makeMove(move, board)
            game.printState(board)
    game.printState(board)
