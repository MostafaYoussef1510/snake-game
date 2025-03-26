import pygame
import random
from enum import Enum
from collections import namedtuple
import os
import time

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 20
SPEED = 10
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (50, 205, 50)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

BONUS_DURATION = 10  # seconds
BONUS_CHANCE = 0.1  # 10% chance for bonus apple to appear

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hovered = False

    def draw(self, surface):
        color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255)) if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return True
        return False

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game by Mostafa Youssef')
        self.clock = pygame.time.Clock()
        
        # Create buttons
        button_width = 120
        button_height = 50
        spacing = 20
        total_width = (button_width * 2) + spacing
        start_x = (width - total_width) // 2
        button_y = height // 2 + 50
        
        self.retry_button = Button(start_x, button_y, button_width, button_height, "Retry", GREEN)
        self.quit_button = Button(start_x + button_width + spacing, button_y, button_width, button_height, "Quit", RED)
        
        # Show welcome screen
        self.show_welcome_screen()
        self.reset_game()

    def show_welcome_screen(self):
        welcome_duration = 3  # seconds
        start_time = time.time()
        
        while time.time() - start_time < welcome_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    return  # Skip welcome screen if any key is pressed
            
            self.display.fill(BLACK)
            
            # Draw title
            font_large = pygame.font.Font(None, 64)
            title = font_large.render("Snake Game", True, GREEN)
            title_rect = title.get_rect(center=(self.width/2, self.height/3))
            self.display.blit(title, title_rect)
            
            # Draw credits
            font_medium = pygame.font.Font(None, 36)
            credit1 = font_medium.render("Created by", True, WHITE)
            credit2 = font_medium.render("Mostafa Youssef", True, PURPLE)
            credit3 = font_medium.render("Junior Python Game Creator", True, LIGHT_GREEN)
            
            credit1_rect = credit1.get_rect(center=(self.width/2, self.height/2))
            credit2_rect = credit2.get_rect(center=(self.width/2, self.height/2 + 40))
            credit3_rect = credit3.get_rect(center=(self.width/2, self.height/2 + 80))
            
            self.display.blit(credit1, credit1_rect)
            self.display.blit(credit2, credit2_rect)
            self.display.blit(credit3, credit3_rect)
            
            # Draw "Press any key to start"
            font_small = pygame.font.Font(None, 24)
            press_key = font_small.render("Press any key to start", True, GRAY)
            press_key_rect = press_key.get_rect(center=(self.width/2, self.height - 50))
            self.display.blit(press_key, press_key_rect)
            
            pygame.display.flip()
            self.clock.tick(60)

    def reset_game(self):
        # Initialize game state
        self.direction = Direction.RIGHT
        self.head = Point(self.width//2, self.height//2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        self.score = 0
        self.food = None
        self.bonus_food = None
        self.bonus_active = False
        self.bonus_start_time = 0
        self.game_over = False
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
        # Chance to spawn bonus food
        if self.bonus_food is None and random.random() < BONUS_CHANCE:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            bonus_point = Point(x, y)
            if bonus_point not in self.snake and bonus_point != self.food:
                self.bonus_food = bonus_point

    def _is_collision(self):
        if self.bonus_active:
            # When bonus is active, wrap around the screen
            self.head = Point(
                self.head.x % self.width,
                self.head.y % self.height
            )
            return False
        # Hit boundary
        if (self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or 
            self.head.y > self.height - BLOCK_SIZE or self.head.y < 0):
            return True
        # Hit self
        if self.head in self.snake[1:]:
            return True
        return False

    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if self.game_over:
                if self.retry_button.handle_event(event):
                    self.reset_game()
                    return False, self.score
                elif self.quit_button.handle_event(event):
                    pygame.quit()
                    quit()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN

        if not self.game_over:
            # Check if bonus effect should end
            if self.bonus_active and time.time() - self.bonus_start_time >= BONUS_DURATION:
                self.bonus_active = False

            # 2. Move
            self._move(self.direction)
            self.snake.insert(0, self.head)
            
            # 3. Check if game over
            if self._is_collision():
                self.game_over = True
                self._update_ui()
                return True, self.score
            
            # 4. Place new food or move
            if self.head == self.food:
                self.score += 1
                self._place_food()
            elif self.bonus_food and self.head == self.bonus_food:
                self.score += 2
                self.bonus_food = None
                self.bonus_active = True
                self.bonus_start_time = time.time()
            else:
                self.snake.pop()

        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        return self.game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        
        if not self.game_over:
            # Draw snake
            for i, pt in enumerate(self.snake):
                if i == 0:  # Head
                    # Draw snake head with eyes
                    pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                    # Draw eyes
                    eye_radius = 3
                    if self.direction == Direction.RIGHT:
                        pygame.draw.circle(self.display, WHITE, (pt.x + BLOCK_SIZE - 5, pt.y + 5), eye_radius)
                        pygame.draw.circle(self.display, WHITE, (pt.x + BLOCK_SIZE - 5, pt.y + BLOCK_SIZE - 5), eye_radius)
                    elif self.direction == Direction.LEFT:
                        pygame.draw.circle(self.display, WHITE, (pt.x + 5, pt.y + 5), eye_radius)
                        pygame.draw.circle(self.display, WHITE, (pt.x + 5, pt.y + BLOCK_SIZE - 5), eye_radius)
                    elif self.direction == Direction.UP:
                        pygame.draw.circle(self.display, WHITE, (pt.x + 5, pt.y + 5), eye_radius)
                        pygame.draw.circle(self.display, WHITE, (pt.x + BLOCK_SIZE - 5, pt.y + 5), eye_radius)
                    else:  # DOWN
                        pygame.draw.circle(self.display, WHITE, (pt.x + 5, pt.y + BLOCK_SIZE - 5), eye_radius)
                        pygame.draw.circle(self.display, WHITE, (pt.x + BLOCK_SIZE - 5, pt.y + BLOCK_SIZE - 5), eye_radius)
                else:
                    pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
            # Draw regular food (red apple)
            self._draw_apple(self.food.x, self.food.y, RED)
            
            # Draw bonus food (green apple) if it exists
            if self.bonus_food:
                self._draw_apple(self.bonus_food.x, self.bonus_food.y, LIGHT_GREEN)
            
            # Draw bonus timer if active
            if self.bonus_active:
                remaining_time = int(BONUS_DURATION - (time.time() - self.bonus_start_time))
                if remaining_time > 0:
                    font = pygame.font.Font(None, 24)
                    text = font.render(f"Bonus: {remaining_time}s", True, YELLOW)
                    self.display.blit(text, [self.width - 100, 0])
            
            # Draw score
            self._draw_score()
        else:
            # Game Over screen
            font = pygame.font.Font(None, 48)
            game_over_text = f'Game Over! Score: {self.score}\n\nCreated by Mostafa Youssef\nJunior Python Game Creator'
            text = font.render(game_over_text, True, WHITE)
            text_rect = text.get_rect(center=(self.width/2, self.height/2 - 50))
            self.display.blit(text, text_rect)
            
            # Draw buttons
            self.retry_button.draw(self.display)
            self.quit_button.draw(self.display)
        
        pygame.display.flip()

    def _draw_apple(self, x, y, color):
        # Draw main apple body
        pygame.draw.circle(self.display, color, (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), BLOCK_SIZE//2)
        
        # Draw stem
        stem_rect = pygame.Rect(x + BLOCK_SIZE//2 - 2, y, 4, 6)
        pygame.draw.rect(self.display, BROWN, stem_rect)
        
        # Draw leaf
        leaf_points = [
            (x + BLOCK_SIZE//2 + 2, y + 3),
            (x + BLOCK_SIZE//2 + 8, y),
            (x + BLOCK_SIZE//2 + 2, y + 6)
        ]
        pygame.draw.polygon(self.display, DARK_GREEN, leaf_points)
        
        # Add highlight to make apple look shiny
        pygame.draw.circle(self.display, WHITE, (x + BLOCK_SIZE//2 - 3, y + BLOCK_SIZE//2 - 3), 2)

    def _draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)

def main():
    game = SnakeGame()
    
    # Game loop
    while True:
        game_over, score = game.play_step()

if __name__ == '__main__':
    main()
