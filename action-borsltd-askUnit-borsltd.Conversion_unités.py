#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from hermes_python.ontology import MqttOptions
from unit_converter import converter

import snips_common


# Basically the inverse of what unit-converter is expecting
PREFIXES = {
    "yocto": "y",
    "zepto": "z",
    "atto": "a",
    "femto": "f",
    "pico": "p",
    "nano": "n",
    "micro": "µ",
    "milli": "m",
    "centi": "c",
    "déci": "d",
    "déca": "da",
    "hecto": "h",
    "kilo": "k",
    "méga": "M",
    "giga": "G",
    "téra": "T",
    "péta": "P",
    "exa": "E",
    "zetta": "Z",
    "yotta": "Y",
}

UNITS = {
    # SI units
    "mètre": "m",
    "gramme": "g",
    "seconde": "s",
    "ampère": "A",
    "kelvin": "K",
    "mole": "mol",
    "candela": "cd",
    # Derived SI units
    "hertz": "Hz",
    "newton": "N",
    "pascal": "Pa",
    "joule": "J",
    "watt": "W",
    "coulomb": "C",
    "volt": "V",
    "ohm": "Ω",
    "siemens": "S",
    "farad": "F",
    "tesla": "T",
    "weber": "Wb",
    "henry": "H",
    "celsius": "°C",
    "degré": "°C",
    "degrés": "°C",
    "degré celsius": "°C",
    "degrés celsius": "°C",
    "radian": "rad",
    "steradian": "sr",
    "lumen": "lm",
    "lux": "lx",
    "becquerel": "Bq",
    "gray": "Gy",
    "sievert": "Sv",
    "katal": "kat",
    # Imperial system
    "fahrenheit": "°F",
    "degré fahrenheit": "°F",
    "degrés fahrenheit": "°F",
    "thou": "thou",
    "pouce": "inch",
    "pied": "foot",
    "yard": "yard",
    "chain": "chin",
    "furlong": "furlong",
    "mile": "mile",
    "league": "league",
    # Miscellaneous units
    "bar": "bar",
    "minute": "min",
    "heure": "h",
    # Extra
    "mètre par heure": "m*h^-1",
    "mètres par heure": "m*h^-1",
    "mile par heure": "mile*h^-1",
    "miles par heure": "mile*h^-1",
}

# The default is to convert to everyday units
DEFAULT_UNITS = {
    "K": ("degrés celsius", "", "°C"),
    "°F": ("degrés celsius", "", "°C"),
    "inch": ("centimètres", "c", "m"),
    "foot": ("centimètres", "c", "m"),
    "yard": ("mètres", "", "m"),
    "mile": ("mètres", "", "m"),
    "mile*h^-1": ("kilomètres par heure", "k", "m*h^-1"),
}


def parse_unit(full_unit):
    full_unit = full_unit.lower()
    base_unit = full_unit

    found_prefix = ""
    for prefix, abbreviation in PREFIXES.items():
        if full_unit.startswith(prefix):
            found_prefix = abbreviation
            base_unit = full_unit[len(prefix) :]
            break
    else:
        print("No prefix")

    print("found_prefix", found_prefix, "base_unit", base_unit)

    found_abbreviation = None
    for unit, abbreviation in UNITS.items():
        if base_unit == unit or base_unit[:-1] == unit:  # Remove plural
            found_abbreviation = abbreviation
            break
    else:
        raise UnknownUnit(base_unit)

    print("found_abbreviation", found_abbreviation)

    print(full_unit, "reads as", found_prefix + found_abbreviation)

    return found_prefix, found_abbreviation


class ConversionError(Exception):
    pass


class UnknownUnit(ConversionError):
    pass


class ActionWrapper(snips_common.ActionWrapper):
    reactions = {
        UnknownUnit: "Désolée, je ne sais pas convertir les {}",
        ConversionError: "Désolée, {}",
    }

    def __init__(self, hermes, intent_message):
        self.hermes = hermes
        self.intent_message = intent_message

    def action(self):
        """ Write the body of the function that will be executed once the intent is recognized.
        In your scope, you have the following objects :
        - intent_message : an object that represents the recognized intent
        - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol.
        - conf : a dictionary that holds the skills parameters you defined.
        To access global parameters use conf['global']['parameterName']. For end-user parameters use conf['secret']['parameterName']

        Refer to the documentation for further details.
        """
        slots = self.intent_message.slots
        quantity = slots.quantity.first().value
        source_unit = slots.source_unit.first().value
        dest_unit = slots.dest_unit.first().value if len(slots.dest_unit) else None
        print('quantity', quantity, 'source_unit', source_unit, 'dest_unit', dest_unit)

        source_prefix, source_abbreviation = parse_unit(source_unit)
        if dest_unit:
            dest_prefix, dest_abbreviation = parse_unit(dest_unit)
        else:
            try:
                dest_unit, dest_prefix, dest_abbreviation = DEFAULT_UNITS[
                    source_prefix + source_abbreviation
                ]
            except KeyError:
                raise ConversionError(
                    "Je ne sais pas encore choisir une unité par défaut."
                )
            print("fallback on", dest_prefix + dest_abbreviation)

        converted = converter.converts(
            "".join([str(quantity), source_prefix, source_abbreviation]),
            "".join([dest_prefix, dest_abbreviation]),
        )

        print("converted", converted)

        message = "{} {} est égal à {} {}.".format(
            snips_common.french_number(quantity),
            source_unit,
            "est égal à",
            snips_common.french_number(converted),
            dest_unit,
        )
        extra = "Mais vous le saviez déjà." if source_unit == dest_unit else ""

        self.end_session(message, extra)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()

    with Hermes(mqtt_options=mqtt_opts) as hermes:
        hermes.subscribe_intent("borsltd:askUnit", ActionWrapper.callback).start()
