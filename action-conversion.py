#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from hermes_python.ontology import MqttOptions

import snips_common

import converter
import exceptions


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
        print(
            'quantity', quantity,
            'source_unit', source_unit,
            'dest_unit', dest_unit
        )

        message = converter.convert(quantity, source_unit, dest_unit)
        self.end_session(message)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()

    with Hermes(mqtt_options=mqtt_opts) as hermes:
        hermes.subscribe_intent(
            "borsltd:askUnit", ActionConversion.callback
        ).start()
