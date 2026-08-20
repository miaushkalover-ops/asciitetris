import random

from tetras import tetras
from tetras.tetras import Vector, Tetra, ITetra, OTetra


TetraType = Tetra | ITetra | OTetra


class Game:
    def __init__(self, board, factory) -> None:
        self._board = board
        self._factory = factory

        self._current_tetra: TetraType | None = None
        self._next_tetra: TetraType | None = None

        self._score = 0
        self._level = 1
        self._lines_cleared = 0
        self._game_over = False

        self._last_lines_cleared = 0

    def spawn_tetra(self) -> None:
        if self._next_tetra is None:
            self._next_tetra = self._factory.get_random_tetra()

        self._current_tetra = self._next_tetra
        self._next_tetra = self._factory.get_random_tetra()

        self._current_tetra.set_position([
            self._board.width // 2,
            1,
        ])

        if not self._board.is_valid(self._current_tetra.blocks):
            self._game_over = True

    def move_current_tetra(self, vector: Vector) -> bool:
        if self._current_tetra is None:
            return False

        dx, dy = vector.value

        new_coordinates = [
            [x + dx, y + dy]
            for x, y in self._current_tetra.blocks
        ]

        if not self._board.is_valid(new_coordinates):
            return False

        self._current_tetra.move(vector)
        return True

    def rotate_current_tetra(self) -> bool:
        if self._current_tetra is None:
            return False

        self._current_tetra.rotate()

        if self._board.is_valid(self._current_tetra.blocks):
            return True

        # Undo rotation.
        for _ in range(3):
            self._current_tetra.rotate()

        return False

    def lock_current_tetra(self) -> None:
        if self._current_tetra is None:
            return

        self._board.lock_tetra(
            self._current_tetra.blocks,
            self._current_tetra.color,
        )

        lines_cleared = self._board.clear_lines()

        self._last_lines_cleared = lines_cleared

        self._lines_cleared += lines_cleared
        self._score += self._calculate_score(lines_cleared)
        self._level = 1 + self._lines_cleared // 5

        self.spawn_tetra()

    def soft_drop(self) -> None:
        if not self.move_current_tetra(Vector.DOWN):
            self.lock_current_tetra()

    def hard_drop(self) -> None:
        while self.move_current_tetra(Vector.DOWN):
            pass

        self.lock_current_tetra()

    def _calculate_score(self, lines: int) -> int:
        scores = {
            0: 0,
            1: 100,
            2: 300,
            3: 500,
            4: 800,
        }

        return scores[lines] * self._level

    def soft_drop(self) -> bool:
        if self._current_tetra is None:
            return False

        if self.move_current_tetra(Vector.DOWN):
            return True

        self.lock_current_tetra()
        return False

    def hard_drop(self) -> None:
        if self._current_tetra is None:
            return

        while self.move_current_tetra(Vector.DOWN):
            pass

        self.lock_current_tetra()

    
    def consume_last_lines_cleared(self) -> int:
        lines = self._last_lines_cleared
        self._last_lines_cleared = 0
        return lines

    @property
    def current_tetra(self) -> TetraType | None:
        return self._current_tetra

    @property
    def score(self) -> int:
        return self._score

    @property
    def level(self) -> int:
        return self._level

    @property
    def lines_cleared(self) -> int:
        return self._lines_cleared

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def last_lines_cleared(self) -> int:
        return self._last_lines_cleared