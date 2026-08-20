import random

from tetras.tetras import Tetra, ITetra, OTetra, TetraColor


class TetraFactory:
    def get_random_tetra(self) -> Tetra | ITetra | OTetra:
        tetra_type = random.choice([
            "I",
            "O",
            "T",
            "J",
            "L",
            "S",
            "Z",
        ])

        match tetra_type:
            case "I":
                return ITetra()

            case "O":
                return OTetra()

            case "T":
                return Tetra(
                    [[0, 0], [-1, 0], [1, 0], [0, 1]],
                    TetraColor.MAGENTA,
                )

            case "J":
                return Tetra(
                    [[0, 0], [-1, 0], [1, 0], [-1, 1]],
                    TetraColor.BLUE,
                )

            case "L":
                return Tetra(
                    [[0, 0], [-1, 0], [1, 0], [1, 1]],
                    TetraColor.ORANGE,
                )

            case "S":
                return Tetra(
                    [[0, 0], [1, 0], [0, 1], [-1, 1]],
                    TetraColor.GREEN,
                )

            case "Z":
                return Tetra(
                    [[0, 0], [-1, 0], [0, 1], [1, 1]],
                    TetraColor.RED,
                )

        raise RuntimeError("Unknown tetra type")