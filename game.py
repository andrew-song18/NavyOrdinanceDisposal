class Game():
	def __init__(self):
		self.level = 0
		self.score = 1
		self.state = "playing"
		self.pen = turtle.Turtle()
		
	def draw_border(self):
		#Draw border
		self.pen.speed(0)
		self.pen.color("white")
		self.pen.pensize(3)
		self.pen.penup()
		self.pen.goto(-300, 300)
		self.pen.pendown()
		for side in range(4):
			self.pen.fd(600)
			self.pen.rt(90)
		self.pen.penup()
		self.pen.ht()
		self.pen.pendown()
		
	def show_status(self):
		self.pen.undo()
		msg = "Landmines: %s" %(self.score+9)
		self.pen.penup()
		self.pen.goto(-50, 310)
		self.pen.write(msg, font=("Times New Roman", 18, "normal"))