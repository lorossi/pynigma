from enigma import Enigma


class EnigmaFactory:
    def __init__(self) -> None:
        self._settings = {
            "Commercial": {
                "rotors_map": {
                    "IC": {"alphabet": "DMTWSILRUYQNKFEJCAZBPGXOHV", "notch": ["Z"]},
                    "IIC": {"alphabet": "HQZGPJTMOBLNCIFDYAWVEUSRKX", "notch": ["Z"]},
                    "IIIC": {"alphabet": "UQNTLSZFMREHDPXKIBVYGJCWOA", "notch": ["Z"]},
                },
                "ukw_map": {},
                "etw_map": {},
                "year": 1924,
                "max_rotors": 3,
            },
            "Rocket": {
                "rotors_map": {
                    "I": {"alphabet": "JGDQOXUSCAMIFRVTPNEWKBLZYH", "notch": ["Z"]},
                    "II": {"alphabet": "NTZPSFBOKMWRCJDIVLAEYUXHGQ", "notch": ["Z"]},
                    "III": {"alphabet": "JVIUBHTCDYAKEQZPOSGXNRMWFL", "notch": ["Z"]},
                },
                "ukw_map": {"UKW": {"alphabet": "QYHOGNECVPUZTFDJAXWMKISRBL"}},
                "etw_map": {"ETW": {"alphabet": "QWERTZUIOASDFGHJKPYXCVBNML"}},
                "year": 1941,
                "max_rotors": 3,
            },
            "Swiss": {
                "rotors_map": {
                    "I-K": {"alphabet": "PEZUOHXSCVFMTBGLRINQJWAYDK", "notch": ["Z"]},
                    "II-K": {"alphabet": "ZOUESYDKFWPCIQXHMVBLGNJRAT", "notch": ["Z"]},
                    "III-K": {"alphabet": "EHRVXGAOBQUSIMZFLYNWKTPDJC", "notch": ["Z"]},
                },
                "ukw_map": {"UKW-K": {"alphabet": "IMETCGFRAYSQBZXWLHKDVUPOJN"}},
                "etw_map": {"ETW-K": {"alphabet": "QWERTZUIOASDFGHJKPYXCVBNML"}},
                "year": 1939,
                "max_rotors": 3,
            },
            "M3": {
                "rotors_map": {
                    "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                    "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                    "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                },
                "ukw_map": {
                    "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
                    "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
                    "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
                },
                "etw_map": {},
                "year": 1938,
                "max_rotors": 3,
            },
            "M4": {
                "rotors_map": {
                    "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                    "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                    "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                    "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["J"]},
                    "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z"]},
                    "VI": {
                        "alphabet": "JPGVOUMFYQBENHZRDKASXLICTW",
                        "notch": ["Z", "M"],
                    },
                    "VII": {
                        "alphabet": "NZJHGRCXMYSWBOUFAIVLPEKQDT",
                        "notch": ["Z", "M"],
                    },
                    "VIII": {
                        "alphabet": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
                        "notch": ["Z", "M"],
                    },
                },
                "ukw_map": {
                    "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
                    "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
                    "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
                },
                "etw_map": {},
                "year": 1938,
                "max_rotors": 4,
            },
            "M4-Thin": {
                "rotors_map": {
                    "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                    "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                    "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                    "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["J"]},
                    "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z"]},
                    "VI": {
                        "alphabet": "JPGVOUMFYQBENHZRDKASXLICTW",
                        "notch": ["Z", "M"],
                    },
                    "VII": {
                        "alphabet": "NZJHGRCXMYSWBOUFAIVLPEKQDT",
                        "notch": ["Z", "M"],
                    },
                    "VIII": {
                        "alphabet": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
                        "notch": ["Z", "M"],
                    },
                },
                "ukw_map": {
                    "A-Thin": {"alphabet": "ENKQAUYWJICOPBLMDXZVFTHRGS"},
                    "B-Thin": {"alphabet": "RDOBJNTKVEHMLFCWZAXGYIPSUQ"},
                },
                "etw_map": {},
                "year": 1939,
                "max_rotors": 4,
            },
        }

    def __str__(self) -> str:
        return f"Class used to create historically accurate Enigma machines. Available models: {', '.join(self.available_models)}"

    def createEnigma(self, model: str) -> Enigma:
        if self._settings.get(model):
            return Enigma(model=model, **self._settings[model])

        raise ValueError(
            f"Invalid model. Valid models are: {', '.join(self.available_models)}"
        )

    @property
    def available_models(self) -> list[str]:
        return [m for m in self._settings]


class CustomEnigmaFactory:
    def __init__(self) -> None:
        self._custom_rotors = {}
        self._custom_etw = {}
        self._custom_ukw = {}

    def __str__(self) -> str:
        return f"Class used to create custom Enigma machines."

    def createCustomEnigma(self) -> Enigma:
        raise NotImplementedError

    def addCustomETW(self, alphabet: str) -> None:
        raise NotImplementedError

    def addCustomUWK(self, alphabet: str) -> None:
        raise NotImplementedError

    def addCustomRotor(self, alphabet: str, notch: list[str]) -> None:
        raise NotImplementedError()
