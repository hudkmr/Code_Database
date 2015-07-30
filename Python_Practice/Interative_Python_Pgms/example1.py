import simplegui

message = "Hello World"

def click():
	global message
	message = "Good Job!"
	
def draw(canvas):
	canvas.draw_test(message, [50,112], 48, "Red")
	
frame = simplegui.create_frame("Home",300,200)
frame.add_button("Click me", click)
frame.set_draw_handler(draw)

frame.start()