from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from collections import deque
import random
import time

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize game state
        self.BLOCK_SIZE = 40  # Larger for touch screens
        self.SPEED = 0.15  # slightly slower for mobile
        self.score = 0
        self.bonus_active = False
        self.bonus_start_time = 0
        self.BONUS_DURATION = 10
        
        # Colors
        self.RED = (1, 0, 0, 1)
        self.GREEN = (0, 1, 0, 1)
        self.BLUE = (0, 0, 1, 1)
        self.WHITE = (1, 1, 1, 1)
        self.PURPLE = (0.5, 0, 0.5, 1)
        
        # Initialize snake
        self.snake = deque([(3, 10), (2, 10), (1, 10)])
        self.direction = 'right'
        self.next_direction = 'right'
        
        # Place initial food
        self.food = self._place_food()
        self.bonus_food = None
        
        # Add welcome screen
        self.show_welcome = True
        self.game_started = False
        
        # Add score label with larger font for mobile
        self.score_label = Label(
            text='Score: 0',
            pos=(10, Window.height - 50),
            size_hint=(None, None),
            font_size='24sp'
        )
        self.add_widget(self.score_label)
        
        # Add bonus timer label
        self.bonus_label = Label(
            text='',
            pos=(Window.width - 150, Window.height - 50),
            size_hint=(None, None),
            font_size='24sp'
        )
        self.add_widget(self.bonus_label)
        
        # Start game loop
        Clock.schedule_interval(self.update, self.SPEED)

    def on_touch_down(self, touch):
        if self.show_welcome:
            self.show_welcome = False
            self.game_started = True
            return True
            
        self.touch_start_x = touch.x
        self.touch_start_y = touch.y
        return True

    def update(self, dt):
        if self.show_welcome:
            self.draw_welcome_screen()
            return True
            
        if not self.game_started:
            return True
            
        # Update direction
        self.direction = self.next_direction
        
        # Get head position
        head_x, head_y = self.snake[0]
        
        # Move head
        if self.direction == 'up':
            head_y += 1
        elif self.direction == 'down':
            head_y -= 1
        elif self.direction == 'left':
            head_x -= 1
        elif self.direction == 'right':
            head_x += 1
        
        # Check if bonus should end
        if self.bonus_active and time.time() - self.bonus_start_time >= self.BONUS_DURATION:
            self.bonus_active = False
            self.bonus_label.text = ''
        
        # Handle wall collision or wrapping
        if self.bonus_active:
            head_x = head_x % (Window.width // self.BLOCK_SIZE)
            head_y = head_y % (Window.height // self.BLOCK_SIZE)
        else:
            if (head_x < 0 or head_x >= Window.width // self.BLOCK_SIZE or
                head_y < 0 or head_y >= Window.height // self.BLOCK_SIZE):
                self.game_over()
                return False
        
        # Check self collision
        if (head_x, head_y) in self.snake:
            self.game_over()
            return False
        
        # Move snake
        self.snake.appendleft((head_x, head_y))
        
        # Check for food collision
        if (head_x, head_y) == self.food:
            self.score += 1
            self.score_label.text = f'Score: {self.score}'
            self.food = self._place_food()
            
            # Maybe spawn bonus food
            if self.bonus_food is None and random.random() < 0.1:  # 10% chance
                self.bonus_food = self._place_food()
        elif self.bonus_food and (head_x, head_y) == self.bonus_food:
            self.score += 2
            self.score_label.text = f'Score: {self.score}'
            self.bonus_food = None
            self.bonus_active = True
            self.bonus_start_time = time.time()
        else:
            self.snake.pop()
        
        # Update bonus timer
        if self.bonus_active:
            remaining = int(self.BONUS_DURATION - (time.time() - self.bonus_start_time))
            if remaining > 0:
                self.bonus_label.text = f'Bonus: {remaining}s'
            else:
                self.bonus_label.text = ''
        
        # Redraw
        self.draw()

    def draw_welcome_screen(self):
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(0, 0, 0, 1)  # Black
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))
            
            # Title
            title_label = Label(
                text='Snake Game',
                font_size='48sp',
                pos=(Window.width/2, Window.height * 0.7),
                color=self.GREEN
            )
            title_label.texture_update()
            
            # Credits
            credits1 = Label(
                text='Created by',
                font_size='24sp',
                pos=(Window.width/2, Window.height * 0.5),
                color=self.WHITE
            )
            credits2 = Label(
                text='Mostafa Youssef',
                font_size='32sp',
                pos=(Window.width/2, Window.height * 0.4),
                color=self.PURPLE
            )
            credits3 = Label(
                text='Junior Python Game Creator',
                font_size='24sp',
                pos=(Window.width/2, Window.height * 0.3),
                color=self.GREEN
            )
            
            # Start instruction
            start_label = Label(
                text='Tap anywhere to start',
                font_size='20sp',
                pos=(Window.width/2, Window.height * 0.1),
                color=(0.5, 0.5, 0.5, 1)  # Gray
            )
            
            title_label.draw()
            credits1.draw()
            credits2.draw()
            credits3.draw()
            start_label.draw()

    def draw(self):
        self.canvas.clear()
        
        # Draw snake
        with self.canvas:
            for i, (x, y) in enumerate(self.snake):
                if i == 0:  # Head
                    Color(*self.BLUE)
                else:  # Body
                    Color(0, 0, 0.8, 1)
                Rectangle(
                    pos=(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE),
                    size=(self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
                )
        
        # Draw food
        with self.canvas:
            # Regular food (red apple)
            Color(*self.RED)
            Ellipse(
                pos=(self.food[0] * self.BLOCK_SIZE, self.food[1] * self.BLOCK_SIZE),
                size=(self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
            )
            
            # Bonus food (green apple)
            if self.bonus_food:
                Color(*self.GREEN)
                Ellipse(
                    pos=(self.bonus_food[0] * self.BLOCK_SIZE, self.bonus_food[1] * self.BLOCK_SIZE),
                    size=(self.BLOCK_SIZE - 2, self.BLOCK_SIZE - 2)
                )

    def _place_food(self):
        while True:
            x = random.randint(0, (Window.width - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            y = random.randint(0, (Window.height - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            if (x, y) not in self.snake:
                return (x, y)

    def on_touch_up(self, touch):
        # Calculate swipe direction
        dx = touch.x - self.touch_start_x
        dy = touch.y - self.touch_start_y
        
        # Determine which direction had the larger movement
        if abs(dx) > abs(dy):
            if dx > 0 and self.direction != 'left':
                self.next_direction = 'right'
            elif dx < 0 and self.direction != 'right':
                self.next_direction = 'left'
        else:
            if dy > 0 and self.direction != 'down':
                self.next_direction = 'up'
            elif dy < 0 and self.direction != 'up':
                self.next_direction = 'down'

    def game_over(self):
        content = Widget()
        
        # Create popup content with credits
        game_over_text = f'Game Over!\nScore: {self.score}\n\nCreated by\nMostafa Youssef\nJunior Python Game Creator'
        score_label = Label(
            text=game_over_text,
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_size='24sp'
        )
        
        retry_button = Button(
            text='Retry',
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.3, 'center_y': 0.3},
            font_size='24sp'
        )
        quit_button = Button(
            text='Quit',
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.7, 'center_y': 0.3},
            font_size='24sp'
        )
        
        content.add_widget(score_label)
        content.add_widget(retry_button)
        content.add_widget(quit_button)
        
        # Create and show popup
        popup = Popup(
            title='Game Over',
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=False
        )
        
        def retry(instance):
            self.__init__()
            popup.dismiss()
            
        def quit(instance):
            App.get_running_app().stop()
            
        retry_button.bind(on_press=retry)
        quit_button.bind(on_press=quit)
        
        popup.open()

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

if __name__ == '__main__':
    SnakeApp().run()
