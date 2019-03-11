import pint.errors
import snips_common

import exceptions
import registry


def convert(quantity, source_unit, dest_unit):
    """
    Natural (French) language converter.

    See tests for examples.
    """
    source_quantity = registry.to_quantity(source_unit)

    if dest_unit:
        dest_quantity = registry.to_quantity(dest_unit)
    else:
        # Keep, e.g. Celsius as the default temperature unit, or let Pint choose
        dest_quantity = registry.DEFAULT_UNITS.get(source_quantity.units)

    # Must be called this way for the temperature (absolute versus relative unit)
    source_quantity = registry.ureg.Quantity(quantity, source_quantity)
    if dest_quantity:
        try:
            dest_quantity = source_quantity.to(dest_quantity)
        except pint.errors.DimensionalityError:
            raise exceptions.UnknownUnit(
                "{} en {}".format(source_unit, dest_unit)
            )
    else:
        # Let Pint choose the default unit among SI units, and prefix it
        dest_quantity = (
            source_quantity.to_base_units().to_reduced_units().to_compact()
        )

    converted = dest_quantity.format_babel(locale='fr_FR')
    print("converted", converted)

    # Quick fix how the number will be said
    magnitude, converted = converted.split(" ", 1)
    magnitude = snips_common.french_number(magnitude)
    # Work around Pint bug: https://github.com/hgrecco/pint/pull/773
    converted = converted.replace("{0}", "")
    # Quick fix how the unit will be said
    converted = converted.replace("²", " carré")
    converted = converted.replace("³", " cube")
    converted = magnitude + converted

    return "{} {} est égal à {}".format(
        snips_common.french_number(quantity), source_unit, converted
    )
