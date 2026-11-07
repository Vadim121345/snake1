
import sys

CLEAR = "\033[H"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"


def build_frame(game) -> str:
    w, h = game.w, game.h
    snake_body = set(game.snake.body)
    head = game.snake.head()

    lines = []
    lines.append("+" + "-" * w + "+")
    for y in range(h):
        row = ["|"]
        for x in range(w):
            p = (x, y)
            if p == head:
                row.append(GREEN + "O" + RESET)
            elif p in snake_body:
                row.append(GREEN + "o" + RESET)
            elif p == game.food:
                row.append(RED + "*" + RESET)
            else:
                row.append(" ")
        row.append("|")
        lines.append("".join(row))
    lines.append("+" + "-" * w + "+")

    status = (
        f" Счёт: {CYAN}{game.score}{RESET}  "
        f"Уровень: {YELLOW}{game.level}{RESET}  "
        f"Скорость: {game.speed:.1f}  "
        f"Пауза: {'ДА' if game.paused else 'нет'} "
    )
    lines.append(status)
    lines.append(" Управление: стрелки | P — пауза | Q — выход ")
    return "\n".join(lines)


def draw(game):
    sys.stdout.write(CLEAR)
    sys.stdout.write(build_frame(game) + "\n")
    sys.stdout.flush()


def game_over_screen(game) -> str:
    return (
        "\n"
        + "=" * 40 + "\n"
        + "            GAME OVER\n"
        + "=" * 40 + "\n"
        + f"  Ваш счёт: {game.score}\n"
        + f"  Достигнут уровень: {game.level}\n"
        + "  Сыграть ещё раз? (y/n): "
    )