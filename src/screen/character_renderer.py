from enum import Enum
from pathlib import Path


class CharacterState(Enum):
    IDLE = "idle"
    HAPPY = "happy"
    EXCITED = "excited"
    WORRIED = "worried"
    GAME_OVER = "game_over"


class CharacterRenderer:
    def __init__(self, assets_path: str) -> None:
        self._assets_path = Path(assets_path)
        self._state = CharacterState.IDLE

        self._arts = {
            state: self._load_art(state)
            for state in CharacterState
        }

    def _load_art(self, state: CharacterState) -> list[str]:
        path = self._assets_path / f"{state.value}.txt"

        if not path.exists():
            raise FileNotFoundError(
                f"Character asset not found: {path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            return file.read().splitlines()

    def set_state(self, state: CharacterState) -> None:
        self._state = state

    @property
    def state(self) -> CharacterState:
        return self._state

    @property
    def lines(self) -> list[str]:
        return self._arts[self._state][:]