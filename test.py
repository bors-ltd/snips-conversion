from converter import convert


for quantity, source_unit, dest_unit, expected in [
    (17, "miles", None, "17 miles est égal à 27,36kilomètres"),
    (1024, "heures", None, "1 024 heures est égal à 3,69megasecond"),
    (80, "fahrenheit", None, "80 fahrenheit est égal à 26,67degrés Celsius"),
    (80, "degrés fahrenheit", None,
     "80 degrés fahrenheit est égal à 26,67degrés Celsius"),
    (300, "kelvins", None, "300 kelvins est égal à 26,85degrés Celsius"),
    (170, "centimètres", "pieds", "170 centimètres est égal à 5,58pieds"),
    (60, "miles par heure", "kilomètre heure",
     "60 miles par heure est égal à 96,56kilomètres par heures"),
    (80, "kilomètres à l'heure", "miles par heure",
     "80 kilomètres à l'heure est égal à 49,71miles par heures"),
    (2, "mètres", "pieds", "2 mètres est égal à 6,56pieds"),
    (537, "minutes", "heures", "537 minutes est égal à 8,95heures"),
    (40, "yards", None, "40 yards est égal à 36,58mètres"),
    (3, "gallons", "litres", "3 gallons est égal à 11,36litres"),
    (7, "livres", "grammes", "7 livres est égal à 3 175,15gram"),
    (20, "degrés", "fahrenheit", "20 degrés est égal à 68,0000004degrés Fahrenheit"),
    (4, "miles", "kilomètres", "4 miles est égal à 6,44kilomètres"),
    (2, "pouces", None, "2 pouces est égal à 50,8millimètres"),
    (1, "mètre", "pouces", "1 mètre est égal à 39,37pouces"),
]:
    message = convert(quantity, source_unit, dest_unit)
    assert message.strip() == expected, "%s != %s" % (message, expected)
