from collections import deque
from copy import deepcopy
from string import ascii_letters, ascii_uppercase


class Rotor:
    def __init__(
        self, alphabet: str, notch: list[str], position: str = "A", model: str = None
    ) -> None:
        if len(position) > 1 or position not in ascii_letters:
            raise ValueError(f"Invalid starting position {position}")

        if len(alphabet) != 26:
            raise ValueError(f"Invalid rotor length")

        if any(l not in alphabet.upper() for l in ascii_uppercase):
            raise ValueError(f"Invalid rotor")

        self._alphabet = deque([a for a in alphabet])
        self._notch = [ord(n.upper()) - 65 for n in notch]
        self._position = ord(position.upper()) - 65
        self._model = model

        self.step(self._position)
        self._stepped = False

    def _wrapPosition(self, position: int) -> int:
        while position < 0:
            position += 25
        while position > 25:
            position -= 25
        return position

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
            raise ValueError(f"Invalid starting position {position}")

        self._alphabet.rotate(self._position)
        self._position = ord(position.upper()) - 65
        self._alphabet.rotate(-self._position)

    @property
    def alphabet(self) -> str:
        return "".join(self._alphabet)

    @property
    def hit_notch(self) -> bool:
        return self._wrapPosition(self._position - 1) in self._notch and self._stepped

    @property
    def in_notch(self) -> bool:
        return self._wrapPosition(self._position) in self._notch and not self._stepped

    @property
    def model(self) -> str:
        return self._model


class UKW(Rotor):
    def __init__(self, alphabet: str, model: str = None):
        self._alphabet = deque([a for a in alphabet])
        self._model = model


class ETW(Rotor):
    def __init__(self, alphabet: str, model: str = None):
        self._alphabet = deque([a for a in alphabet])
        self._model = model


class Enigma:
    def __init__(self, model="Custom", **kwargs) -> None:
        """Keyword Args:
        rotors_map (Optional[Dict]): containing name, alphabet and notch for each available rotor. Defaults to M3 rotors (see below).
        ukw_map (Optional[Dict]): containing name, alphabet and notch for each available reflector (UKW). Defaults to M3 reflectors (see below).
        etw_map (Optional[Dict]): containing name, alphabet and notch for each available ETW. Defaults to None.
        max_rotors (Optional[int]): number of maximum allowed rotors. Defaults to None (unlimited rotors.)
        model (Optional[str]): name of the model of the machine. Defaults to "Custom".
        year (Optional[int]): year of manifacture of the machine. Defaults to 2022.
        """

        if kwargs.get("etw_map") or isinstance(kwargs.get("etw_map"), dict):
            self._etw_map = deepcopy(kwargs["etw_map"])
        else:
            self._etw_map = None

        if kwargs.get("ukw_map") or isinstance(kwargs.get("ukw_map"), dict):
            self._ukw_map = deepcopy(kwargs["ukw_map"])
        else:
            self._ukw_map = {
                "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
                "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
                "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
            }

        if kwargs.get("rotors_map"):
            self._rotors_map = deepcopy(kwargs["rotors_map"])
        else:
            self._rotors_map = {
                "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["J"]},
                "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z"]},
            }

        self._model = model
        self._year = kwargs.get("year", 2022)
        self._max_rotors = kwargs.get("max_rotors")
        self._rotors = []
        self._etw = None
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
        # entry
        if self._etw:
            c = self._etw.left(c)

        # right to left
        for r in self._rotors[::-1]:
            c = r.left(c)

        # reflector
        if self._ukw:
            c = self._ukw.left(c)

        # left to right
        for r in self._rotors:
            c = r.right(c)

        if self._etw:
            c = self._etw.right(c)

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
        if self._max_rotors and len(self._rotors) > self._max_rotors:
            raise ValueError(f"This machine supports only {self._max_rotors} rotors.")

        try:
            self._rotors.append(
                Rotor(
                    self._rotors_map[rotor]["alphabet"],
                    self._rotors_map[rotor]["notch"],
                    position=position,
                    model=rotor,
                )
            )
        except Exception:
            raise ValueError(f"Unknown rotor {rotor}")

    def removeRotors(self) -> None:
        self._rotors = []

    def setRotorsPositions(self, pos: str) -> None:
        if len(pos) != len(self._rotors):
            raise ValueError("Invalid rotors position")

        for x, p in enumerate(pos):
            if p not in ascii_letters:
                raise ValueError(f"Position {p} is not valid")
            self._rotors[x].position = p

    def getRotorsPositions(self) -> str:
        return "".join(r.position for r in self._rotors)

    def setRotors(self, *rotors: str) -> None:
        self._rotors = []
        for r in rotors:
            self.addRotor(r, "A")

    def setUKW(self, ukw: str) -> None:
        try:
            self._ukw = UKW(self._ukw_map[ukw]["alphabet"], model=ukw)
        except KeyError:
            raise ValueError(f"Unknown ukw {ukw}")

    def setETW(self, etw: str) -> None:
        try:
            self._etw = ETW(self._etw_map[etw]["alphabet"], model=etw)
        except KeyError:
            raise ValueError(f"Unknown ukw {etw}")

    def setPlugboard(self, *plugs: str) -> None:
        if len(plugs) > 10:
            raise ValueError("Max 10 plugs are allowed")

        for p in plugs:
            if len(p) != 2:
                raise Exception("Invalid plugs combinations")

        self._plugboard = [(x[0], x[1]) for x in plugs]

    def encode(self, clean: str, format_output: bool = False) -> str:
        if not self._rotors:
            raise Exception("No rotors have been added")

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

    @property
    def available_rotors(self) -> list[str]:
        return [r for r in self._rotors_map.keys()]

    @property
    def available_UKWs(self) -> list[str]:
        if self._ukw_map:
            return [u for u in self._ukw_map.keys()]
        return []

    @property
    def available_ETWs(self) -> list[str]:
        if self._etw_map:
            return [e for e in self._etw_map.keys()]
        return []

    @property
    def max_rotors(self) -> int:
        if self._max_rotors:
            return self._max_rotors
        return -1

    @property
    def year(self) -> int:
        return self._year

    @property
    def model(self) -> str:
        return self._model
