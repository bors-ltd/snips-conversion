"""
Generate what Snips is to be expecting directly from the list of supported units.
"""
from registry import PREFIXES, UNITS

# Maybe, maybe not...
UNITS_WITH_PREFIXES = (
    "mètre", "seconde", "ampère", "gramme", "coulomb", "volt", "ohm", "tesla",
    "gauss", "joule", "newton", "octet", "octets", "watt", "watts", "bar",
    "litre", "litres", "mètre cube",
)


def generate_slot(fp):
    for unit in sorted(UNITS):
        if unit in UNITS_WITH_PREFIXES:
            for prefix in PREFIXES:
                fp.write(prefix + unit + "\n")
        else:
            fp.write(unit + "\n")


if __name__ == '__main__':
    with open("slot-unit.txt", 'w') as fp:
        generate_slot(fp)
