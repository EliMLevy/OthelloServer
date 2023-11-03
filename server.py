import http.server
import socketserver
import game
import alphaBetaPrunning
from urllib.parse import urlparse, parse_qs
import copy


board = game.create() 
game.printState(board)
game.setMyColor('○','●')


class MyHandler(http.server.BaseHTTPRequestHandler):


    def do_GET(self):
        global board
        # Parse the query string
        parsed_url = urlparse(self.path)
        parsed_url.geturl()
        query_params = parse_qs(parsed_url.query)

        # Check if the "move" parameter is in the query string
        move_value = None
        if 'move' in query_params:
            move_value = int(query_params['move'][0])
            print(f'Move: {move_value}'.encode('utf-8'))
        else:
            print(b'Missing "move" parameter in the query string')
        if parsed_url.path == '/' and move_value != None:
            # Update board
            if game.isLegal(move_value, board):
                game.makeMove(move_value, board)
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
                res = bytes(f'{my_move}'.encode('utf-8'))
                # Respond with my move
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(res)
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid move')
                

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    PORT = 8000

    with socketserver.TCPServer(('', PORT), MyHandler) as httpd:
        print(f'Serving on port {PORT}')
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()


    # Create the board
    # Wait for a client to send a move
    # Update the board and respond with our move
    # Go back to wait
