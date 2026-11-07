
import unittest

from game.snake import Snake
from game.game import Game


class TestSnake(unittest.TestCase):
    def test_move_head(self):
        s = Snake((5, 5), direction=(1, 0), length=3)
        self.assertEqual(s.head(), (5, 5))
        s.move()
        self.assertEqual(s.head(), (6, 5))

    def test_move_respects_direction(self):
        s = Snake((5, 5), direction=(1, 0), length=1)
        s.move(0, 1)
        self.assertEqual(s.head(), (5, 6))
        s.move(-1, 0)
        self.assertEqual(s.head(), (4, 6))

    def test_no_reverse(self):
        s = Snake((5, 5), direction=(1, 0), length=2)
        s.move(-1, 0)
        self.assertEqual(s.direction, (1, 0))
        self.assertEqual(s.head(), (6, 5))
        s.move()
        self.assertEqual(s.head(), (7, 5))

    def test_grow(self):
        s = Snake((5, 5), direction=(1, 0), length=3)
        old_len = len(s.body)
        s.grow()
        s.move()
        self.assertEqual(len(s.body), old_len + 1)

    def test_collides_self(self):
        s = Snake((5, 5), direction=(1, 0), length=1)
        s.body = [(5, 5), (4, 5), (3, 5), (3, 6), (4, 6)]
        s.body[0] = (4, 6)
        self.assertTrue(s.collides_self())


class TestGame(unittest.TestCase):
    def test_wall_collision_game_over(self):
        g = Game(5, 5, speed=8)
        g.snake.body = [(4, 2), (3, 2), (2, 2)]
        g.snake.direction = (1, 0)
        g.food = None
        ok = g.step()
        self.assertFalse(ok)
        self.assertTrue(g.is_over)

    def test_eat_food_grows_and_scores(self):
        g = Game(10, 10, speed=8)
        g.snake.body = [(5, 5), (4, 5), (3, 5)]
        g.snake.direction = (1, 0)
        g.food = (6, 5)
        old_len = len(g.snake.body)

        g.step()
        self.assertEqual(g.score, 1)
        self.assertEqual(len(g.snake.body), old_len)
        self.assertNotEqual(g.food, (6, 5))

        g.step()
        self.assertEqual(len(g.snake.body), old_len + 1)

    def test_spawn_food_free_cell(self):
        g = Game(10, 10, speed=8)
        for _ in range(200):
            g.food = None
            f = g.spawn_food()
            self.assertIsNotNone(f)
            self.assertNotIn(f, set(g.snake.body))
            self.assertTrue(0 <= f[0] < g.w and 0 <= f[1] < g.h)

    def test_pause_blocks_step(self):
        g = Game(10, 10, speed=8)
        g.toggle_pause()
        head = g.snake.head()
        g.step()
        self.assertEqual(g.snake.head(), head)

    def test_level_and_speed_grow(self):
        g = Game(10, 10, speed=8)
        base = g.speed
        g.score = 10
        self.assertGreater(g.level, 1)
        self.assertGreater(g.speed, base)


if __name__ == "__main__":
    unittest.main()