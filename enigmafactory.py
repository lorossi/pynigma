from pynigma import Enigma
import ujson


class EnigmaFactory(Enigma):
    def __init__(self) -> None:
        # settings sourced from https://www.cryptomuseum.com/crypto/enigma/wiring.htm
        # TODO remember to credit it in readme
        with open("settings.json") as f:
            self._settings = ujson.load(f)

    def __str__(self) -> str:
        return (
            f"Class used to create historically accurate Enigma machines. "
            f"Available models: {', '.join(self.available_models)}."
        )

    def createEnigma(self, model: str) -> Enigma:
        if self._settings.get(model):
            super().__init__(model=model, **self._settings[model])
            return self

        raise ValueError(
            f"Invalid model. Valid models are: {', '.join(self.available_models)}"
        )

    @property
    def available_models(self) -> list[str]:
        return [m for m in self._settings]


class CustomEnigmaFactory(Enigma):
    def __init__(self) -> None:
        self._initSettings()

    def __str__(self) -> str:
        return (
            f"Class used to create custom Enigma machines. "
            f"Current settings: {self.settings}"
        )

    def createCustomEnigma(self) -> Enigma:
        super().__init__(**self._settings)
        self._initSettings()
        return self

    def addCustomETW(self, model: str, alphabet: str) -> None:
        self._settings["etw_map"][model] = {"alphabet": alphabet}

    def addCustomUKW(self, model: str, alphabet: str) -> None:
        self._settings["ukw_map"][model] = {"alphabet": alphabet}

    def addCustomRotor(self, model: str, alphabet: str, notch: list[str]) -> None:
        self._settings["rotors_map"][model] = {
            "alphabet": alphabet,
            "notch": [n for n in notch],
        }

    def setCustomModel(self, model: str) -> None:
        self._settings["model"] = model

    def setCustomYear(self, year: int) -> None:
        if not isinstance(year, int):
            raise ValueError("Year is not a number")

        self._settings["year"] = year

    def setMaxRotors(self, max_rotors: int) -> None:
        self._settings["max_rotors"] = max_rotors

    def _initSettings(self) -> None:
        self._settings = {
            "rotors_map": {},
            "ukw_map": {},
            "etw_map": {},
            "max_rotors": None,
            "model": None,
            "year": None,
        }

    @property
    def settings(self) -> str:
        return ", ".join(
            f"{k.replace('_map', '')}: {v if v else 'not set'}"
            for k, v in self._settings.items()
        )
