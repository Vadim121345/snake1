
class Snake:
    def __init__(self, start_pos, direction=(1, 0), length=3):

        x, y = start_pos
        dx, dy = direction
        self.direction = (dx, dy)

        self.body = [(x - dx * i, y - dy * i) for i in range(length)]
        self._pending_grow = 0

    def head(self):
        return self.body[0]

    def move(self, dx=None, dy=None):

        if dx is not None and dy is not None:
            if (dx, dy) != (-self.direction[0], -self.direction[1]):
                self.direction = (dx, dy)

        hx, hy = self.head()
        ndx, ndy = self.direction
        new_head = (hx + ndx, hy + ndy)

        self.body.insert(0, new_head)
        if self._pending_grow > 0:
            self._pending_grow -= 1
        else:
            self.body.pop()
        return new_head

    def grow(self, amount=1):

        self._pending_grow += amount

    def collides_self(self) -> bool:

        return self.head() in self.body[1:]

    def __len__(self):
        return len(self.body)