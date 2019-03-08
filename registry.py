import pint
import pint.errors

from exceptions import UnknownUnit

# Translate French prefix to abbreviation
PREFIXES = {
    # decimal prefixes
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
    # binary prefixes
    "kibi": "Ki",
    "mebi": "Mi",
    "gibi": "Gi",
    "tebi": "Ti",
    "pebi": "Pi",
    "exbi": "Ei",
    "zebi": "Zi",
    "yobi": "Yi",
}

# Translate French units to abbreviation (I can't cover them all!)
UNITS = {
    # reference
    "mètre": "m",
    "seconde": "s",
    "ampère": "A",
    "candela": "cd",
    "gramme": "g",
    "mole": "mol",
    "kelvin": "K",
    "radian": "rad",
    "bit": "bit",
    # Angle
    "tour": "turn",
    "degré angulaire": "degree",
    "minute_angulaire": "arcminute",
    "seconde angulaire": "arcsecond",
    "stéradian": "sr",
    # Area
    "are": "are",
    "hectare": "ha",
    # EM
    "coulomb": "C",
    "volt": "V",
    "ohm": "Ω",
    "tesla": "T",
    "gauss": "gauss",
    # Energy
    "joule": "J",
    "watt heure": "Wh",
    # Force
    "newton": "N",
    "hertz": "Hz",
    "tour par minute": "rpm",
    "tours par minute": "rpm",
    # Information
    "octet": "B",
    "octets": "B",
    "baud": "Bd",
    "bauds": "Bd",
    # Length
    "angstrom": "Å",
    "parsec": "pc",
    "année lumière": "ly",
    "année-lumière": "ly",
    "unité astronomique": "au",
    "unités astronomique": "au",
    # Mass
    "carat": "carat",
    "carats": "carat",
    # Photometry
    "lumen": "lm",
    "lux": "lx",
    # Power
    "watt": "W",
    "watts": "W",
    "cheval vapeur": "metric_horsepower",
    "chevaux vapeur": "metric_horsepower",
    # Pressure
    "mercure": "Hg",
    "pascal": "Pa",
    "bar": "bar",
    "atmosphère": "atm",
    # Temperature
    "celsius": "celsius",
    "degré": "celsius",
    "degrés": "celsius",
    "degré celsius": "celsius",
    "degrés celsius": "celsius",
    "fahrenheit": "fahrenheit",
    "degré fahrenheit": "fahrenheit",
    "degrés fahrenheit": "fahrenheit",
    # Time
    "mn": "minute",  # XXX Snips abbreviating
    "minute": "minute",
    "minutes": "minute",
    "heure": "hour",
    "heures": "hour",
    "jour": "day",
    "jours": "day",
    "semaine": "week",
    "semaines": "week",
    "année": "year",
    "années": "year",
    "mois": "month",
    "jour sidéral": "sidereal_day",
    "jours sidéraux": "sidereal_day",
    "heure sidérale": "sidereal_hour",
    "heures sidérales": "sidereal_hour",
    "minute sidérale": "sidereal_minute",
    "minutes sidérales": "sidereal_minute",
    "seconde sidérale": "sidereal_second",
    "secondes sidérales": "sidereal_second",
    "année sidérale": "sidereal_year",
    "années sidérales": "sidereal_year",
    "mois sidéral": "sidereal_month",
    "mois sidéraux": "sidereal_month",
    "année bissextile": "leap_year",
    "années bissextiles": "leap_year",
    "année julienne": "julian_year",
    "années juliennes": "julian_year",
    "année grégorienne": "gregorian_year",
    "années grégoriennes": "gregorian_year",
    "millénaire": "millenium",
    # Velocity
    "mile nautique": "nmi",
    "miles nautiques": "nmi",
    "mille nautique": "nmi",  # XXX
    "milles nautiques": "nmi",  # XXX
    "mile marin": "nmi",
    "miles marins": "nmi",
    "mille nautique": "nmi",  # XXX
    "milles nautiques": "nmi",  # XXX
    "noeud": "knot",
    "noeuds": "knot",
    "mile par heure": "mile / hour",
    "miles par heure": "mile / hour",
    "mètre par heure": "meter / hour",
    "mètres par heure": "meter / hour",
    "mètre heure": "meter / hour",
    "mètres heure": "meter / hour",
    "mètre par minute": "meter / minute",
    "mètres par minute": "meter / minute",
    "mètre par seconde": "meter / second",
    "mètres par seconde": "meter / second",
    # Volume
    "litre": "l",
    "litres": "l",
    "mètre cube": "meter ** 3",
    "stère": "stere",
    # USCSLengthInternational
    "pouce": "inch",
    "pouces": "inch",
    "pied": "foot",
    "pieds": "foot",
    "yard": "yard",
    "yards": "yard",
    "mile": "mile",
    "miles": "mile",
    # USCSLiquidVolume
    "pinte": "US_pint",
    "gallon": "US_liquid_gallon",
    # Avoirdupois
    "once": "ounce",
    "onces": "ounce",
    "livre": "pound",
    "livres": "pound",
    # Constants
    "vitesse de la lumière": "c",  # Cheat by saying "une vitesse de la lumière"
}


ureg = pint.UnitRegistry()


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
    for prefix, abbreviation in PREFIXES.items():
        if french_unit.startswith(prefix):
            found_prefix = abbreviation
            base_unit = french_unit[len(prefix) :]
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

    print(french_unit, "reads as", found_prefix + found_abbreviation)

    return ureg(found_prefix + found_abbreviation)
