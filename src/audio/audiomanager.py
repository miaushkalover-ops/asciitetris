from pathlib import Path

import pygame


class AudioManager:
    def __init__(
        self,
        music_path: str,
        sounds_path: str,
    ) -> None:
        pygame.mixer.init()

        self._music_path = Path(music_path)
        sounds_path = Path(sounds_path)

        self._move_sound = pygame.mixer.Sound(
            sounds_path / "move.wav"
        )
        self._rotate_sound = pygame.mixer.Sound(
            sounds_path / "rotate.wav"
        )
        self._drop_sound = pygame.mixer.Sound(
            sounds_path / "drop.wav"
        )
        self._line_clear_sound = pygame.mixer.Sound(
            sounds_path / "line_clear.wav"
        )
        self._tetris_sound = pygame.mixer.Sound(
            sounds_path / "tetris.wav"
        )
        self._game_over_sound = pygame.mixer.Sound(
            sounds_path / "game_over.wav"
        )

    def start_music(self) -> None:
        pygame.mixer.music.load(self._music_path)
        pygame.mixer.music.play(-1)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()

    def pause_music(self) -> None:
        pygame.mixer.music.pause()

    def resume_music(self) -> None:
        pygame.mixer.music.unpause()

    def play_move(self) -> None:
        self._move_sound.play()

    def play_rotate(self) -> None:
        self._rotate_sound.play()

    def play_drop(self) -> None:
        self._drop_sound.play()

    def play_line_clear(self) -> None:
        self._line_clear_sound.play()

    def play_tetris(self) -> None:
        self._tetris_sound.play()

    def play_game_over(self) -> None:
        self._game_over_sound.play()

    def set_music_volume(self, volume: float) -> None:
        pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, volume: float) -> None:
        sounds = [
            self._move_sound,
            self._rotate_sound,
            self._drop_sound,
            self._line_clear_sound,
            self._tetris_sound,
            self._game_over_sound,
        ]

        for sound in sounds:
            sound.set_volume(volume)

    def shutdown(self) -> None:
        pygame.mixer.quit()