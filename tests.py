from math import factorial
from enigma import Enigma
from enigmafactory import EnigmaFactory

from random import randint, seed, choice, shuffle
from time import time
from string import ascii_uppercase

import unittest


STRING_LENGTH = 1000
TESTS_NUM = 250


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

    def _random_string(self, length: int = 3) -> str:
        return "".join([chr(randint(0, 25) + 65) for x in range(length)])

    def _simple_encode(self, a: str, format_output: bool = False) -> tuple[str, str]:
        e = Enigma()
        e.addRotor("I", "A")
        e.addRotor("II", "A")
        e.addRotor("III", "A")
        e.setUKW("A")

        encoded = e.encode(a, format_output)
        e.setRotorsPositions("AAA")
        decoded = e.encode(encoded)

        if not format_output:
            return a.upper(), decoded

        return e._formatOutput(a.upper()), decoded

    def _factory_hard_encode(self, e: Enigma):
        for _ in range(e.max_rotors):
            e.addRotor(choice(e.available_rotors))

        e.setUKW(choice(e.available_UKWs))

        pos = self._random_positions(len(e._rotors))
        clear = self._random_string(STRING_LENGTH)

        e.setRotorsPositions(pos)
        encoded = e.encode(clear)

        e.setRotorsPositions(pos)
        decoded = e.encode(encoded)

        return decoded, clear

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

        for _ in range(100):
            pos = self._random_positions(3)
            e.setRotorsPositions(pos)
            self.assertEqual(e.rotors_position, pos)

    def test_add_ukw(self):
        e = Enigma()

        for u in e._ukw_map:
            e.setUKW(u)

        with self.assertRaises(Exception):
            e.setUKW("ASD")

    def test_set_plugboard(self):
        e = Enigma()
        e.setPlugboard("AB", "CD", "EF")

        with self.assertRaises(Exception):
            e.setPlugboard("A", "D", "E")

        with self.assertRaises(Exception):
            e.setPlugboard("ABS", "CDS", "EFS")

        with self.assertRaises(Exception):
            e.setPlugboard(["AB" for _ in range(20)])

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
            e = Enigma()

            for _ in range(randint(3, 10)):
                e.addRotor(choice(e.available_rotors))

            e.setUKW(choice(e.available_UKWs))

            pos = self._random_positions(len(e._rotors))
            clear = self._random_string(STRING_LENGTH)

            e.setRotorsPositions(pos)
            encoded = e.encode(clear)

            e.setRotorsPositions(pos)
            decoded = e.encode(encoded)

            self.assertEqual(decoded, clear)

    def test_random_encoding_with_plugs(self):
        seed(time())

        for _ in range(TESTS_NUM):
            e = Enigma()

            for _ in range(randint(3, 10)):
                e.addRotor(choice(e.available_rotors))

            e.setUKW(choice(e.available_UKWs))
            e.setPlugboard(*self._random_plugs())

            pos = self._random_positions(len(e._rotors))
            clear = self._random_string(STRING_LENGTH)

            e.setRotorsPositions(pos)
            encoded = e.encode(clear)

            e.setRotorsPositions(pos)
            decoded = e.encode(encoded)

            self.assertEqual(decoded, clear)

    def test_extremely_long_strings(self):
        seed(time())
        e = Enigma()

        for _ in range(100):
            e.addRotor(choice(e.available_rotors))

        e.setUKW(e.available_UKWs[0])
        e.setPlugboard(*self._random_plugs())

        pos = self._random_positions(100)
        clear = self._random_string(1000)

        e.setRotorsPositions(pos)
        encoded = e.encode(clear)

        e.setRotorsPositions(pos)
        decoded = e.encode(encoded)

        self.assertEqual(decoded, clear)

    def test_factory(self):
        factory = EnigmaFactory()
        for model in factory.available_models:
            e = factory.createEnigma(model)
            self.assertEqual(e.model, model)

        e = factory.createEnigma("M4")
        with self.assertRaises(Exception):
            e.setRotors("I", "II", "III", "IV", "V", "VI", "VII")

        # Not working somehow
        for model in factory.available_models:
            e = factory.createEnigma(model)
            for _ in range(TESTS_NUM):
                self.assertEqual(*self._factory_hard_encode(e))


if __name__ == "__main__":
    unittest.main()
