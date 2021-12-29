from collections import deque
from string import ascii_letters


class Rotor:
    def __init__(self, alphabet: str, notch: list[str], position: chr = "A") -> None:
        if len(position) > 1 or position not in ascii_letters:
            raise Exception("Invalid starting position")

        self._alphabet = deque([a for a in alphabet])
        self._notch = [ord(n.upper()) - 65 for n in notch]
        self._position = ord(position.upper()) - 65

        self.step(self._position)
        self._stepped = False

    def left(self, letter: str) -> str:
        pos = ord(letter.upper()) - 65
        return self._alphabet[pos]

    def right(self, letter: str) -> str:
        pos = self._alphabet.index(letter)
        return chr(pos + 65)

    def step(self, steps=1) -> None:
        self._position += steps
        self._alphabet.rotate(-steps)
        self._stepped = True

    def reset(self) -> None:
        self._stepped = False

    @property
    def position(self) -> str:
        return chr(self._position % 26 + 65)

    @position.setter
    def position(self, position: str) -> None:
        if len(position) > 1 or position not in ascii_letters:
            raise Exception("Invalid starting position")

        self._alphabet.rotate(self._position)
        self._position = ord(position.upper()) - 65
        self._alphabet.rotate(-self._position)

    @property
    def alphabet(self) -> str:
        return "".join(self._alphabet)

    @property
    def hit_notch(self) -> bool:
        return self._position % 26 - 1 in self._notch and self._stepped

    @property
    def in_notch(self):
        return self._position % 26 in self._notch and not self._stepped


class UKW(Rotor):
    def __init__(self, alphabet: str):
        self._alphabet = deque([a for a in alphabet])


class Enigma:
    def __init__(self) -> None:
        self._rotors_map = {
            "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
            "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
            "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
            "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["Z"]},
            "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z", "M"]},
            "VI": {"alphabet": "JPGVOUMFYQBENHZRDKASXLICTW", "notch": ["Z", "M"]},
            "VII": {"alphabet": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "notch": ["Z", "M"]},
            "VIII": {"alphabet": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "notch": ["Z", "M"]},
            "BETA": {"alphabet": "LEYJVCNIXWPBQMDRTAKZGFUHOS", "notch": []},
            "GAMMA": {"alphabet": "FSOKANUERHMBTIYCWLQPZXVGJD", "notch": []},
        }

        self._ukw_map = {
            "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
            "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
            "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
            "B-THIN": {"alphabet": "ENKQAUYWJICOPBLMDXZVFTHRGS"},
            "C-THIN": {"alphabet": "RDOBJNTKVEHMLFCWZAXGYIPSUQ"},
        }

        self._rotors = []
        self._ukw = None
        self._plugboard = []

    def _formatOutput(self, output: str) -> str:
        formatted = "".join(output.split(" "))
        return " ".join(formatted[x : x + 5] for x in range(0, len(formatted), 5))

    def _applyPlugboard(self, c: str) -> str:
        if not self._plugboard:
            return c

        for p in self._plugboard:
            if c in p:
                if c == p[0]:
                    return p[1]
                return p[0]

        return c

    def _signalTravel(self, c: str) -> str:
        # right to left
        for r in self._rotors[::-1]:
            c = r.left(c)

        # reflector
        c = self._ukw.left(c)

        # left to right
        for r in self._rotors:
            c = r.right(c)

        return c

    def _applyNotches(self) -> None:
        for x in range(len(self._rotors) - 1, 0, -1):
            # notch stepping
            if self._rotors[x].hit_notch:
                self._rotors[x - 1].step()

            if self._rotors[x].in_notch and x < len(self._rotors) - 1:
                # double stepping
                self._rotors[x].step()
                self._rotors[x - 1].step()

    def addRotor(self, rotor: str, position: str = "A") -> None:
        try:
            self._rotors.append(
                Rotor(
                    self._rotors_map[rotor]["alphabet"],
                    self._rotors_map[rotor]["notch"],
                    position,
                )
            )
        except Exception:
            raise Exception(f"Unknown rotor {rotor}")

    def removeRotors(self) -> None:
        self._rotors = []

    def setRotorsPositions(self, pos: str) -> None:
        if len(pos) != len(self._rotors):
            raise Exception("Invalid rotors position")

        for x, p in enumerate(pos):
            if p not in ascii_letters:
                raise Exception(f"Position {p} is not valid")
            self._rotors[x].position = p

    def getRotorsPositions(self) -> str:
        return "".join(r.position for r in self._rotors)

    def setRotors(self, *rotors: str) -> None:
        self._rotors = []
        for r in rotors:
            self.addRotor(r, "A")

    def setUKW(self, ukw: str) -> None:
        try:
            self._ukw = UKW(self._ukw_map[ukw]["alphabet"])
        except KeyError:
            raise KeyError(f"Unknown ukw {ukw}")

    def setPlugboard(self, *plugs: str) -> None:
        if len(plugs) > 10:
            raise Exception("Max 10 plugs")

        for p in plugs:
            if len(p) != 2:
                raise Exception("Invalid plugs combinations")

        self._plugboard = [(x[0], x[1]) for x in plugs]

    def encode(self, clean: str, format_output: bool = False) -> str:
        if not self._rotors:
            raise Exception("No rotors have been added")
        if not self._ukw:
            raise Exception("No ukw has been added")

        encoded = []

        for c in clean:
            if c not in ascii_letters:
                if not format_output:
                    encoded.append(c)
                continue

            # reset rotors
            for r in self._rotors:
                r.reset()

            # step last
            self._rotors[-1].step()

            # plugboard
            e = self._applyPlugboard(c)

            # rotors and stuff
            e = self._signalTravel(e)

            # plugboard
            e = self._applyPlugboard(e)

            # notches turnover happens when the button is depressed
            self._applyNotches()

            # append encoded character
            encoded.append(e)

        unformatted = "".join(encoded)
        if not format_output:
            return unformatted

        return self._formatOutput(unformatted)

    @property
    def rotors_position(self) -> str:
        return self.getRotorsPositions()


class EnigmaFactory:
    def __init__(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
