
import argparse
import os
import sys


try:
    import colorama
    colorama.just_fix_windows_console()
except ImportError:
    os.system("")

from game.game import Game
from game import renderer
from game.input import RawInput, DIRECTIONS


def parse_args():
    p = argparse.ArgumentParser(description="Консольная змейка (Windows)")
    p.add_argument("--width", type=int, default=20)
    p.add_argument("--height", type=int, default=15)
    p.add_argument("--speed", type=float, default=8.0)
    return p.parse_args()


def play_once(width, height, speed):
    game = Game(width, height, speed)

    with RawInput() as ri:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        pending_dir = None

        while not game.is_over:
            renderer.draw(game)
            key = ri.read_key(game.tick_interval)

            if key in DIRECTIONS:
                pending_dir = DIRECTIONS[key]
            elif key in ("p", "P"):
                game.toggle_pause()
                pending_dir = None
                continue
            elif key in ("q", "Q"):
                return None

            game.step(pending_dir)
            pending_dir = None


        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(renderer.game_over_screen(game))
        sys.stdout.flush()


        while True:
            k = ri.read_key(1.0)
            if k in ("y", "Y"):
                return True
            if k in ("n", "N", "q", "Q"):
                return False


def main():
    args = parse_args()
    try:
        while True:
            again = play_once(args.width, args.height, args.speed)
            if again is None or not again:
                break
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\033[0m\n")
        print("Пока!")


if __name__ == "__main__":
    main()