# Pynigma

A modern implementation of the Enigma machine in Python.

## Background

In the past month I have finally managed to see [The Imitation Game](https://it.wikipedia.org/wiki/The_Imitation_Game), the famous 2014 movie *(yep, it took me a long while)* about Alan Turing and its incredible breaking of the german crypto machine [Enigma](https://en.wikipedia.org/wiki/Enigma_machine).

Since I was a kid, I have been really fascinated by this machine.
I couldn't understand how it worked, let alone how it was cracked without any kind of computer.

An *electromechanical machine* that was so secure that took years to be decrypted! That can't be true!

So, in order to understand a little bit more how this marvelous machine worked, I decided to try and implement by using the *best programming language ever and ever in the past, present and future or computers* (Python3).

For the first time I actually started using common sense and modern coding recommendations:

1. Type hinting
2. A meaningful and complete testing suite

I have to say, I don't regret this the least.
Making a proper set of tests really helped me a lot.

*Who could have ever imagined that?* Well.

At this point, there's almost more test than code.
*Isn't this how it should work?*

## How to use

The class `EnigmaFactory` creates Enigma machines based off real models, produced before and during WWII, while the class `CustomEnigmaFactory` allows you to create, well, Enigma machines with custom settings (rotors, plugboards and deflectors).

## Code reference

### Code snippets

#### Create a machine using the `EnigmaFactory` class

``` Python
f = EnigmaFactory()
print(f.models) # list all available models
for m in f.models:
  e = f.createEnigma(m)
  print(e) # get some infos about the machine
```

#### Create a custom machine using the `CustomEnigmaFactory` class

``` Python
# TODO
```

#### Compose an Enigma machine using the default `Enigma` class

By using the `Enigma` class, a *quasi-*replica of the 1938 model M3.

``` Python
# TODO
```

#### Encrypt and decrypt a message

``` Python
from Enigmafactory import EnigmaFactory

f = EnigmaFactory()
e = f.createEnigma("M3")

# list reflectors, rotors
print(e.availableRotors, e.available_UKWs, e.available_ETWs)
# setup rotors and reflectors
e.setRotors(["I", "III", "II"])
e.setUKW("UKW-B")
e.setETW("ETW")
# set rotors position
e.setRotorsPositions("AZE")
# set a plugboard (max 10)
e.setPlugboard(["AB", "DE", "KC", "QW"])

# now encode
print(e.encode("HELLO WORlD"))

# reset rotors positions
e.setRotorsPositions("AZE")

# now decode
print(e.decode("")) # TODO
```

## Credits

Thanks to [Crypto Museum](https://www.cryptomuseum.com/crypto/Enigma/wiring.html) for the rotors wiring and all the information about various models.
It's a really interesting website that you should check out!

## Licensing

This project is distributed under Attribution 4.0 International (CC BY 4.0) license.
