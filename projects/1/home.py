import turtle
import random

# Setup the turtle screen
screen = turtle.Screen()
screen.bgcolor("darkblue")  # Background color for the sky
screen.title("House Drawing")

# Create the turtle
pen = turtle.Turtle()
pen.speed(3)

# Draw the base of the house
pen.penup()
pen.goto(-100, -150)  # Start position for the base
pen.pendown()
pen.fillcolor("lightblue")
pen.begin_fill()
for _ in range(2):
    pen.forward(200)  # Width of the house
    pen.left(90)
    pen.forward(150)  # Height of the house
    pen.left(90)
pen.end_fill()

# Draw the roof
pen.fillcolor("brown")
pen.begin_fill()
pen.goto(-100, 0)  # Bottom-left corner of the roof
pen.goto(0, 100)  # Peak of the roof
pen.goto(100, 0)  # Bottom-right corner of the roof
pen.goto(-100, 0)  # Back to the starting point of the roof
pen.end_fill()

# Draw the door
pen.penup()
pen.goto(-30, -150)  # Bottom-left corner of the door
pen.pendown()
pen.fillcolor("darkblue")
pen.begin_fill()
pen.setheading(90)  # Point the turtle upwards
for _ in range(2):
    pen.forward(75)  # Door height
    pen.right(90)
    pen.forward(50)  # Door width
    pen.right(90)
pen.end_fill()

# Draw the first window
pen.penup()
pen.goto(40, -60)  # Bottom-left corner of the first window
pen.pendown()
pen.fillcolor("yellow")
pen.begin_fill()
for _ in range(4):
    pen.forward(40)  # Window size
    pen.right(90)
pen.end_fill()

# Draw the second window
pen.penup()
pen.goto(-80, -60)  # Bottom-left corner of the second window (on the left)
pen.pendown()
pen.fillcolor("yellow")
pen.begin_fill()
for _ in range(4):
    pen.forward(40)  # Window size
    pen.right(90)
pen.end_fill()

# Function to draw stars (star shape instead of dots)
def draw_star(x, y, size):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color("yellow")
    pen.setheading(random.randint(0, 360))  # Randomize the angle to make stars look different
    for _ in range(5):  # Draw a 5-pointed star
        pen.forward(size)
        pen.right(144)  # Angle for a 5-point star
        pen.forward(size)
        pen.right(72)

# Draw random stars in the sky
for _ in range(50):  # Number of stars
    x_pos = random.randint(-200, 200)  # Random x position
    y_pos = random.randint(50, 200)   # Random y position (above the house)
    size = random.randint(5, 10)  # Random size of the stars
    draw_star(x_pos, y_pos, size)

# Finish up
pen.hideturtle()
screen.mainloop()
