import socket
import ai.ai as artint
import Tkinter
import time

GUI = False

def send_move(moves):
	for i in range(len(moves)):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1', 5005))
		s.send(moves[i])
		s.close()
		time.sleep(15)


def createGUI():
	window = Tkinter.Tk()
	text_field = Tkinter.Label(window, text = "LOOOOOL", font="Helvetica 55 bold italic")


	window_width = 800
	window_height = 600
	def LOOOL():
		print "LOOOL"

	window.title("Chess robot")


	text_field.place(relx= 0.5, rely = 0.3, anchor='center')

	startButton = Tkinter.Button(window, text = "LOOOL", command = LOOOL)
	startButton.place(relx = 0.5, rely=0.6, anchor='center')
	window.geometry(str(window_width)+"x"+str(window_height))

def update_label(label_text):
	if GUI:
		text_field.config(text=label_text)
		window.update_idletasks()
		time.sleep(1)



def main():
	ai = artint.AI()
	if GUI:
		createGUI()



	while not ai.game_over():
		#get move made by the player from computer vision
		move = raw_input("Next Move:")

		#Makes the move on the board
		ai.set_move(move)
		update_label("TEST")

		#calculate robot move with ai
		moves = ai.get_move_stockfish()

		#send move to robot
		#send_move(moves)


if __name__ == "__main__":
	main()

window.mainloop()
