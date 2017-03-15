import Tkinter
window = Tkinter.Tk()
window_width = 800
window_height = 600
def LOOOL():
	text_field.config(text = "TEST")

window.title("Chess robot")

text_field = Tkinter.Label(window, text = "LOOOOOL", font="Helvetica 55 bold italic")

text_field.place(relx= 0.5, rely = 0.3, anchor='center')

startButton = Tkinter.Button(window, text = "LOOOL", command = LOOOL)
startButton.place(relx = 0.5, rely=0.6, anchor='center')
window.geometry(str(window_width)+"x"+str(window_height))
window.mainloop()
