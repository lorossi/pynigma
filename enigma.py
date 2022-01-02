from collections import deque
from copy import deepcopy
from string import ascii_letters, ascii_uppercase


class Rotor:
    def __init__(
        self, alphabet: str, notch: list[str], position: str = "A", model: str = None
    ) -> None:
        """Creates a rotor.

        Args:
            alphabet (str): Alphabet of the rotor
            notch (list[str]): List of notches for the rotor
            position (str, optional): Starting position of the rotor. Defaults to "A".
            model (str, optional): Model of the rotor. Defaults to None.

        Raises:
            ValueError: Alphabet is invalid
            ValueError: Notch is invalid
            ValueError: Starting position is invalid
        """

        # check if all letters are in the alphabet and if alphabet is valid
        if len(alphabet) != 26 or any(
            l not in alphabet.upper() for l in ascii_uppercase
        ):
            raise ValueError(f"Invalid rotor alphabet ({alphabet})")
        # check if notch is valid
        for n in notch:
            if not n in ascii_letters:
                raise ValueError(f"Invalid notch {n}")
        # check if start position is valid
        if len(position) > 1 or position not in ascii_letters:
            raise ValueError(f"Invalid starting position {position}")

        # find a smarter way to do this, maybe using dictionaries?
        # there's no much sense in looking at the index of a letter to go right
        self._alphabet = {ascii_uppercase[x]: alphabet[x].upper() for x in range(26)}

        self._notch = [ord(n.upper()) - 65 for n in notch]
        self._position = ord(position.upper()) - 65
        self._model = model
        # set rotor in place
        self.step(self._position)
        self._stepped = False

    def __str__(self) -> str:
        return f"Alphabet: {''.join(self._alphabet)}. Position: {self._position}"

    def left(self, letter: str) -> str:
        """Move letter from right to left.

        Args:
            letter (str): Letter to encode

        Returns:
            str: Encoded letter
        """
        pos = ord(letter.upper()) - 65
        return self._alphabet[pos]

    def right(self, letter: str) -> str:
        """Move letter from left to right.

        Args:
            letter (str): Letter to encode

        Returns:
            str: Encoded letter
        """
        pos = self._alphabet.index(letter)
        return chr(pos + 65)

    def step(self, steps=1) -> None:
        """Steps the rotor by a set number of steps.

        Args:
            steps (int, optional): Number of steps. Defaults to 1.
        """
        self._position += steps
        self._alphabet.rotate(-steps)
        self._stepped = True

    def resetStep(self) -> None:
        """Resets the current status of the rotation."""
        self._stepped = False

    def _wrapOrd(self, position: int) -> int:
        """Wraps the ord of a letter in range 0-25

        Args:
            position (int)

        Returns:
            int
        """
        while position < 0:
            position += 25
        while position > 25:
            position -= 25
        return position

    @property
    def position(self) -> str:
        """Returns current position fo the rotor as a letter

        Returns:
            str
        """
        return chr(self._wrapOrd(self._position) + 65)

    @position.setter
    def position(self, position: str) -> None:
        """Sets the current position of the rotor as a letter."""
        if len(position) > 1 or position not in ascii_letters:
            raise ValueError(f"Invalid starting position {position}")

        self._alphabet.rotate(self._position)
        self._position = ord(position.upper()) - 65
        self._alphabet.rotate(-self._position)

    @property
    def alphabet(self) -> str:
        """Returns the alphabet of the rotor as a string.

        Returns:
            str
        """
        return "".join(self._alphabet)

    @property
    def hit_notch(self) -> bool:
        """Returns True if the rotor has hit a notch position in the current step, False otherwise.

        Returns:
            bool
        """
        return self._wrapOrd(self._position - 1) in self._notch and self._stepped

    @property
    def in_notch(self) -> bool:
        """Returns True if the rotor is in the notch position when the step is completed, False otherwise.

        Returns:
            bool
        """
        return self._wrapOrd(self._position) in self._notch and not self._stepped

    @property
    def model(self) -> str:
        """Returns rotor model.

        Returns:
            str
        """
        return self._model


class Stator(Rotor):
    def __init__(self, alphabet: str, model: str = None):
        # check if all letters are in the alphabet and if alphabet is valid
        if len(alphabet) != 26 or any(
            l not in alphabet.upper() for l in ascii_uppercase
        ):
            raise ValueError(f"Invalid stator alphabet ({alphabet})")

        self._alphabet = deque([a for a in alphabet])
        self._model = model

        # each letter should be mapped to itself
        if any(self.right(self.left(a)) != a for a in alphabet):
            raise ValueError(f"Invalid stator alphabet ({alphabet})")

    def __str__(self) -> str:
        return f"Alphabet: {''.join(self._alphabet)}"


class Enigma:
    def __str__(self) -> str:
        return (
            f"Enigma machine model {self.model}, built in {self.year}. "
            f"Current ETW: {self._etw if self._etw else 'N/A'}. "
            f"Current UKW: {self._ukw if self._ukw else 'N/A'}. "
            f"Current rotors position: {self.rotors_position}."
        )

    def __init__(self, **kwargs) -> None:
        """Create a Enigma machine. With default settings, it generates a version similar to 1938 model M3.

        Keyword Args:
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

        self._model = kwargs.get("model", "Custom")
        self._year = kwargs.get("year", 2022)
        self._max_rotors = kwargs.get("max_rotors")
        self._rotors = []
        self._etw = None
        self._ukw = None
        self._plugboard = []

    def addRotor(self, rotor: str, position: str = "A") -> None:
        """Adds a rotor to the machine.

        Args:
            rotor (str): Model of the rotor
            position (str, optional): Starting position of the rotor. Defaults to "A".

        Raises:
            ValueError: Too many rotors have been added
            ValueError: The rotor is not available in the current machine
        """
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

    def setRotors(self, *rotors: str) -> None:
        """Sets a variable number of rotors according to their model.
        Their starting positions are defaulted to "A".

        Shorthand for self.addRotor() called multiple times.
        """
        self._rotors = []
        for r in rotors:
            self.addRotor(r, "A")

    def removeRotors(self) -> None:
        """Removes all rotors from the current machine."""
        self._rotors = []

    def setRotorsPositions(self, pos: str) -> None:
        """Set configuration of the rotors

        Args:
            pos (str): String of characters corresponding to the position of each rotor.

        Raises:
            ValueError: Length of the position is different to the number of rotors
            ValueError: A character is not valid (not a letter in range A-Z)
        """
        if len(pos) != len(self._rotors):
            raise ValueError("Invalid rotors position")

        for x, p in enumerate(pos):
            if p not in ascii_letters:
                raise ValueError(f"Position {p} is not valid")
            self._rotors[x].position = p

    def setUKW(self, ukw: str) -> None:
        """Set the UKW (reflector) according to its model.

        Args:
            ukw (str): Model of the UKW

        Raises:
            ValueError: UKW model is not valid
        """
        try:
            self._ukw = Stator(self._ukw_map[ukw]["alphabet"], model=ukw)
        except KeyError:
            raise ValueError(f"Unknown ukw {ukw}")

    def setETW(self, etw: str) -> None:
        """Set the ETW (entry rotor) according to its model.

        Args:
            etw (str): Model of the ETW

        Raises:
            ValueError: ETW model is not valid
        """
        try:
            self._etw = Stator(self._etw_map[etw]["alphabet"], model=etw)
        except KeyError:
            raise ValueError(f"Unknown ukw {etw}")

    def setPlugboard(self, *plugs: str) -> None:
        """Set the plugboard for the current machine.

        Raises:
            ValueError: More than 10 plugs are provided
            ValueError: Plugboards are not all in "AB" form
        """
        if len(plugs) > 10:
            raise ValueError("Max 10 plugs are allowed")

        if any(len(p) != 2 for p in plugs):
            raise ValueError("Invalid plugs combinations")

        self._plugboard = [(x[0], x[1]) for x in plugs]

    def encode(self, clean: str, format_output: bool = False) -> str:
        """Encodes a string using the current configuration of the machine.
        Can output formatted strings.

        Args:
            clean (str): String to be encoded.
            format_output (bool, optional): If True, groups the encoded strings into 5 characters words. Defaults to False.

        Raises:
            Exception: No rotors have been added
            Exception: No UKWs have been set (if available)
            Exception: No ETWs have been set (if available)

        Returns:
            str: Encoded string
        """
        if not self._rotors:
            raise Exception("No rotors have been added")
        if self._ukw_map and not self._ukw:
            raise Exception("No UKW has been added")
        if self._etw_map and not self._etw:
            raise Exception("No ETW has been added")

        encoded = []

        for c in clean:
            if c not in ascii_letters:
                if not format_output:
                    encoded.append(c)
                continue

            # reset rotors
            for r in self._rotors:
                r.resetStep()

            # step last
            self._rotors[-1].step()

            # plugboard
            e = self._applyPlugboard(c)

            # rotors and stuff
            e = self._signalTravel(e)

            # plugboard
            e = self._applyPlugboard(e)

            # notches turnover happens when the button is depressed
            self._computeRotations()

            # append encoded character
            encoded.append(e)

        unformatted = "".join(encoded)
        if not format_output:
            return unformatted

        return self._formatOutput(unformatted)

    def _formatOutput(self, raw: str) -> str:
        """Format string by grouping words by 4 letters

        Args:
            raw (str): Raw, unformatted, string

        Returns:
            str: Formatted string
        """
        formatted = "".join(raw.split(" "))
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
        """Moves a signal (the letter) through the machine, effectively encoding it.
        Handles ETW, UKW and rotors.

        Args:
            c (str): Character to encode

        Returns:
            str: Encoded character
        """
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

    def _computeRotations(self) -> None:
        """Handles all the rotations of the rotors in the machine.
        This has to be called after each step.
        """
        for x in range(len(self._rotors) - 1, 0, -1):
            # notch stepping
            if self._rotors[x].hit_notch:
                self._rotors[x - 1].step()

            if self._rotors[x].in_notch and x < len(self._rotors) - 1:
                # double stepping
                self._rotors[x].step()
                self._rotors[x - 1].step()

    @property
    def rotors_position(self) -> str:
        return "".join(r.position for r in self._rotors)

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


def main():
    ...
    print("This should not happen")


if __name__ == "__main__":
    main()
