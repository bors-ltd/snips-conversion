"""
Generate what Snips is to be expecting directly from the list of supported units.
"""
import itertools

from registry import PREFIXES, BINARY_PREFIXES, UNITS

# Maybe, maybe not, maybe more...
UNITS_WITH_PREFIXES = (
    "m", "s", "A", "g", "C", "V", "Ω", "T", "gauss", "J", "N", "Hz", "B", "bit",
    "W", "bar", "pc", "W", "Pa", "bar", "meter / hour", "meter / minute",
    "meter / second", "l", "meter ** 3",
)


def generate_slot(fp):
    # Sort the dicts for consistent output, remove with Python 3.6+
    for unit, synonyms in sorted(UNITS.items()):
        fp.write(",".join(synonyms) + "\n")
        if unit in UNITS_WITH_PREFIXES:
            prefixes = PREFIXES.values()
            if unit in ('B', 'bit'):
                prefixes = itertools.chain(prefixes, BINARY_PREFIXES.values())
            for prefix in sorted(prefixes):
                fp.write(",".join(prefix + synonym for synonym in synonyms) + "\n")


if __name__ == '__main__':
    with open("slot-unit.txt", 'w') as fp:
        generate_slot(fp)
