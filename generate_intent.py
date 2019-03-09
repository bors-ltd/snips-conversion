"""
Generate what Snips is to be expecting directly from the list of supported units.
"""
import re


SENTENCES = (
    "[17](quantity) [miles](source_unit), ça fait beaucoup ?",
    "Je mesure [170](quantity) [centimètres](source_unit), je mesure combien en [pieds](dest_unit) ?",
    "Si la vitesse est limitée à [60](quantity) [miles par heure](source_unit), à combien je peux rouler en [kilomètre heure](dest_unit) ?",
    "Si je roule à [80](quantity) [kilomètres à l'heure](source_unit), je roule à combien en [miles par heure](dest_unit) ?",
    "Si je fais [deux](quantity) [mètres](source_unit), ça fait combien en [pieds](dest_unit) ?",
    "[537](quantity) [minutes](source_unit), ça fait combien [d'heures](dest_unit) ?",
    "[Quarante](quantity) [yards](source_unit) en [miles](dest_unit), ça fait combien ?",
    "La conversion de [trois](quantity) [gallons](source_unit) en [litres](dest_unit) ?",
    "[7](quantity) [livres](source_unit) en [grammes](dest_unit) ?",
    "Donne-moi [20](quantity) [degrés](source_unit) en [fahrenheit](dest_unit)",
    "Ça fait combien [quatre](quantity) [miles](source_unit) en [kilomètres](dest_unit) ?",
    "Combien font [deux](quantity) [pouces](source_unit) ?",
    "Convertis [un](quantity) [mètre](source_unit) en [pouces](dest_unit)",
)

SOURCE_PATTERN = re.compile(r"\[([\w\s']+)\]\(source_unit\)", flags=re.UNICODE)
DEST_PATTERN = re.compile(r"\[([\w\s']+)\]\(dest_unit\)", flags=re.UNICODE)

# A mix of abbreviations sometimes Snips is giving without asking
# and alternative expressions we would say
ALTERNATIVES = {
    "miles": "miles",  # or "mailles"?
    "centimètres": "cm",
    "pieds": "pieds",
    "miles par heure": "miles à l'heure",
    "kilomètre heure": "kilomètres par heure",
    "kilomètres à l'heure": "kilomètres par heure",
    "mètres": "m",
    "minutes": "mn",  # As seen from Snips
    "d'heures": "en heures",
    "yards": "yards",
    "gallons": "gallons",  # "galons"?
    "litres": "l",
    "livres": "livres",
    "grammes": "g",
    "degrés": "degrés",
    "fahrenheit": "fahrenheit",
    "kilomètres": "km",
    "pouces": "pouces",
    "mètre": "m",
}


def replace_source(sentence, old_unit, new_unit):
    return sentence.replace(
        '[%s](source_unit)' % (old_unit,),
        '[%s](source_unit)' % (new_unit,),
    )


def replace_dest(sentence, old_unit, new_unit):
    return sentence.replace(
        '[%s](dest_unit)' % (old_unit,),
        '[%s](dest_unit)' % (new_unit,),
    )


def generate_intent(fp):
    for sentence in SENTENCES:
        sentences = [
            sentence,
        ]

        source_match = SOURCE_PATTERN.findall(sentence)
        source_unit = source_match[0] if source_match else None
        if source_unit:
            alternative = replace_source(
                sentence, source_unit, ALTERNATIVES[source_unit]
            )
            if alternative not in sentences:
                sentences.append(alternative)

        dest_match = DEST_PATTERN.findall(sentence)
        dest_unit = dest_match[0] if dest_match else None
        if dest_unit:
            alternative = replace_dest(
                sentence, dest_unit, ALTERNATIVES[dest_unit]
            )
            if alternative not in sentences:
                sentences.append(alternative)

        if source_unit and dest_unit:
            alternative = replace_source(
                replace_dest(
                    sentence, dest_unit, ALTERNATIVES[dest_unit]
                ),
                source_unit, ALTERNATIVES[source_unit]
            )
            if alternative not in sentences:
                sentences.append(alternative)

        fp.write("\n".join(sentences) + "\n")


if __name__ == '__main__':
    with open("intent-askUnit.txt", 'w') as fp:
        generate_intent(fp)
