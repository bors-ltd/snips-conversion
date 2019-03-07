#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from hermes_python.ontology import MqttOptions

import snips_common

import exceptions
import registry


class ActionConversion(snips_common.ActionWrapper):
    reactions = {
        exceptions.UnknownUnit: "Désolée, je ne sais pas convertir les {}",
        exceptions.ConversionError: "Désolée, {}",
    }

    def action(self):
        slots = self.intent_message.slots
        quantity = slots.quantity.first().value
        source_unit = slots.source_unit.first().value
        dest_unit = slots.dest_unit.first().value if len(slots.dest_unit) else None
        print('quantity', quantity, 'source_unit', source_unit, 'dest_unit', dest_unit)

        source_quantity = registry.to_quantity(source_unit)
        dest_quantity = registry.to_quantity(dest_unit) if dest_unit else None

        source_quantity = quantity * source_quantity
        if dest_quantity:
            dest_quantity = source_quantity.to(dest_quantity)
        else:
            dest_quantity = source_quantity.to_base_units().to_reduced_units()

        converted = dest_quantity.format_babel(locale='fr_FR')
        print("converted", converted)

        # Quick fix how the number will be said
        magnitude, converted = converted.split(' ', 1)
        magnitude = snips_common.french_number(magnitude)
        if converted.startswith('{0}'):
            # Bypass Babel or Pint bug
            converted = converted[3:]
        # Quick fix how the unit will be said
        converted = converted.replace('³', " cube")
        converted = magnitude + converted

        message = "{} {} est égal à {}".format(
            snips_common.french_number(quantity),
            source_unit,
            converted,
        )
        self.end_session(message)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()

    with Hermes(mqtt_options=mqtt_opts) as hermes:
        hermes.subscribe_intent("borsltd:askUnit", ActionConversion.callback).start()
