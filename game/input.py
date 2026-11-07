
import time
import msvcrt


_WIN_SPECIAL = {
    b"H": "UP",
    b"P": "DOWN",
    b"K": "LEFT",
    b"M": "RIGHT",
}


class RawInput:


    def __enter__(self):
        return self

    def __exit__(self, *exc):

        while msvcrt.kbhit():
            msvcrt.getch()

    def read_key(self, timeout: float):

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if msvcrt.kbhit():
                ch = msvcrt.getch()

                if ch in (b"\xe0", b"\x00"):
                    if msvcrt.kbhit():
                        ch2 = msvcrt.getch()
                        return _WIN_SPECIAL.get(ch2)
                    return None
                try:
                    return ch.decode("ascii")
                except UnicodeDecodeError:
                    return None
            time.sleep(0.005)
        return None


DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}