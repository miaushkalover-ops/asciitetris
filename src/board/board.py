from tetras.tetras import TetraColor


class Board:
    def __init__(self) -> None:
        self._height = 20
        self._width = 10
        self._board = [[0 for _ in range(self._width)] for _ in range(self._height)]
        self._colors = [[None for _ in range(self._width)] for _ in range(self._height)]

    @property
    def cells(self) -> list[list[int]]:
        return self._board

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def colors(self) -> list[list[TetraColor | None]]:
        return [row[:] for row in self._colors]

    def is_valid(self, coordinates: list[list[int]]) -> bool:
        for x, y in coordinates:
            if x < 0 or x >= self._width or y < 0 or y >= self._height:
                return False
            if self._board[y][x] != 0:
                return False
        return True

    def lock_tetra(self, coordinates: list[list[int]], color: TetraColor) -> None:
        for x, y in coordinates:
            self._board[y][x] = 1
            self._colors[y][x] = color

    def clear_lines(self) -> int:
        counter = 0

        for i in range(self._height - 1, -1, -1):
            if all(self._board[i]):
                self._board.pop(i)
                self._colors.pop(i)
                counter += 1

        for _ in range(counter):
            self._board.insert(0, [0 for _ in range(self._width)])
            self._colors.insert(0, [None for _ in range(self._width)])

        return counter

