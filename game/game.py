
import random

from .snake import Snake


class Game:
    def __init__(self, w, h, speed=8):
        self.w = w
        self.h = h
        self.base_speed = speed
        self.score = 0
        self.is_over = False
        self.paused = False
        start = (w // 2, h // 2)
        self.snake = Snake(start, direction=(1, 0), length=3)
        self.food = None
        self.spawn_food()


    @property
    def level(self) -> int:
        return 1 + self.score // 5

    @property
    def speed(self) -> float:

        return self.base_speed + (self.level - 1) * 1.5

    @property
    def tick_interval(self) -> float:
        return 1.0 / self.speed


    def free_cells(self):
        occupied = set(self.snake.body)
        return [
            (x, y)
            for x in range(self.w)
            for y in range(self.h)
            if (x, y) not in occupied
        ]

    def spawn_food(self):
        cells = self.free_cells()
        self.food = random.choice(cells) if cells else None
        return self.food


    def step(self, direction=None):

        if self.is_over or self.paused:
            return False

        if direction is not None:
            self.snake.move(*direction)
        else:
            self.snake.move()

        hx, hy = self.snake.head()


        if not (0 <= hx < self.w and 0 <= hy < self.h):
            self.is_over = True
            return False


        if self.snake.collides_self():
            self.is_over = True
            return False


        if self.food == (hx, hy):
            self.snake.grow()
            self.score += 1
            self.spawn_food()

        return True

    def toggle_pause(self):
        if not self.is_over:
            self.paused = not self.paused