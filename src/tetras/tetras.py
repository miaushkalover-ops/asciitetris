from abc import ABC, abstractmethod
from typing import override
from enum import Enum


class Vector(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, 1)


class TetraColor(Enum):
    CYAN = (0, 240, 240)
    YELLOW = (240, 220, 0)
    MAGENTA = (180, 60, 220)
    GREEN = (60, 210, 80)
    RED = (230, 60, 60)
    BLUE = (50, 100, 230)
    ORANGE = (240, 140, 30)


class _BaseTetra(ABC):
    @abstractmethod
    def rotate(self) -> None:
        pass

    @property
    @abstractmethod
    def position(self) -> list[int]:
        pass

    @property
    @abstractmethod
    def blocks(self) -> list[list[int]]:
        pass

    @property
    @abstractmethod
    def color(self) -> TetraColor:
        pass

    @abstractmethod
    def set_position(self, position: list[int]) -> None:
        pass

    @abstractmethod
    def move(self, vector: Vector) -> None:
        pass


class Tetra(_BaseTetra):
    def __init__(
        self,
        offsets: list[list[int]],
        color: TetraColor,
    ) -> None:
        self._position = [0, 0]
        self._offsets = offsets
        self._color = color

    def rotate(self) -> None:
        for offset in self._offsets:
            offset[0], offset[1] = -offset[1], offset[0]

    @property
    def position(self) -> list[int]:
        return self._position[:]

    @property
    def blocks(self) -> list[list[int]]:
        px, py = self._position

        return [
            [px + offset_x, py + offset_y]
            for offset_x, offset_y in self._offsets
        ]

    @property
    def color(self) -> TetraColor:
        return self._color

    def set_position(self, position: list[int]) -> None:
        self._position = position[:]

    def move(self, vector: Vector) -> None:
        self._position[0] += vector.value[0]
        self._position[1] += vector.value[1]


class ITetra(Tetra):
    def __init__(self) -> None:
        super().__init__(
            [[0, 0], [1, 0], [-1, 0], [-2, 0]],
            TetraColor.CYAN,
        )

    @override
    def rotate(self) -> None:
        px, py = -1, 1
        new_offsets = []

        for x, y in self._offsets:
            x *= 2
            y *= 2

            rx = x - px
            ry = y - py

            rx, ry = -ry, rx

            rx = (rx + px) // 2
            ry = (ry + py) // 2

            new_offsets.append([rx, ry])

        self._offsets = new_offsets


class OTetra(Tetra):
    def __init__(self) -> None:
        super().__init__(
            [[0, 0], [1, 0], [0, 1], [1, 1]],
            TetraColor.YELLOW,
        )

    @override
    def rotate(self) -> None:
        pass