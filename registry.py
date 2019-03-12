import itertools

import pint
import pint.errors

from exceptions import UnknownUnit


# Translate prefixes to French
PREFIXES = {  # decimal prefixes
    'y': 'yocto',
    'z': 'zepto',
    'a': 'atto',
    'f': 'femto',
    'p': 'pico',
    'n': 'nano',
    'µ': 'micro',
    'm': 'milli',
    'c': 'centi',
    'd': 'déci',
    'da': 'déca',
    'h': 'hecto',
    'k': 'kilo',
    'M': 'méga',
    'G': 'giga',
    'T': 'téra',
    'P': 'péta',
    'E': 'exa',
    'Z': 'zetta',
    'Y': 'yotta',
}

BINARY_PREFIXES = {
    'Ki': 'kibi',
    'Mi': 'mebi',
    'Gi': 'gibi',
    'Ti': 'tebi',
    'Pi': 'pebi',
    'Ei': 'exbi',
    'Zi': 'zebi',
    'Yi': 'yobi',
}

# Translate units to French (I can't cover them all!)
UNITS = {
    # reference
    'm': ('mètre', 'mètres'),
    's': ('seconde', 'secondes'),
    'A': ('ampère', 'ampères'),
    'cd': ('candela', 'candelas'),
    'g': ('gramme', 'grammes'),
    'mol': ('mole', 'moles'),
    'K': ('kelvin', 'kelvins'),
    'rad': ('radian', 'radians'),
    'bit': ('bit', 'bits'),

    # Angle
    'turn': ('tour', 'tours', 'révolution', 'cycle', 'cercle'),
    'arcdeg': ('degré angulaire', "degré d'arc"),
    'arcmin': ('minute angulaire', "minute d'arc"),
    'arcsec': ('seconde angulaire', "seconde d'arc"),
    'sr': ('stéradian', 'stéradians'),

    # Area
    'are': ('are', 'ares'),
    'ha': ('hectare', 'hectares'),
    'm**2': ('mètre carré', 'mètres carré'),

    # EM
    'C': ('coulomb', 'coulombs'),
    'V': ('volt', 'volts'),
    'Ω': ('ohm', 'ohms'),
    'T': ('tesla', 'teslas'),
    'gauss': ('gauss',),

    # Energy
    'J': ('joule', 'joules'),
    'Wh': ('watt heure', 'watts heure'),
    'eV': ('électron volt', 'électrons volt'),
    'cal': ('calorie', 'calories'),

    # Force
    'N': ('newton', 'newtons'),

    # Frequency
    'Hz': ('hertz',),
    'rpm': ('tour par minute', 'tours par minute', 'révolution par minute', 'révolutions par minute'),

    # Information
    'B': ('octet', 'octets'),
    'Bd': ('baud', 'bauds'),

    # Length
    'Å': ('ångström', 'ångströms', 'angström', 'angströms', 'angstrœm', 'angstrœms'),
    'pc': ('parsec', 'parsecs'),
    'ly': ('année-lumière', 'années-lumière', 'année lumière', 'années lumière', 'al'),
    'au': ('unité astronomique', 'unités astronomique'),

    # Mass
    'carat': ('carat', 'carats'),

    # Photometry
    'lm': ('lumen', 'lumens'),
    'lx': ('lux',),

    # Power
    'W': ('watt', 'watts'),
    'metric_horsepower': ('cheval vapeur', 'chevaux vapeur'),

    # Pressure
    'Pa': ('pascal', 'pascals'),
    'bar': ('bar', 'bars'),
    'atm': ('atmosphère', 'atmosphères'),

    # Temperature
    'degC': ('celsius', 'degré', 'degrés', 'degré celsius', 'degrés celsius'),
    'degF': ('fahrenheit', 'degré fahrenheit', 'degrés fahrenheit'),

    # Time
    'min': ('minute', 'minutes', 'mn'),
    'hr': ('heure', 'heures'),
    'day': ('jour', 'jours'),
    'week': ('semaine', 'semaines'),
    'year': ('année', 'années'),
    'month': ('mois',),
    # Yes, the mix of singular and plural happened
    'sidereal_day': ('jour sidéral', 'jours sidéraux', 'jour sidéraux'),
    'sidereal_hour': ('heure sidérale', 'heures sidérales', 'heure sidérales'),
    'sidereal_minute': ('minute sidérale', 'minutes sidérales', 'minute sidérales'),
    'sidereal_second': ('seconde sidérale', 'secondes sidérales', 'seconde sidérales'),
    'sidereal_year': ('année sidérale', 'années sidérales', 'année sidérales'),
    'sidereal_month': ('mois sidéral', 'mois sidéraux'),
    'leap_year': ('année bissextile', 'années bissextiles', 'année bissextiles'),
    'julian_year': ('année julienne', 'années juliennes', 'année juliennes'),
    'gregorian_year': ('année grégorienne', 'années grégoriennes', 'année grégoriennes'),
    'millenium': ('millénaire', 'millénaires'),

    # Velocity
    'nmi': ('mille marin', 'milles marins', 'mille nautique', 'milles nautiques'),
    'knot': ('nœud', 'nœuds', 'noeud' 'noeuds'),
    'mile / hour': ('miles par heure', "miles à l'heure"),
    'meter / hour': (
        'mètre par heure', 'mètres par heure',
        "mètre à l'heure", "mètres à l'heure",
        'mètre heure', 'mètres heure',
    ),
    'meter / minute': ('mètre par minute', 'mètres par minute'),
    'meter / second': ('mètre par seconde', 'mètres par seconde'),

    # Volume
    'l': ('litre', 'litres'),
    'm**3': ('mètre cube', 'mètres cube'),
    'stere': ('stère', 'stères'),

    # USCSLengthInternational
    'inch': ('pouce', 'pouces'),
    'foot': ('pied', 'pieds'),
    'yard': ('yard', 'yards'),
    'mile': ('mile', 'miles'),

    # USCSLiquidVolume
    'US_pint': ('pinte', 'pintes'),
    'US_liquid_gallon': ('gallon', 'gallons'),

    # Avoirdupois
    'ounce': ('once', 'onces'),
    'pound': ('livre', 'livres'),

    # Constants TODO
    'c': ('vitesse de la lumière', 'la vitesse de la lumière'),
}

ureg = pint.UnitRegistry()

DEFAULT_UNITS = {
    # What general public is expecting when asking a temperature
    ureg.degK: ureg.degC,
    ureg.degF: ureg.degC,
}


def to_quantity(french_unit):
    """
    Translate a French unit into a Pint Quantity.

    Magnitude defaults to 1 (or whatever the definition says).
    """
    # Sometimes Snips would already give the abbreviation
    try:
        return ureg(french_unit)
    except pint.errors.UndefinedUnitError:
        pass
    french_unit = french_unit.lower()
    base_unit = french_unit

    found_prefix = ""
    for prefix, plain in itertools.chain(PREFIXES.items(), BINARY_PREFIXES.items()):
        if french_unit.startswith(plain):
            found_prefix = prefix
            base_unit = french_unit[len(plain):]
            break
    else:
        print("No prefix")

    print("found_prefix", found_prefix, "base_unit", base_unit)

    found_unit = None
    for unit, synonyms in UNITS.items():
        if base_unit in synonyms:
            found_unit = unit
            break
    else:
        raise UnknownUnit(base_unit)

    print("found_unit", found_unit)

    print(french_unit, "reads as", found_prefix + found_unit)

    return ureg(found_prefix + found_unit)
