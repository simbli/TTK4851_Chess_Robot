from stockfish import Stockfish
import chess

board = chess.Board()

stockfish = Stockfish()

moves = []
print chess.SQUARES
print chess.SQUARE_NAMES
print board.piece_type_at(9)

while True:
	moves.append(raw_input("Next Move:"))
	stockfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))


	moves.append(stockfish.get_best_move())
	stockfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "computer made move:",moves[len(moves)-1]
	print board 
