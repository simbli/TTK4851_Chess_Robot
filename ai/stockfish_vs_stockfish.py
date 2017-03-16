from stockfish import Stockfish
import chess
import time

board = chess.Board()

stockfish = Stockfish()


moves = []

while True:
	moves.append(stockfish.get_best_move())
	stockfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "ai 1 made move:",moves[len(moves)-1]
	print board 

	time.sleep(3)

	moves.append(stockfish.get_best_move())
	stockfish.set_position(moves)
	board.push(chess.Move.from_uci(moves[len(moves)-1]))

	print "ai 2 made move:",moves[len(moves)-1]
	print board 
	print
	time.sleep(3)