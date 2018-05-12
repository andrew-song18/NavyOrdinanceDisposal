#player setup over spring break through turtle
#week 1: set up of turtle and user control, imported libraries
#week 2: tijuana immersion, didn't really work on code as much as I would have wanted to
#week 3: create boundaries detection and draw borders, initial listening of keyboard
#week 4: defined collision if turtle hits boundaries. Created github repository. Created "mine" class
#week 4 cont: having hard time with user detecting collision with "mine" class.
#week 5: Recreated "mine" class to be more functionable
#week 6: game class created, mine and user collison now works
#week 7: created shell class, figured out code was broken because failed to intilialize shells to emerge from mine after explosion
#week 8: Blitting and using images to replace simple surrogate polygons, emphasizing aesthetic gameplay.
#week 9: scoreboard, TBD must blit turtle,landmines,background. Customize

#import libraries

import random
import time
import turtle 

bgTurtle = turtle
screenTurtle = bgTurtle.getscreen()
screenTurtle.bgpic("ocean.gif")

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor('blue')
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

class Sprite(turtle.Turtle):
	def __init__(self, spriteshape, color, startx, starty):
		turtle.Turtle.__init__(self, shape = spriteshape)
		self.speed(0)
		self.penup()
		self.color(color)
		self.fd(0)
		self.goto(startx, starty)
		self.speed = 1
		
	def move(self):
		self.fd(self.speed)
		
		#Boundary detection
		if self.xcor() > 290:
			self.setx(290)
			self.rt(60)
		
		if self.xcor() < -290:
			self.setx(-290)
			self.rt(60)
		
		if self.ycor() > 290:
			self.sety(290)
			self.rt(60)
		
		if self.ycor() < -290:
			self.sety(-290)
			self.rt(60)
			
	def is_collision(self, other):
		if (self.xcor() >= (other.xcor() - 20)) and \
		(self.xcor() <= (other.xcor() + 20)) and \
		(self.ycor() >= (other.ycor() - 20)) and \
		(self.ycor() <= (other.ycor() + 20)):
			return True
		else:
			return False
				
class Player(Sprite):
	def __init__(self, spriteshape, color, startx, starty):
		Sprite.__init__(self, spriteshape, color, startx, starty)
		s = turtle.Screen()
		image = "BattleShip.gif"
		s.addshape(image)
		self.shape(image)
		s.bgcolor("black")
		self.shapesize(stretch_wid=1.8, stretch_len=1.2, outline=None)
		self.speed = 5
		self.lives = 3

	def turn_left(self):
		self.lt(45)
		
	def turn_right(self):
		self.rt(45)
		
	def decelerate(self):
		self.speed -= 1
		
class Landmine(Sprite):
	def __init__(self, spriteshape, color, startx, starty):
		Sprite.__init__(self, spriteshape, color, startx, starty)
		self.speed = 0
		self.setheading(random.randint(0,360))

class Torpedo(Sprite):
	def __init__(self, spriteshape, color, startx, starty):
		Sprite.__init__(self, spriteshape, color, startx, starty)
		self.speed = 2
		self.setheading(random.randint(0,360))

class Shell(Sprite):
	def __init__(self, spriteshape, color, startx, starty):
		Sprite.__init__(self, spriteshape, color, startx, starty)
		self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
		self.goto(-1000,-1000)
		self.frame = 0
		
	def explode(self, startx, starty):
		self.goto(startx,starty)
		self.setheading(random.randint(0,360))
		self.frame = 3

	def move(self):
		if self.frame > 0:
			self.fd(10)
			self.frame += 1

		if self.frame > 15:
			self.frame = 0
			self.goto(-1000, -1000)

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
		msg = "Landmines: %s" %(self.score+19)
		self.pen.penup()
		self.pen.goto(-50, 310)
		self.pen.write(msg, font=("Times New Roman", 18, "normal"))

game = Game()

game.draw_border()

game.show_status()

player = Player("triangle", "black", -160, 0)

Landmines =[]
for i in range(10):
	Landmines.append(Landmine("square", "blue", -120, 0))

Torpedoes =[]
for i in range(3):
	Torpedoes.append(Torpedo("triangle", "red", -120, 0))

shells = []
for i in range(45):
	shells.append(Shell("circle", "orange", 10, 0))

#Keyboard bindings
turtle.onkey(player.turn_left, "Right")
turtle.onkey(player.turn_right, "Left")
turtle.onkey(player.decelerate, "Down")
turtle.listen()

# screen = pygame.display.set_mode([800, 800], 0, 32)
# image1 = pygame.image.load('ocean.jpg')
# screen.blit(image1, [200, 200])

#Main game loop
while True:
	turtle.update()
	time.sleep(0.02)

	player.move()
	
	for Landmine in Landmines:
		Landmine.move()
		
		#Check for a trigger with player
		if player.is_collision(Landmine):
			x = random.randint(-250, 250)
			y = random.randint(-250, 250)
			Landmine.goto(x, y)
			game.score += 1
			game.show_status()
			for shell in shells:
				shell.explode(player.xcor(), player.ycor())

	for Torpedo in Torpedoes:
		Torpedo.move()
		
		#Check for a trigger with player
		if player.is_collision(Torpedo):
			x = random.randint(-250, 250)
			y = random.randint(-250, 250)
			Torpedo.goto(x, y)
			game.score -=10
			game.show_status()
			for shell in shells:
				shell.explode(player.xcor(), player.ycor())

	for shell in shells:
		shell.move() 




    


