import time

from board.board import Board
from gameloop.game import Game
from screen.renderer import Renderer
from screen.character_renderer import (
    CharacterRenderer,
    CharacterState,
)
from tetras.tetras import Vector
from tetras.factory import TetraFactory
from input.input import InputHandler
from audio.audiomanager import AudioManager


def update_character_state(game, character_renderer) -> None:
    if game.game_over:
        character_renderer.set_state(
            CharacterState.GAME_OVER
        )
        return

    if game.last_lines_cleared == 4:
        character_renderer.set_state(
            CharacterState.EXCITED
        )
        return

    if game.last_lines_cleared > 0:
        character_renderer.set_state(
            CharacterState.HAPPY
        )
        return

    character_renderer.set_state(
        CharacterState.IDLE
    )


def main() -> None:
    board = Board()
    tetra_factory = TetraFactory()

    game = Game(
        board,
        tetra_factory,
    )

    character_renderer = CharacterRenderer(
        assets_path="assets/character",
    )

    renderer = Renderer(
        board,
        game,
        character_renderer,
    )

    audio_manager = AudioManager(
        music_path="assets/music/caffeine_crazed_coin-op_kids.ogg",
        sounds_path="assets/sounds",
    )

    input_handler = InputHandler()

    game.spawn_tetra()

    audio_manager.set_music_volume(0.9)
    audio_manager.set_sound_volume(0.5)

    renderer.clear_screen()
    renderer.hide_cursor()

    input_handler.start()
    audio_manager.start_music()

    running = True

    last_fall_time = time.monotonic()

    character_state_until = 0.0

    try:
        while running and not game.game_over:
            current_time = time.monotonic()

            fall_interval = max(
                0.001,
                0.35 * (0.78 ** (game.level - 1)),
            )

            if current_time - last_fall_time >= fall_interval:
                game.soft_drop()
                last_fall_time = current_time

            key = input_handler.read_key()

            if key == "a":
                if game.move_current_tetra(Vector.LEFT):
                    audio_manager.play_move()

            elif key == "d":
                if game.move_current_tetra(Vector.RIGHT):
                    audio_manager.play_move()

            elif key == "s":
                if game.soft_drop():
                    audio_manager.play_drop()

            elif key == "w":
                if game.rotate_current_tetra():
                    audio_manager.play_rotate()

            elif key == " ":
                game.hard_drop()
                audio_manager.play_drop()

            elif key == "q":
                running = False

            # Character reactions
            lines = game.consume_last_lines_cleared()

            if lines == 4:
                character_renderer.set_state(
                    CharacterState.EXCITED
                )
                character_state_until = current_time + 1.5

            elif lines > 0:
                character_renderer.set_state(
                    CharacterState.HAPPY
                )
                character_state_until = current_time + 1.0

            elif current_time >= character_state_until:
                character_renderer.set_state(
                    CharacterState.IDLE
                )

            renderer.render()

            time.sleep(0.01)

            if game.game_over:
                character_renderer.set_state(
                    CharacterState.GAME_OVER
                )

                renderer.render()

                audio_manager.stop_music()
                audio_manager.play_game_over()

                time.sleep(1)

    finally:
        input_handler.stop()
        audio_manager.shutdown()

        renderer.show_cursor()

        print()

if __name__ == "__main__":
    main()