"""
Generate what Snips is to be expecting directly from the list of supported units.
"""
import re


SENTENCES = (
    "[17](quantity) [pouces](source_unit), ça fait combien ?",
    "[64](quantity) [pieds](source_unit), ça fait beaucoup ?",
    "[80](quantity) [miles](source_unit), c'est long ?",
    "[60](quantity) [miles par heure](source_unit), c'est rapide ?",
    "[100](quantity) [degrés fahrenheit](source_unit), c'est chaud ?",
    "[11](quantity) [onces](source_unit), c'est lourd ?",
    "[3](quantity) [gallons](source_unit), c'est volumineux ?",
    "[20](quantity) [nœuds](source_unit), ça souffle fort ?",
    "[50](quantity) [milles marins](source_unit), c'est loin ?",
    "Convertis [2](quantity) [livres](source_unit)",
    "Convertis [1](quantity) [mètre](source_unit) en [pouces](dest_unit)",
    "La conversion de [3](quantity) [gallons](source_unit) en [litres](dest_unit) ?",
    "La conversion de [9](quantity) [pintes](source_unit) en [litres](dest_unit), s'il te plaît",
    "[537](quantity) [minutes](source_unit), ça fait combien [d'heures](dest_unit) ?",
    "[40](quantity) [yards](source_unit) en [miles](dest_unit), ça fait combien ?",
    "[7](quantity) [livres](source_unit) en [grammes](dest_unit) ?",
    "Donne-moi [20](quantity) [degrés](source_unit) en [fahrenheit](dest_unit)",
    "Ça fait combien [4](quantity) [miles](source_unit) en [kilomètres](dest_unit) ?",
    "Combien ça fait [6](quantity) [onces](source_unit) en [grammes](dest_unit) ?",
    "Il y a combien de [grammes](dest_unit) dans [1](quantity) [livre](source_unit) ?",
    "Il y a combien de [jours](dest_unit) dans [1](quantity) [année sidérale](source_unit) ?",
    "Je mesure [170](quantity) [centimètres](source_unit), je mesure combien en [pieds](dest_unit) ?",
    "Si je fais [2](quantity) [mètres](source_unit), ça fait combien en [pieds](dest_unit) ?",
    "Si la vitesse est limitée à [60](quantity) [miles par heure](source_unit), à combien je peux rouler en [kilomètre heure](dest_unit) ?",
    "Si je roule à [80](quantity) [kilomètres à l'heure](source_unit), je roule à combien en [miles par heure](dest_unit) ?",
    # "Quelle est la vitesse de la lumière ?",
)

SOURCE_PATTERN = re.compile(r"\[([\w\s']+)\]\(source_unit\)", flags=re.UNICODE)
DEST_PATTERN = re.compile(r"\[([\w\s']+)\]\(dest_unit\)", flags=re.UNICODE)

# A mix of abbreviations sometimes Snips is giving without asking
# and alternative expressions we would say
ALTERNATIVES = {
    "centimètres": "cm",
    "degrés fahrenheit": "fahrenheit",
    "d'heures": "en heures",
    "fahrenheit": "degrés fahrenheit",
    "gallons": "galons",
    "grammes": "g",
    "kilomètre heure": "kilomètres par heure",
    "kilomètres à l'heure": "kilomètres par heure",
    "kilomètres": "km",
    "litres": "l",
    "mètre": "m",
    "mètres": "m",
    "miles par heure": "miles à l'heure",
    "minutes": "mn",  # As seen from Snips
    "nœuds": "noeuds",
}


def replace_source(sentence, old_unit, new_unit):
    if not new_unit or not sentence:
        return
    return sentence.replace(
        '[%s](source_unit)' % (old_unit,),
        '[%s](source_unit)' % (new_unit,),
    )


def replace_dest(sentence, old_unit, new_unit):
    if not new_unit:
        return
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
                sentence, source_unit, ALTERNATIVES.get(source_unit)
            )
            if alternative and alternative not in sentences:
                sentences.append(alternative)

        dest_match = DEST_PATTERN.findall(sentence)
        dest_unit = dest_match[0] if dest_match else None
        if dest_unit:
            alternative = replace_dest(
                sentence, dest_unit, ALTERNATIVES.get(dest_unit)
            )
            if alternative and alternative not in sentences:
                sentences.append(alternative)

        if source_unit and dest_unit:
            alternative = replace_source(
                replace_dest(
                    sentence, dest_unit, ALTERNATIVES.get(dest_unit)
                ),
                source_unit, ALTERNATIVES.get(source_unit)
            )
            if alternative and alternative not in sentences:
                sentences.append(alternative)

        fp.write("\n".join(sentences) + "\n")


if __name__ == '__main__':
    with open("intent-askUnit.txt", 'w') as fp:
        generate_intent(fp)
