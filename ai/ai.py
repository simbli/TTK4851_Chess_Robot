from stockfish import Stockfish
import chess


class AI():

	def __init__(self):
		self.board = chess.Board()
		self.stockfish = Stockfish()
		self.moves = []
	
	#generates move with stockfish, makes the move and returns the move to send it to the robot.
	def get_move_stockfish(self):
		self.stockfish.set_position(self.moves)
		self.moves.append(self.stockfish.get_best_move())
		self.board.push(chess.Move.from_uci(self.moves[len(self.moves)-1]))
		
		print "Move made by ai:",self.moves[len(self.moves)-1]
		print self.board 
		
		return self.moves[len(self.moves)-1]


	#Adds the players move to the move list and the board representation.
	def set_move(self, move):
		self.moves.append(move)
		self.board.push(chess.Move.from_uci(self.moves[len(self.moves)-1]))

