import socket
import ai.ai as artint
import Tkinter
import time
import computervision.cv as cv

GUI = False

def send_move(moves):
	for i in range(len(moves)):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1', 5005))
		s.send(moves[i])
		s.close()
		get_response()

def get_response():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 5006))
	s.listen(1)

	conn, addr = s.accept()
	print 'Connection address:', addr
	while 1:
	    data = conn.recv(1024)
	    if not data: break
	    print "received data:", data
	    conn.send(data)  # echo
	conn.close()

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
	c = cv.Compvision()
	ai = artint.AI()
	if GUI:
		createGUI()



	while not ai.game_over():
		#get move made by the player from computer vision
		move = raw_input('White player: take your move, then press Enter')
		move = c.get_move()
		if (True):
			print "White players move: {}".format(move)
			#Makes the move on the board
			ai.set_move(move)

			#calculate robot move with ai
			moves = ai.get_move_stockfish()
			#raw_input('Black player: take your move, then press Enter')
			#send move to robot
			send_move(moves)
			move = c.get_move()
			print "Black players move: {}".format(move)

if __name__ == "__main__":
	main()

#window.mainloop()
