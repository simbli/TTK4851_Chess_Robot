from stockfish import Stockfish
import chess
import time

board = chess.Board()

shallowfish = Stockfish(depth=17)
deepfish = Stockfish(depth=17)



moves = []

while True:
	if board.is_game_over():
		break
	#raw_input("Press enter to continue...")
	moves.append(shallowfish.get_best_move())
	shallowfish.set_position(moves)
	deepfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "ai 1 made move:",moves[len(moves)-1]
	print board 

	if board.is_game_over():
		break

	moves.append(deepfish.get_best_move())
	shallowfish.set_position(moves)
	deepfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "ai 2 made move:",moves[len(moves)-1]
	print board 
	print

print board.result()