import sys
import tty
import termios
import select


class InputHandler:
    def __init__(self) -> None:
        self._fd = sys.stdin.fileno()
        self._old_settings = None

    def start(self) -> None:
        self._old_settings = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)

    def stop(self) -> None:
        if self._old_settings is not None:
            termios.tcsetattr(
                self._fd,
                termios.TCSADRAIN,
                self._old_settings,
            )

    def read_key(self) -> str | None:
        ready, _, _ = select.select(
            [sys.stdin],
            [],
            [],
            0,
        )

        if not ready:
            return None

        return sys.stdin.read(1)