#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Python Snake
# ************************************
from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 25
BODY_PARTS = 3
AI_BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
AI_SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
class AI_snake:

    def __init__(self):
        self.body_size = AI_BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0, AI_BODY_PARTS):
            self.coordinates.append([400, 400])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=AI_SNAKE_COLOR, tag="ai_snake")
            self.squares.append(square)
    

class Food:

    def __init__(self):
        
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, ai_snake, food):

    x, y = snake.coordinates[0]
    x2,y2 = ai_snake.coordinates[0]
    x_goal,y_goal = food.coordinates
    global ai_direction
    #our snake logic here
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    if((x_goal<x2 and y_goal<y2)  or  (x_goal>x2 and y_goal<y2)):
        
        change_ai_direction("up",ai_snake)
        
        if(flag == False):
            if(x_goal<x2):
                change_ai_direction("left",ai_snake)
            else:
                change_ai_direction("right",ai_snake)
        
    elif( (x_goal<x2 and y_goal>y2) or (x_goal>x2 and y_goal>y2) ):
        
        change_ai_direction("down",ai_snake)
        
        if(flag == False):
            
            if(x_goal<x2):
                change_ai_direction("left",ai_snake)
            else:
                change_ai_direction("right",ai_snake)
    else:
        if(x_goal<x2):
            change_ai_direction("left",ai_snake)
        elif(x_goal>x2):
            change_ai_direction("right",ai_snake)
        elif(y_goal>y2):
            change_ai_direction("down",ai_snake)
        elif(y_goal<y2):
            change_ai_direction("up",ai_snake)
            

    x2,y2 = ai_snake.coordinates[0]
    
    #ai_snake coordinates already inserted so dont repeat
    snake.coordinates.insert(0, (x, y))
   

    #fill the squares for both
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    square2 = canvas.create_rectangle(x2, y2, x2 + SPACE_SIZE, y2 + SPACE_SIZE, fill=AI_SNAKE_COLOR)
    
    snake.squares.insert(0, square)
    ai_snake.squares.insert(0,square2)

    
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        global BODY_PARTS

        score += 1
        BODY_PARTS+=1

        label.config(text=f"YOUR SCORE : {score}  SNAKE LENGTH : {BODY_PARTS}")
        
        canvas.delete("food")

        food = Food()
        
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
        
        
    if x2 == food.coordinates[0] and y2 == food.coordinates[1]:
        
        global ai_score
        global AI_BODY_PARTS

        ai_score += 1
        AI_BODY_PARTS+=1
        label2.config(text=f"AI SCORE:{ai_score}  AI SNAKE LENGTH:{AI_BODY_PARTS}")
        
        canvas.delete("food")

        food = Food()

    else:
        
        del ai_snake.coordinates[-1]
        canvas.delete(ai_snake.squares[-1])
        del ai_snake.squares[-1]

    if check_collisions(snake,ai_snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, ai_snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def change_ai_direction(new_direction, ai_snake):
    
    global ai_direction, flag
    flag = False
    x,y = ai_snake.coordinates[0]

    if new_direction == 'left':
        if ai_direction != 'right':
            flag = True
            ai_direction = new_direction
            x-=SPACE_SIZE
            
    elif new_direction == 'right':
        if ai_direction != 'left':
            flag = True
            ai_direction = new_direction
            x+=SPACE_SIZE
            
    elif new_direction == 'up':
        if ai_direction != 'down':
            flag = True
            ai_direction = new_direction
            y-=SPACE_SIZE
            
    elif new_direction == 'down':
        if ai_direction != 'up':
            flag = True
            ai_direction = new_direction
            y+=SPACE_SIZE
    
    ai_snake.coordinates.insert(0, (x, y))



def check_collisions(snake,ai_snake):

    x, y = snake.coordinates[0]
    
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    for body_part in ai_snake.coordinates[:]:
        for i in snake.coordinates[:]:
            if(i == body_part):
                return True
                
    return False


def game_over():
    global score,ai_score
    
    canvas.delete("food")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    
    if(score > ai_score):
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/4,
                           font=('consolas',70), text="YOU WIN", fill="green", tag="snake_wins")
    elif (score < ai_score):
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/4,
                       font=('consolas',70), text="YOU LOSE", fill="red", tag="AI_snake wins")
    else:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/4,
                       font=('consolas',70), text="DRAW", fill="yellow", tag="AI_snake wins")
    
    


window = Tk()
window.title("Snake Vs AI_Snake game")
window.resizable(False, False)

score = 0
ai_score = 0
direction = 'down'
ai_direction = 'up'
flag = True

label = Label(window, text=f"YOUR SCORE:{score}  SNAKE LENGTH:{BODY_PARTS}", font=('consolas', 20))
label2 = Label(window, text=f"AI SCORE:{ai_score}  AI SNAKE LENGTH:{AI_BODY_PARTS}", font=('consolas',20))

label.pack()
label2.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
ai_snake = AI_snake()
food = Food()

next_turn(snake,ai_snake,food)

window.mainloop()


# In[ ]:





# In[ ]:




