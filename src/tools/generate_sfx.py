import math
import random
import wave
from pathlib import Path


SAMPLE_RATE = 44100
VOLUME = 0.35

OUTPUT_DIR = Path("assets/sounds")


def square_wave(frequency: float, time: float) -> float:
    return 1.0 if math.sin(2 * math.pi * frequency * time) >= 0 else -1.0


def triangle_wave(frequency: float, time: float) -> float:
    return 2 * abs(
        2 * (frequency * time - math.floor(frequency * time + 0.5))
    ) - 1


def envelope(time: float, duration: float) -> float:
    return max(0.0, 1.0 - time / duration)


def save_wav(
    filename: str,
    samples: list[float],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / filename

    with wave.open(str(path), "w") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)

        for sample in samples:
            sample = max(-1.0, min(1.0, sample))
            value = int(sample * 32767)

            file.writeframesraw(
                value.to_bytes(
                    2,
                    byteorder="little",
                    signed=True,
                )
            )

    print(f"Generated: {path}")


def generate_tone(
    frequency: float,
    duration: float,
    wave_type: str = "square",
) -> list[float]:
    samples = []
    count = int(SAMPLE_RATE * duration)

    for i in range(count):
        time = i / SAMPLE_RATE

        if wave_type == "triangle":
            value = triangle_wave(frequency, time)
        else:
            value = square_wave(frequency, time)

        value *= envelope(time, duration)
        value *= VOLUME

        samples.append(value)

    return samples


def generate_move() -> None:
    samples = generate_tone(
        frequency=180,
        duration=0.035,
        wave_type="square",
    )

    save_wav("move.wav", samples)


def generate_rotate() -> None:
    duration = 0.09
    samples = []

    for i in range(int(SAMPLE_RATE * duration)):
        time = i / SAMPLE_RATE

        progress = time / duration
        frequency = 280 + 250 * progress

        value = square_wave(frequency, time)
        value *= envelope(time, duration)
        value *= VOLUME

        samples.append(value)

    save_wav("rotate.wav", samples)


def generate_drop() -> None:
    duration = 0.12
    samples = []

    for i in range(int(SAMPLE_RATE * duration)):
        time = i / SAMPLE_RATE

        progress = time / duration
        frequency = 150 - 90 * progress

        tone = triangle_wave(frequency, time)
        noise = random.uniform(-1, 1) * 0.20

        value = tone + noise
        value *= envelope(time, duration)
        value *= VOLUME

        samples.append(value)

    save_wav("drop.wav", samples)


def generate_line_clear() -> None:
    samples = []

    notes = [
        (523.25, 0.08),
        (659.25, 0.08),
        (783.99, 0.12),
    ]

    for frequency, duration in notes:
        samples.extend(
            generate_tone(
                frequency,
                duration,
                "square",
            )
        )

    save_wav("line_clear.wav", samples)


def generate_tetris() -> None:
    samples = []

    notes = [
        (523.25, 0.07),
        (659.25, 0.07),
        (783.99, 0.07),
        (1046.50, 0.20),
    ]

    for frequency, duration in notes:
        samples.extend(
            generate_tone(
                frequency,
                duration,
                "square",
            )
        )

    save_wav("tetris.wav", samples)


def generate_game_over() -> None:
    samples = []

    notes = [
        (392.00, 0.14),
        (329.63, 0.14),
        (261.63, 0.14),
        (196.00, 0.30),
    ]

    for frequency, duration in notes:
        samples.extend(
            generate_tone(
                frequency,
                duration,
                "triangle",
            )
        )

    save_wav("game_over.wav", samples)


def main() -> None:
    generate_move()
    generate_rotate()
    generate_drop()
    generate_line_clear()
    generate_tetris()
    generate_game_over()

    print("\nAll sound effects generated.")


if __name__ == "__main__":
    main()