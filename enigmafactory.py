
from enigma import Enigma

class EnigmaFactory:
    def createEnigma(self, model: str = "M3") -> Enigma:
        kwargs = {}

        match model:
            case "Commercial":
                kwargs["rotors_map"] = {
                        "IC": {"alphabet": "DMTWSILRUYQNKFEJCAZBPGXOHV"}, "notch": ["Z"],
                        "IIC": {"alphabet": "HQZGPJTMOBLNCIFDYAWVEUSRKX"}, "notch": ["Z"],
                        "IIIC": {"alphabet": "UQNTLSZFMREHDPXKIBVYGJCWOA"}, "notch": ["Z"],
                }
                kwargs["ukw_map"] = None
                kwargs["etw_map"] = None
                kwargs["year"] = 1924
                kwargs["max_rotors"] = 3

            case "Rocket":
                kwargs["rotors_map"] = {
                        "I": {"alphabet": "JGDQOXUSCAMIFRVTPNEWKBLZYH"}, "notch": ["Z"],
                        "II": {"alphabet": "NTZPSFBOKMWRCJDIVLAEYUXHGQ"}, "notch": ["Z"],
                        "III": {"alphabet": "JVIUBHTCDYAKEQZPOSGXNRMWFL"}, "notch": ["Z"],
                }
                kwargs["ukw_map"] = {
                    "UKW": {"alphabet": "QYHOGNECVPUZTFDJAXWMKISRBL"},
                }
                kwargs["etw_map"] = {
                    "ETW": {"alphabet": "QWERTZUIOASDFGHJKPYXCVBNML"},
                }
                kwargs["year"] = 1941
                kwargs["max_rotors"] = 3

            case "Swiss":
                    kwargs["rotors_map"] = {
                        "I-K": {"alphabet": "PEZUOHXSCVFMTBGLRINQJWAYDK"}, "notch": ["Z"],
                        "II-K": {"alphabet": "ZOUESYDKFWPCIQXHMVBLGNJRAT"}, "notch": ["Z"],
                        "III-K": {"alphabet": "EHRVXGAOBQUSIMZFLYNWKTPDJC"}, "notch": ["Z"],
                    }
                    kwargs["ukw_map"] = {
                        "UKW-K": {"alphabet": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
                    }
                    kwargs["etw_map"] = {
                        "ETW-K": {"alphabet": "QWERTZUIOASDFGHJKPYXCVBNML"},
                    }
                    kwargs["year"] = 1939
                    kwargs["max_rotors"] = 3

            case "M3":
                    kwargs["rotors_map"] = {
                        "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                        "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                        "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                    }
                    kwargs["ukw_map"] = {
                        "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
                        "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
                        "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
                    }
                    kwargs["etw_map"] = None
                    kwargs["year"] = 1938
                    kwargs["max_rotors"] = 3

            case "M4":
                    kwargs["rotors_map"] = {
                        "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                        "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                        "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                        "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["J"]},
                        "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z"]},
                        "VI": {"alphabet": "JPGVOUMFYQBENHZRDKASXLICTW", "notch": ["Z", "M"]},
                        "VII": {"alphabet": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "notch": ["Z", "M"]},
                        "VIII": {"alphabet": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "notch": ["Z", "M"]},
                    }
                    kwargs["ukw_map"] = {
                        "A": {"alphabet": "EJMZALYXVBWFCRQUONTSPIKHGD"},
                        "B": {"alphabet": "YRUHQSLDPXNGOKMIEBFZCWVJAT"},
                        "C": {"alphabet": "FVPJIAOYEDRZXWGCTKUQSBNMHL"},
                        "BETA": {"alphabet": "LEYJVCNIXWPBQMDRTAKZGFUHOS"},
                        "GAMMA": {"alphabet": "FSOKANUERHMBTIYCWLQPZXVGJD"},
                    }
                    kwargs["etw_map"] = None
                    kwargs["year"] = 1938
                    kwargs["max_rotors"] = 4

            case "M4-Thin":
                    kwargs["rotors_map"] = {
                        "I": {"alphabet": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch": ["Q"]},
                        "II": {"alphabet": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch": ["E"]},
                        "III": {"alphabet": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch": ["V"]},
                        "IV": {"alphabet": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch": ["J"]},
                        "V": {"alphabet": "VZBRGITYUPSDNHLXAWMJQOFECK", "notch": ["Z"]},
                        "VI": {"alphabet": "JPGVOUMFYQBENHZRDKASXLICTW", "notch": ["Z", "M"]},
                        "VII": {"alphabet": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "notch": ["Z", "M"]},
                        "VIII": {"alphabet": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "notch": ["Z", "M"]},
                    }
                    kwargs["ukw_map"] = {
                        "A-Thin": {"alphabet": "ENKQAUYWJICOPBLMDXZVFTHRGS"},
                        "B-Thin": {"alphabet": "RDOBJNTKVEHMLFCWZAXGYIPSUQ"},
                    }
                    kwargs["etw_map"] = None
                    kwargs["year"] = 1939
                    kwargs["max_rotors"] = 4

            case _:
                raise ValueError(f"Invalid model. Valid models are: {', '.join(self.available_models)}")


        kwargs["model"] = model
        return Enigma(**kwargs)

    def __str__(self):
        return f"Class used to create historically accurate Enigma machines. Available models: {', '.join(self.available_models)}"

    @property
    def available_models(self):
        return ["Commercial", "Rocket", "Swiss", "M3", "M4", "M4-Thin"]

def main():
    factory = EnigmaFactory()
    e = factory.createEnigma()

if __name__ == "__main__":
    main()
