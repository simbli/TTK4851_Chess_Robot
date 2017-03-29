from stockfish import Stockfish
import chess


class AI():

	def __init__(self):
		self.board = chess.Board()
		self.stockfish = Stockfish(depth=2)
		self.moves = []

	def game_over(self):
		return self.board.is_game_over()

	#generates move with stockfish, makes the move and returns the move to send it to the robot.
	def get_move_stockfish(self):
		self.stockfish.set_position(self.moves)
		bestMove = self.stockfish.get_best_move()
		self.moves.append(bestMove)
		currentMove = chess.Move.from_uci(self.moves[len(self.moves)-1]);
		print "CURRENT MOVE:",currentMove

		moveList = []
		print bestMove[0:2]
		print bestMove[2:4]

		if self.board.is_capture(currentMove):
			if self.board.is_en_passant(currentMove):
				print "EN PASSANT!!!!"
				moveList.append(bestMove[2:3] + chr(ord(bestMove[3:4]) + 1) + "j8")
				moveList.append(bestMove)

			else:
				print "CAPTURE!!!!"
				moveList.append(bestMove[2:4]+"n9")
				moveList.append(bestMove)
		elif self.board.is_kingside_castling(currentMove):
			print "KINGSIDE CASTLE!!!"
			moveList.append(bestMove)
			moveList.append("h8f8")
		elif self.board.is_queenside_castling(currentMove):
			print "QUEENSIDE CASTLE!!!"
			moveList.append(bestMove)
			moveList.append("a8d8")
		else:
			moveList.append(bestMove)


		print "Move made by ai:",self.moves[len(self.moves)-1]
		self.board.push(currentMove)
		print self.board

		return moveList


	#Adds the players move to the move list and the board representation.
	def set_move(self, move):
		if move is False or None:
			return False
		else:
			self.moves.append(move)
			currentMove = chess.Move.from_uci(self.moves[len(self.moves)-1])

			self.board.push(currentMove)
			return True


if __name__ == "__main__":
	ai = AI()
	ai.loopshit()
