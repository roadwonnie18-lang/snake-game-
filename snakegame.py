from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 1000
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    draw_hat(x, y)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(game_speed, next_turn, snake, food)

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

def check_collisions(snake):

    x, y = snake.coordinates[0]


    if x < 0 or x >= GAME_WIDTH:
       return True
    elif y < 0 or y >= GAME_HEIGHT:
       return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global restart_button
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    restart_button = Button(window, text="Play Again", font=('consolas', 20), command=restart_game)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 80, window=restart_button)

def restart_game():
    global snake, food, score, direction, restart_button

    if restart_button is not None:
        restart_button.destroy()
        restart_button = None

        show_difficulty_screen()

        canvas.delete(ALL)

        score = 0
        direction = 'down'
        label.config(text="score:{}".format(score))
        draw_grid()
        snake = Snake()
        food = Food()
        draw_hat(snake.coordinates[0][0], snake.coordinates[0][1])

        next_turn(snake, food)

def draw_grid():
    for i in range (0, GAME_WIDTH,SPACE_SIZE):
        canvas.create_line(i, 0, i, GAME_HEIGHT, fill="#1a1a1a", tag="grid")
    for i in range (0, GAME_HEIGHT,SPACE_SIZE):
        canvas.create_line( 0, i, GAME_WIDTH, i, fill="#1a1a1a", tag="grid")

def draw_hat(x, y):
    canvas.delete("hat")
    if not hat_enabled:
        return
    canvas.create_polygon(
        x + SPACE_SIZE / 2, y - SPACE_SIZE,
        x, y,
        x + SPACE_SIZE, y,
        fill="blue", outline="white", tag="hat"
    )
    canvas.create_oval(
        x + SPACE_SIZE / 2 - 6, y - SPACE_SIZE - 12,
        x + SPACE_SIZE / 2 + 6, y - SPACE_SIZE,
        fill="yellow", tag="hat"
    )

def toggle_hat():
    global hat_enabled
    hat_enabled = not hat_enabled
    draw_hat(snake.coordinates[0][0], snake.coordinates[0][1])

def start_game(speed):
    global snake, food, score, direction, game_speed, difficulty_buttons

    game_speed = speed

    for btn in difficulty_buttons:
        btn.destroy()
    difficulty_buttons = []

    canvas.delete(ALL)

    draw_grid()

    snake = Snake()
    food = Food()

    draw_hat(snake.coordinates[0][0], snake.coordinates[0][1])
    next_turn(snake, food)

def show_difficulty_screen():
    global difficulty_buttons

    canvas.delete(ALL)
    draw_grid()

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 150,
                       font=('consolas', 50), text="Choose Difficulty", fill="white", tag="difficulty")


    easy_btn = Button(window, text="Easy", font=('consolas', 20), width=10,
                      command=lambda: start_game(150))
    medium_btn = Button(window, text="Medium", font=('consolas', 20), width=10,
                      command=lambda: start_game(90))
    hard_btn = Button(window, text="HARD", font=('consolas', 20), width=10,
                      command=lambda: start_game(50))

    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 90, window=easy_btn)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 45, window=medium_btn)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 5, window=hard_btn)

    difficulty_buttons = [easy_btn, medium_btn, hard_btn]

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
restart_button = None
hat_enabled = True
difficlty_buttons = []
game_speed = 100


label = Label(window, text="score:{}".format(score), font=('consolas', 40))
label.pack()

controls_label = Label(window, text="Controls: The Arrow Keys", font=('consolas', 14))
controls_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
hat_button = Button(window, text="toggle Hat", font=('consolas', 14), command=toggle_hat)
hat_button.pack()

window.update()

window_with = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_with / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_with}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

show_difficulty_screen()

window.mainloop()
