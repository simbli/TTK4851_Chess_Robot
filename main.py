import socket
import ai.ai as artint


def send_move(move):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 5005))
	s.send(move)
	s.close()

def main():
	ai = artint.AI()

	while True:
		#get move made by the player from computer vision
		move = raw_input("Next Move:")

		#Makes the move on the board
		ai.set_move(move)

		#calculate robot move with ai
		move = ai.get_move_stockfish()

		#send move to robot
		send_move(move)


if __name__ == "__main__":
	main()
	