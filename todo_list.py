import pygame
import sys
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("To-Do List")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREY = (200, 200, 200)
LIGHT_GREY = (240, 240, 240)
GREEN = (0, 200, 100)

# Font
font = pygame.font.Font(None, 36)
header_font = pygame.font.Font(None, 48)

# To-do and completed tasks
todo_list = ["Task 1", "Task 2", "Task 3"]
completed_tasks = []

# Input box variables
input_box = pygame.Rect(350, 100, 300, 36)
input_text = ''
input_active = False

# Buttons
clear_completed_button = pygame.Rect(WIDTH - 200, HEIGHT - 50, 200, 40)

# Current screen
current_screen = "To-Do"

# Save and load functions
def save_tasks():
    with open('tasks.txt', 'w') as file:
        for task in todo_list:
            file.write(f"{task},False\n")
        for task, date in completed_tasks:
            file.write(f"{task},True,{date}\n")

def load_tasks():
    global todo_list, completed_tasks
    if os.path.exists('tasks.txt'):
        with open('tasks.txt', 'r') as file:
            todo_list = []
            completed_tasks = []
            for line in file:
                parts = line.strip().split(',')
                task = parts[0]
                checked = parts[1] == 'True'
                if checked and len(parts) > 2:
                    date = parts[2]
                    completed_tasks.append((task, date))
                elif not checked:
                    todo_list.append(task)

def draw_gradient():
    for i in range(HEIGHT):
        color = (35, min(255, i // 2), min(255, 102 + i // 3))
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def draw_tabs():
    # Top Tabs Background
    pygame.draw.rect(screen, LIGHT_GREY, (0, 0, WIDTH, 60))
    pygame.draw.line(screen, WHITE, (0, 60), (WIDTH, 60), 3)

    # To-Do Tab
    todo_color = WHITE if current_screen == "To-Do" else GREY
    todo_tab = pygame.Rect(0, 0, WIDTH // 2, 60)
    pygame.draw.rect(screen, todo_color, todo_tab)
    todo_text = font.render("To-Do", True, BLACK)
    screen.blit(todo_text, (WIDTH // 4 - 30, 15))

    # Completed Tab
    completed_color = WHITE if current_screen == "Completed" else GREY
    completed_tab = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, 60)
    pygame.draw.rect(screen, completed_color, completed_tab)
    completed_text = font.render("Completed", True, BLACK)
    screen.blit(completed_text, (3 * WIDTH // 4 - 60, 15))

def draw_input_box():
    color = BLUE if input_active else GREY
    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    input_box.w = max(300, text_surface.get_width() + 10)

def draw_todo_list():
    y = 150
    for i, task in enumerate(todo_list):
        checkbox = pygame.Rect(50, y, 20, 20)
        pygame.draw.rect(screen, WHITE, checkbox)
        pygame.draw.rect(screen, BLACK, checkbox, 2)
        task_surface = font.render(task, True, BLACK)
        screen.blit(task_surface, (80, y - 5))
        y += 40

def draw_completed_list():
    y = 150
    for task, date in completed_tasks:
        task_surface = font.render(f"{task} (Completed on {date})", True, BLACK)
        screen.blit(task_surface, (50, y))
        y += 40

def draw_clear_completed_button():
    pygame.draw.rect(screen, RED, clear_completed_button)
    button_text = font.render("Clear Completed", True, WHITE)
    screen.blit(button_text, (clear_completed_button.x + 10, clear_completed_button.y + 5))

# Main loop
load_tasks()
running = True
while running:
    screen.fill(WHITE)
    draw_gradient()
    draw_tabs()

    if current_screen == "To-Do":
        draw_input_box()
        draw_todo_list()
    elif current_screen == "Completed":
        draw_completed_list()
        draw_clear_completed_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False

            # Handle tab switching
            if pygame.Rect(0, 0, WIDTH // 2, 60).collidepoint(event.pos):
                current_screen = "To-Do"
            elif pygame.Rect(WIDTH // 2, 0, WIDTH // 2, 60).collidepoint(event.pos):
                current_screen = "Completed"

            # Handle clear completed button
            if clear_completed_button.collidepoint(event.pos) and current_screen == "Completed":
                completed_tasks = []

        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        todo_list.append(input_text.strip())
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Handle checkbox clicks
        if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "To-Do":
            y = 150
            for i, task in enumerate(todo_list):
                checkbox = pygame.Rect(50, y, 20, 20)
                if checkbox.collidepoint(event.pos):
                    date = datetime.now().strftime("%Y-%m-%d")
                    completed_tasks.append((task, date))
                    todo_list.pop(i)
                    break
                y += 40

    pygame.display.flip()

save_tasks()
pygame.quit()