from enigma import Enigma
import ujson


class EnigmaFactory:
    def __init__(self) -> None:
        # settings sourced from https://www.cryptomuseum.com/crypto/enigma/wiring.htm
        # TODO remember to credit it in readme
        with open("settings.json") as f:
            self._settings = ujson.load(f)

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
        e = Enigma(
            rotors_map=self._custom_rotors,
            etw_map=self._custom_etw,
            ukw_map=self._custom_ukw,
        )
        self._custom_rotors = {}
        self._custom_etw = {}
        self._custom_ukw = {}
        return e

    def addCustomETW(self, model: str, alphabet: str) -> None:
        self._custom_etw[model] = {"alphabet": alphabet}

    def addCustomUKW(self, model: str, alphabet: str) -> None:
        self._custom_ukw[model] = {"alphabet": alphabet}

    def addCustomRotor(self, model: str, alphabet: str, notch: list[str]) -> None:
        self._custom_rotors[model] = {"alphabet": alphabet, "notch": [n for n in notch]}
