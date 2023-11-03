from time import sleep
import requests
import game
import alphaBetaPrunning
import copy

host = "localhost:8000"
board = game.create() 
game.printState(board)
game.setMyColor('●', '○')

def send_get_request():
    global board
    temp_host = input("Enter host: ")
    if temp_host != "":
        host = temp_host
    print(host)
    # Choose my move
    my_move = 0
    print(game.legalMoves(board))
    next_state = alphaBetaPrunning.go(board)
    for move in game.legalMoves(board):
        tmp=copy.deepcopy(board)
        game.makeMove(move,tmp)
        if tmp == next_state:
            my_move = move
            break
    board = next_state
    print(board)
    game.printState(board)
    url = f"http://{host}/?move={my_move}"
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("GET Request was successful.")
            print("Response content:")
            print(response.text)
            opp_move = int(response.text)
            if game.isLegal(opp_move, board):
                game.makeMove(opp_move, board)
                game.printState(board)
            else:
                raise Exception("Server played with an invalid move")
        else:
            print(f"GET Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    oneMoreTurn = False
    while not game.isFinished(board) or oneMoreTurn:
        send_get_request()
        print("Sent")
        # sleep(0.1)
