from .character_renderer import CharacterRenderer


class Renderer:
    EMPTY_CELL = "  "

    def __init__(
        self,
        board,
        game,
        character_renderer: CharacterRenderer,
    ) -> None:
        self._board = board
        self._game = game
        self._character_renderer = character_renderer

    def render(self) -> None:
        frame = self._build_frame()

        print("\033[H", end="")

        for line in frame.splitlines():
            print("\033[2K", end="")
            print(line)

        print("\033[J", end="")

    def _build_frame(self) -> str:
        lines = []

        hud = (
            f"SCORE {self._game.score:06d}"
            f"    LEVEL {self._game.level:02d}"
            f"    LINES {self._game.lines_cleared:03d}"
        )

        lines.append(hud)
        lines.append("")

        board_lines = self._build_board()
        character_lines = self._character_renderer.lines

        combined_lines = self._combine_lines(
            board_lines,
            character_lines,
            gap=6,
        )

        lines.extend(combined_lines)

        return "\n".join(lines) + "\n"

    def _build_board(self) -> list[str]:
        # Board.colors should return a copy.
        cells = self._board.colors

        current_tetra = self._game.current_tetra

        if current_tetra is not None:
            for x, y in current_tetra.blocks:
                if (
                    0 <= x < self._board.width
                    and 0 <= y < self._board.height
                ):
                    cells[y][x] = current_tetra.color

        lines = []

        top_border = "┌" + "──" * self._board.width + "┐"
        bottom_border = "└" + "──" * self._board.width + "┘"

        lines.append(top_border)

        for row in cells:
            line = "│"

            for color in row:
                if color is None:
                    line += self.EMPTY_CELL
                else:
                    line += self._colored_block(color)

            line += "│"
            lines.append(line)

        lines.append(bottom_border)

        return lines

    def _combine_lines(
        self,
        left: list[str],
        right: list[str],
        gap: int,
    ) -> list[str]:
        height = max(len(left), len(right))
        result = []

        separator = " " * gap

        for i in range(height):
            if i < len(left):
                left_line = left[i]
            else:
                # Board visible width:
                # width * 2 cells + 2 border characters.
                left_line = " " * (self._board.width * 2 + 2)

            if i < len(right):
                right_line = right[i]
            else:
                right_line = ""

            result.append(
                left_line
                + separator
                + right_line
            )

        return result

    @staticmethod
    def _colored_block(color) -> str:
        r, g, b = color.value

        return (
            f"\033[48;2;{r};{g};{b}m"
            "  "
            "\033[0m"
        )

    @staticmethod
    def clear_screen() -> None:
        print("\033[2J\033[H", end="", flush=True)

    @staticmethod
    def hide_cursor() -> None:
        print("\033[?25l", end="", flush=True)

    @staticmethod
    def show_cursor() -> None:
        print("\033[?25h", end="", flush=True)