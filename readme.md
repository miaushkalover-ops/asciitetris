# 🧱 Terminal Tetris

> A colorful terminal-based Tetris game written in Python — with music, sound effects, RGB blocks, increasing difficulty, and a reactive ASCII companion.

```text
 SCORE 001200    LEVEL 04    LINES 012

┌────────────────────┐
│                    │          /\_/\
│        ████        │         ( o.o )
│      ██████        │          > ^ <
│                    │
│                    │         READY?
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│                    │
│        ████        │
│      ████████      │
│██████████████████  │
└────────────────────┘
```

---

## ✨ About

**Terminal Tetris** is a Tetris implementation built entirely for the terminal.

Instead of using a graphical game engine for rendering, the game uses terminal output, ANSI escape sequences, RGB colors, and Unicode characters.

The goal of the project was not only to recreate Tetris, but also to experiment with:

* object-oriented game architecture
* 2D vector rotation
* collision detection
* terminal rendering
* non-blocking keyboard input
* procedural sound effects
* real-time game loops
* ASCII / Unicode character animation

And, of course, there is a cat watching you play.

---

## 🐱 Reactive Companion

The character next to the board reacts to what happens during the game.

```text
IDLE
   ↓
HAPPY
   ↓
EXCITED
```

Other states include:

```text
WORRIED
GAME OVER
```

Examples:

* clearing lines → `HAPPY`
* clearing four lines → `EXCITED`
* dangerous board state → `WORRIED`
* losing → `GAME_OVER`

Character artwork is stored separately from the game code:

```text
assets/
└── character/
    ├── idle.txt
    ├── happy.txt
    ├── excited.txt
    ├── worried.txt
    └── game_over.txt
```

This makes it possible to replace the character or create completely different visual themes without touching the game logic.

---

## 🎮 Controls

| Key     | Action     |
| ------- | ---------- |
| `A`     | Move left  |
| `D`     | Move right |
| `S`     | Soft drop  |
| `W`     | Rotate     |
| `SPACE` | Hard drop  |
| `Q`     | Quit       |

Input is read directly from the terminal without waiting for `Enter`.

---

## 🌈 Tetromino Colors

Each tetromino uses its traditional color scheme.

| Tetromino | Color   |
| --------- | ------- |
| `I`       | Cyan    |
| `O`       | Yellow  |
| `T`       | Magenta |
| `S`       | Green   |
| `Z`       | Red     |
| `J`       | Blue    |
| `L`       | Orange  |

Blocks are rendered using **24-bit ANSI RGB background colors**.

```text
I  ████████

O  ████
   ████

T  ██████
     ██

S    ████
   ████

Z  ████
     ████
```

---

## 🔄 Rotation System

Tetrominoes are represented using a central position and relative block offsets.

For most pieces, rotation is calculated using a 90° 2D vector transformation:

```text
(x, y) → (-y, x)
```

For example:

```text
(-1, 0) → ( 0, -1)
( 0, 0) → ( 0,  0)
( 1, 0) → ( 0,  1)
( 0, 1) → (-1,  0)
```

The `I` tetromino uses its own rotation implementation because its rotation center lies between cells.

The `O` tetromino does not require visible rotation.

---

## 🧠 Architecture

The project separates game logic from rendering, input, audio, and assets.

```text
                    ┌───────────────┐
                    │     main      │
                    └───────┬───────┘
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
          ▼                 ▼                  ▼
       Game              Renderer           Audio
          │                 │
     ┌────┴────┐       ┌────┴────────┐
     ▼         ▼       ▼             ▼
   Board   Tetromino   Board      Character
              │
              ▼
        Tetra Factory
```

### Tetromino

Responsible for:

* position
* relative block offsets
* movement
* rotation
* color

### Board

Responsible for:

* board dimensions
* occupied cells
* collision validation
* locking tetrominoes
* clearing completed lines
* dropping remaining rows

### Game

Responsible for:

* current tetromino
* next tetromino
* spawning
* movement requests
* rotation requests
* soft drop
* hard drop
* score
* level
* game-over state

### Renderer

Responsible for:

* drawing the board
* RGB terminal colors
* score / level / line HUD
* active tetromino rendering
* character rendering
* terminal cursor control

### Audio Manager

Responsible for:

* background music
* movement sounds
* rotation sounds
* drop sounds
* line-clear sounds
* Tetris sounds
* game-over sounds

---

## 📁 Project Structure

```text
.
├── assets/
│   ├── character/
│   │   ├── idle.txt
│   │   ├── happy.txt
│   │   ├── excited.txt
│   │   ├── worried.txt
│   │   └── game_over.txt
│   │
│   ├── music/
│   │   └── theme.ogg
│   │
│   └── sounds/
│       ├── move.wav
│       ├── rotate.wav
│       ├── drop.wav
│       ├── line_clear.wav
│       ├── tetris.wav
│       └── game_over.wav
│
├── src/
│   ├── board/
│   │   └── board.py
│   │
│   ├── gameloop/
│   │   └── game.py
│   │
│   ├── input/
│   │   └── input.py
│   │
│   ├── audio/
│   │   └── audiomanager.py
│   │
│   ├── screen/
│   │   ├── renderer.py
│   │   └── character_renderer.py
│   │
│   ├── tetras/
│   │   ├── tetras.py
│   │   └── factory.py
│   │
│   └── main.py
│
└── tools/
    └── generate_sfx.py
```

---

## 🔊 Audio

Background music is played independently from sound effects.

The game currently supports:

```text
move.wav
rotate.wav
drop.wav
line_clear.wav
tetris.wav
game_over.wav
```

The sound effects can also be generated programmatically using the included sound-generation script.

```bash
python tools/generate_sfx.py
```

This generates small retro-style `.wav` effects using synthesized waveforms.

---

## 📈 Difficulty

The game becomes progressively faster as the level increases.

The falling interval decreases dynamically based on the current level, while a minimum interval prevents it from becoming effectively instantaneous.

```text
LEVEL 1  ────────────── slow
LEVEL 2  ────────────
LEVEL 3  ──────────
LEVEL 4  ────────
LEVEL 5  ──────
LEVEL 6  ────
LEVEL 7+ ── FAST
```

---

## 🏆 Scoring

Clearing more lines at once rewards more points.

```text
1 line   → 100
2 lines  → 300
3 lines  → 500
4 lines  → 800
```

Score can also scale with the current level.

---

## 🐧 Requirements

The project is primarily designed for a Linux terminal.

Recommended:

* Linux / Linux Mint
* Python 3.12+
* terminal with ANSI true-color support
* UTF-8 compatible terminal font
* audio output

Install dependencies:

```bash
pip install pygame
```

---

## 🚀 Running

Clone the repository:

```bash
git clone <your-repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install pygame
```

Run the game from the project root:

```bash
python src/main.py
```

---

## 🛠️ Current Features

* [x] Seven tetrominoes
* [x] Tetromino rotation
* [x] Special `I` rotation
* [x] Collision detection
* [x] Automatic falling
* [x] Soft drop
* [x] Hard drop
* [x] Line clearing
* [x] Score system
* [x] Level system
* [x] Increasing difficulty
* [x] Game-over detection
* [x] RGB terminal rendering
* [x] Non-blocking keyboard input
* [x] Background music
* [x] Sound effects
* [x] ASCII / Unicode companion
* [x] Character reactions

---

## 🔮 Ideas for the Future

* [ ] Proper 7-bag randomizer
* [ ] SRS wall kicks
* [ ] Ghost piece
* [ ] Hold piece
* [ ] Next-piece preview
* [ ] Combo system
* [ ] Back-to-back Tetris bonus
* [ ] High-score saving
* [ ] Pause menu
* [ ] Multiple character themes
* [ ] Character color maps
* [ ] Character animations
* [ ] Music changing with difficulty
* [ ] Configurable controls
* [ ] Settings file
* [ ] Terminal resize detection

---

## 💡 Why a Terminal?

Because this:

```text
pygame window
```

is normal.

But this:

```text
Linux terminal
+
RGB Tetris
+
music
+
sound effects
+
reactive ASCII cat
```

is much more fun.

---

## 🎵 Credits

Background music and third-party assets should be credited here according to their respective licenses.

```text
Music:
<track name>
<artist>
<license / source>

Character:
Original terminal artwork

Sound Effects:
Procedurally generated for this project
```

---

## 📜 License

Choose a license before distributing the project publicly.

For an open-source project, the MIT License is a common simple option.

---

<p align="center">
  <b>Built with Python, ANSI escape sequences, questionable terminal magic, and a cat.</b>
</p>

<p align="center">
  🐱 + 🧱 + 🎵 = Tetris
</p>
