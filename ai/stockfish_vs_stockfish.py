from stockfish import Stockfish
import chess
import time

board = chess.Board()

stockfish = Stockfish(depth=2)
stockfish2 = Stockfish(depth=20)

moves = []

while True:
	moves.append(stockfish.get_best_move())
	stockfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "shallow AI made move:",moves[len(moves)-1]
	print board 

	time.sleep(3)

	moves.append(stockfish2.get_best_move())
	stockfish2.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "deep AI made move:",moves[len(moves)-1]
	print board 
	print
	print
	time.sleep(3)