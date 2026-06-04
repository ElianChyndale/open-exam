"""False friends database — Spanish/English cognate traps."""

from __future__ import annotations

FALSE_FRIENDS: dict[str, dict[str, str]] = {
    "actualmente": {
        "correct": "currently / at present",
        "wrong": "actually",
        "note": "English 'actually' = en realidad",
    },
    "asistir": {
        "correct": "to attend",
        "wrong": "to assist / to help",
        "note": "English 'assist' = ayudar",
    },
    "atender": {
        "correct": "to attend to / to pay attention to",
        "wrong": "to attend (an event)",
        "note": "English 'attend an event' = asistir",
    },
    "bizarro": {
        "correct": "brave / gallant",
        "wrong": "bizarre / strange",
        "note": "English 'bizarre' = extraño / raro",
    },
    "carpeta": {
        "correct": "folder",
        "wrong": "carpet",
        "note": "English 'carpet' = alfombra",
    },
    "constipado": {
        "correct": "to have a cold",
        "wrong": "constipated",
        "note": "English 'constipated' = estreñido",
    },
    "decepción": {
        "correct": "disappointment",
        "wrong": "deception",
        "note": "English 'deception' = engaño",
    },
    "delito": {
        "correct": "crime / offense",
        "wrong": "delight",
        "note": "English 'delight' = delicia / encanto",
    },
    "disgusto": {
        "correct": "annoyance / displeasure",
        "wrong": "disgust (strong revulsion)",
        "note": "English 'disgust' = asco / repugnancia",
    },
    "embarazada": {
        "correct": "pregnant",
        "wrong": "embarrassed",
        "note": "English 'embarrassed' = avergonzada",
    },
    "enviar": {
        "correct": "to send",
        "wrong": "to envy",
        "note": "English 'envy' = envidiar",
    },
    "éxito": {
        "correct": "success",
        "wrong": "exit",
        "note": "English 'exit' = salida",
    },
    "fabrica": {
        "correct": "factory",
        "wrong": "fabric",
        "note": "English 'fabric' = tela / tejido",
    },
    "fábrica": {
        "correct": "factory",
        "wrong": "fabric",
        "note": "English 'fabric' = tela / tejido",
    },
    "ganga": {
        "correct": "bargain",
        "wrong": "gang",
        "note": "English 'gang' = pandilla",
    },
    "gracioso": {
        "correct": "funny / amusing",
        "wrong": "gracious",
        "note": "English 'gracious' = amable / cortés",
    },
    "introducir": {
        "correct": "to insert / to introduce (physically)",
        "wrong": "to introduce (a person)",
        "note": "English 'introduce a person' = presentar",
    },
    "largo": {
        "correct": "long",
        "wrong": "large",
        "note": "English 'large' = grande",
    },
    "lectura": {
        "correct": "reading",
        "wrong": "lecture",
        "note": "English 'lecture' = conferencia / clase magistral",
    },
    "librería": {
        "correct": "bookstore",
        "wrong": "library",
        "note": "English 'library' = biblioteca",
    },
    "molestar": {
        "correct": "to bother / to annoy",
        "wrong": "to molest (sexual assault)",
        "note": "English 'molest' = abusar sexualmente",
    },
    "novedad": {
        "correct": "news / novelty",
        "wrong": "novelty (only trivial new thing)",
        "note": "Can mean any new development",
    },
    "parentes": {
        "correct": "relatives",
        "wrong": "parents",
        "note": "English 'parents' = padres",
    },
    "parecer": {
        "correct": "to seem / to look like",
        "wrong": "to appear (formally)",
        "note": "English 'appear' = aparecer",
    },
    "pretender": {
        "correct": "to try / to attempt",
        "wrong": "to pretend",
        "note": "English 'pretend' = fingir",
    },
    "realizar": {
        "correct": "to carry out / to accomplish",
        "wrong": "to realize (become aware)",
        "note": "English 'realize' = darse cuenta",
    },
    "recordar": {
        "correct": "to remember",
        "wrong": "to record",
        "note": "English 'record' = grabar",
    },
    "robar": {
        "correct": "to steal / to rob",
        "wrong": "to rob (only a person)",
        "note": "Also means to burgle a place",
    },
    "sensible": {
        "correct": "sensitive",
        "wrong": "sensible (practical)",
        "note": "English 'sensible' = sensato / razonable",
    },
    "sopa": {
        "correct": "soup",
        "wrong": "soap",
        "note": "English 'soap' = jabón",
    },
    "suceso": {
        "correct": "event / happening",
        "wrong": "success",
        "note": "English 'success' = éxito",
    },
    "tuna": {
        "correct": "prickly pear cactus",
        "wrong": "tuna fish",
        "note": "English 'tuna' = atún",
    },
    "últimamente": {
        "correct": "lately / recently",
        "wrong": "ultimately",
        "note": "English 'ultimately' = finalmente",
    },
    "vaso": {
        "correct": "drinking glass",
        "wrong": "vase",
        "note": "English 'vase' = jarrón / florero",
    },
}


def lookup_false_friend(spanish_word: str) -> dict[str, str] | None:
    """Look up a Spanish false friend."""
    return FALSE_FRIENDS.get(spanish_word.lower().strip())


def is_false_friend(spanish_word: str, english_guess: str) -> bool:
    """Check if an English guess is the wrong meaning for a Spanish word."""
    entry = FALSE_FRIENDS.get(spanish_word.lower().strip())
    if not entry:
        return False
    return english_guess.lower().strip() in entry["wrong"].lower()
