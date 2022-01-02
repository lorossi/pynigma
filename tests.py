from enigma import Enigma
from enigmafactory import EnigmaFactory, CustomEnigmaFactory

from random import randint, seed, choice, shuffle
from time import time
from string import ascii_uppercase

import unittest


STRING_LENGTH = 100
LONG_STRING_LENGTH = 5000
TESTS_NUM = 500


class TestEnigma(unittest.TestCase):
    def _random_positions(self, rotors: int = 3) -> str:
        return "".join([chr(randint(0, 25) + 65) for _ in range(rotors)])

    def _random_plugs(self) -> list[str]:
        alphabet = [c for c in ascii_uppercase]
        shuffle(alphabet)
        plugs = []

        while len(plugs) < 10:
            a = alphabet.pop()
            b = alphabet.pop()

            plugs.append("".join([a, b]))

        return plugs

    def _random_string(self, length: int = 3) -> list[str, str]:
        return "".join([chr(randint(0, 25) + 65) for x in range(length)])

    def _random_alphabet(self) -> str:
        letters = [x for x in ascii_uppercase]
        shuffle(letters)
        return "".join(letters)

    def _random_stator(self) -> str:
        letters = [x for x in ascii_uppercase]
        shuffle(letters)

        pairs = []
        for x in range(0, len(letters), 2):
            pairs.append((letters[x], letters[x + 1]))
        pairs.sort(key=lambda x: x[0])

        stator = [None for _ in range(26)]

        for p in pairs:
            start = ord(p[0]) - 65
            end = ord(p[1]) - 65
            stator[start] = p[1]
            stator[end] = p[0]

        return "".join(stator)

    def _random_notch(self, length: int = 1) -> list[str]:
        letters = [x for x in ascii_uppercase]
        shuffle(letters)
        notch = []
        for _ in range(length):
            notch.append(letters.pop())
        return notch

    def _simple_encode(
        self, clear: str, format_output: bool = False
    ) -> tuple[str, str]:
        e = Enigma()
        e.addRotor("I", "A")
        e.addRotor("II", "A")
        e.addRotor("III", "A")
        e.setUKW("A")

        encoded = e.encode(clear, format_output)
        e.setRotorsPositions("AAA")
        decoded = e.encode(encoded)

        if not format_output:
            return clear.upper(), decoded

        return e._formatOutput(clear.upper()), decoded

    def _hard_encode(
        self, length: int = STRING_LENGTH, max_rotors: int = 10, plugs: bool = False
    ) -> tuple[str, str]:
        e = Enigma()

        for _ in range(max_rotors):
            e.addRotor(choice(e.available_rotors))

        e.setUKW(choice(e.available_UKWs))

        pos = self._random_positions(len(e._rotors))
        clear = self._random_string(length)

        if plugs:
            e.setPlugboard(*self._random_plugs())

        e.setRotorsPositions(pos)
        encoded = e.encode(clear)

        e.setRotorsPositions(pos)
        decoded = e.encode(encoded)

        return clear, decoded

    def test_create_enigma(self):
        e = Enigma()
        self.assertEqual(e.year, 2022)
        self.assertEqual(e.model, "Custom")

    def test_add_rotors(self):
        e = Enigma()

        for r in e._rotors_map:
            e.addRotor(r, "A")

        for r in e._rotors_map:
            e.addRotor(r)

        with self.assertRaises(Exception):
            e.addRotor("ASD")

    def test_remove_rotors(self):
        e = Enigma()
        e.addRotor("I", "A")
        e.removeRotors()

        with self.assertRaises(Exception):
            e.encode("ASD")

    def test_rotors_position(self):
        e = Enigma()
        e.setUKW("A")
        e.setRotors("I", "II", "III")

        for _ in range(TESTS_NUM):
            pos = self._random_positions(3)
            e.setRotorsPositions(pos)
            self.assertEqual(e.rotors_position, pos)

    def test_add_ukw(self):
        e = Enigma()

        for u in e.available_UKWs:
            e.setUKW(u)

        with self.assertRaises(Exception):
            e.setUKW("ASD")

    def test_set_plugboard(self):
        e = Enigma()
        e.setPlugboard("AB", "CD", "EF")
        self.assertEqual(e.plugboard, ["AB", "CD", "EF"])

        with self.assertRaises(Exception):
            e.setPlugboard("A", "D", "E")

        with self.assertRaises(Exception):
            e.setPlugboard("ABS", "CDS", "EFS")

        with self.assertRaises(Exception):
            e.setPlugboard(["AB" for _ in range(20)])

        for _ in range(TESTS_NUM):
            plug = self._random_plugs()
            e.setPlugboard(*plug)
            self.assertEqual(plug, e.plugboard)

    def test_positions(self):
        e = Enigma()
        e.setRotors("I", "I", "I")
        e.setUKW("A")
        e.setRotorsPositions("ZZZ")

        self.assertEqual(e.rotors_position, "ZZZ")

        for _ in range(5):
            pos = self._random_positions()
            e.setRotorsPositions(pos)
            self.assertEqual(pos, e.rotors_position)

        with self.assertRaises(Exception):
            e.setRotorsPositions("AA3")
        with self.assertRaises(Exception):
            e.setRotorsPositions("")
        with self.assertRaises(Exception):
            e.setRotorsPositions("ASDSADADASD")

    def test_double_stepping(self):
        e = Enigma()
        e.setRotors("I", "II", "III")
        e.setUKW("A")
        e.setRotorsPositions("ADT")
        positions = ["ADU", "ADV", "AEW", "BFX", "BFY"]

        while positions:
            e.encode("A")
            self.assertEqual(e.rotors_position, positions.pop(0))

        e.setRotors("III", "II", "I")
        e.setRotorsPositions("KDO")
        positions = ["KDP", "KDQ", "KER", "LFS", "LFT", "LFU"]

        while positions:
            e.encode("A")
            self.assertEqual(e.rotors_position, positions.pop(0))

        e.setRotors("I", "II", "III")
        e.setRotorsPositions("AAT")
        positions = ["AAU", "AAV", "ABW", "ABX"]
        while positions:
            e.encode("A")
            self.assertEqual(e.rotors_position, positions.pop(0))

    def test_simple_encoding(self):
        self.assertEqual(*self._simple_encode("AAAAAA"))
        self.assertEqual(*self._simple_encode("Ma che bel castello"))
        self.assertEqual(*self._simple_encode("Nel mezzo del cammin di nostra vita..."))
        self.assertEqual(*self._simple_encode("12345 AAAA 5678"))
        self.assertEqual(*self._simple_encode("!!!!?? !!"))

    def test_formatted_simple_encoding(self):
        self.assertEqual(*self._simple_encode("AAAAA", True))
        self.assertEqual(
            *self._simple_encode("Theres nothing more in life than love", True)
        )
        self.assertEqual(
            *self._simple_encode("Pepsi is better than that terrible coca cola", True)
        )

    def test_random_encoding(self):
        seed(time())

        for _ in range(TESTS_NUM):
            self.assertEqual(*self._hard_encode())

    def test_random_encoding_with_plugs(self):
        seed(time())

        for _ in range(TESTS_NUM):
            self.assertEqual(*self._hard_encode(plugs=True))

    def test_extremely_long_strings(self):
        seed(time())

        self.assertEqual(
            *self._hard_encode(plugs=True, length=LONG_STRING_LENGTH, max_rotors=100)
        )

    def test_factory(self):
        f = EnigmaFactory()
        settings = f._settings

        for model in f.available_models:
            e = f.createEnigma(model)
            self.assertEqual(e.model, model)
            self.assertEqual(e.year, settings[e.model]["year"])
            self.assertEqual(settings[e.model]["max_rotors"], e.max_rotors)
            self.assertEqual(
                [k for k in settings[e.model]["rotors_map"].keys()], e.available_rotors
            )
            self.assertEqual(
                [k for k in settings[e.model]["ukw_map"].keys()], e.available_UKWs
            )
            self.assertEqual(
                [k for k in settings[e.model]["etw_map"].keys()], e.available_ETWs
            )

        e = f.createEnigma("M4")
        with self.assertRaises(Exception):
            e.setRotors("I", "II", "III", "IV", "V", "VI", "VII")

        with self.assertRaises(Exception):
            e.setETW("A")

        with self.assertRaises(Exception):
            e.setUKW("Z")

        with self.assertRaises(Exception):
            f.createEnigma("British")

        for model in f.available_models:
            for _ in range(TESTS_NUM):
                e = f.createEnigma(model)

                for _ in range(e.max_rotors):
                    e.addRotor(choice(e.available_rotors))

                if e.available_UKWs:
                    e.setUKW(choice(e.available_UKWs))

                if e.available_ETWs:
                    e.setETW(choice(e.available_ETWs))

                pos = self._random_positions(len(e._rotors))
                clear = self._random_string(STRING_LENGTH)

                e.setRotorsPositions(pos)
                encoded = e.encode(clear)

                e.setRotorsPositions(pos)
                decoded = e.encode(encoded)

                self.assertEqual(decoded, clear)

    def test_custom_factory(self):
        f = CustomEnigmaFactory()

        for _ in range(TESTS_NUM):
            for x in range(randint(3, 10)):
                f.addCustomRotor(
                    str(x), self._random_alphabet(), self._random_notch(length=2)
                )

            f.addCustomETW("A", self._random_stator())
            f.addCustomUKW("B", self._random_stator())

            e = f.createCustomEnigma()

            for _ in range(5):
                e.addRotor(choice(e.available_rotors))

            e.setETW("A")
            e.setUKW("B")
            e.setPlugboard(*self._random_plugs())

            pos = self._random_positions(len(e._rotors))
            clear = self._random_string(STRING_LENGTH)

            e.setRotorsPositions(pos)
            encoded = e.encode(clear)

            e.setRotorsPositions(pos)
            decoded = e.encode(encoded)

            self.assertEqual(decoded, clear)


if __name__ == "__main__":
    unittest.main()
