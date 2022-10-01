"""This module contains the factory for a Enigma machine."""
import ujson
from pynigma import Enigma


class EnigmaFactory(Enigma):
    """This class handles the factory to generate historically accurate \
        Enigma machines."""

    def __init__(self) -> None:
        """Instantiate an Enigma machine.

        Settings have been sourced from \
        https://www.cryptomuseum.com/crypto/Enigma/wiring.htm
        """
        with open("settings.json") as f:
            self._settings = ujson.load(f)

    def __str__(self) -> str:
        """Return the string representation of the Enigma machine.

        Returns:
            str
        """
        return (
            f"Class used to create historically accurate Enigma machines. "
            f"Available models: {', '.join(self.available_models)}."
        )

    def createEnigma(self, model: str) -> Enigma:
        """Create an Enigma machine with the same settings as a model.

        Args:
            model (str): model name. \
                Check self.available_models to see a list of them

        Raises:
            ValueError: model is not valid

        Returns:
            Enigma
        """
        if self._settings.get(model):
            super().__init__(model=model, **self._settings[model])
            return self

        raise ValueError(
            f"Invalid model. Valid models are: {', '.join(self.available_models)}"
        )

    @property
    def available_models(self) -> list[str]:
        """Return list of models that can be created via the factory.

        Returns:
            list[str]
        """
        return [m for m in self._settings]


class CustomEnigmaFactory(Enigma):
    """Create a custom Enigma factory."""

    def __init__(self) -> None:
        """Instantiate the Enigma factory."""
        self._initSettings()

    def __str__(self) -> str:
        """Return the string representation of the Enigma Factory.

        Returns:
            str
        """
        return (
            f"Class used to create custom Enigma machines. "
            f"Current settings: {self.settings}"
        )

    def createCustomEnigma(self) -> Enigma:
        """Create an Enigma machine with custom parameters.

        Returns:
            Enigma
        """
        super().__init__(**self._settings)
        self._initSettings()
        return self

    def addCustomETW(self, model: str, alphabet: str) -> None:
        """Add a custom ETW to the machine.

        Args:
            model (str): model of the ETW
            alphabet (str): alphabet of the ETW
        """
        self._settings["etw_map"][model] = {"alphabet": alphabet}

    def addCustomUKW(self, model: str, alphabet: str) -> None:
        """Add a custom UKW to the machine.

        Args:
            model (str): model of the UKW
            alphabet (str): alphabet of the UKW
        """
        self._settings["ukw_map"][model] = {"alphabet": alphabet}

    def addCustomRotor(self, model: str, alphabet: str, notch: list[str]) -> None:
        """Add a custom rotor to the machine.

        Args:
            model (str): model of the rotor
            alphabet (str): alphabet of the rotor
            notch (list[str]): rotor notches
        """
        self._settings["rotors_map"][model] = {
            "alphabet": alphabet,
            "notch": [n for n in notch],
        }

    def setCustomModel(self, model: str) -> None:
        """Set a custom model name.

        Args:
            model (str): model name
        """
        self._settings["model"] = model

    def setCustomYear(self, year: int) -> None:
        """Set a custom year for the model.

        Args:
            year (int): model year

        Raises:
            ValueError: year is not an integer
        """
        if not isinstance(year, int):
            raise ValueError("Year is not a number")

        self._settings["year"] = year

    def setMaxRotors(self, max_rotors: int) -> None:
        """Set the number of maximum rotors in the machine.

        Args:
            max_rotors (int)
        """
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
        """Return the current settings of the custom Enigma machine.

        Returns:
            str
        """
        return ", ".join(
            f"{k.replace('_map', '')}: {v if v else 'not set'}"
            for k, v in self._settings.items()
        )
