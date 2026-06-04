"""Spanish morphology engine — conjugation, gender, and agreement rules."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ConjugationPattern:
    """A Spanish verb conjugation pattern."""

    infinitive: str
    mood: str  # indicative, subjunctive, imperative
    tense: str  # present, preterite, imperfect, future, conditional
    forms: dict[str, str] = field(default_factory=dict)

    def yo(self) -> str:
        return self.forms.get("yo", "")

    def tu(self) -> str:
        return self.forms.get("tú", "")

    def el_ella(self) -> str:
        return self.forms.get("él/ella", "")

    def nosotros(self) -> str:
        return self.forms.get("nosotros", "")

    def vosotros(self) -> str:
        return self.forms.get("vosotros", "")

    def ellos(self) -> str:
        return self.forms.get("ellos/ellas", "")


@dataclass
class GenderAgreement:
    """Spanish noun gender and number agreement."""

    lemma: str
    gender: Literal["masculine", "feminine", "both"]
    number_invariable: bool = False
    definite_article_sg: str = ""
    definite_article_pl: str = ""

    def with_article(self, number: Literal["singular", "plural"] = "singular") -> str:
        article = self.definite_article_sg if number == "singular" else self.definite_article_pl
        noun = self.lemma if number == "singular" else self._pluralize()
        return f"{article} {noun}"

    def _pluralize(self) -> str:
        if self.number_invariable:
            return self.lemma
        if self.lemma.endswith(("a", "e", "i", "o", "u")):
            return f"{self.lemma}s"
        if self.lemma.endswith(("z",)):
            return f"{self.lemma[:-1]}ces"
        return f"{self.lemma}es"


# Regular conjugation endings
_AR_ENDINGS = {
    "present": {"yo": "o", "tú": "as", "él/ella": "a", "nosotros": "amos", "vosotros": "áis", "ellos/ellas": "an"},
    "preterite": {"yo": "é", "tú": "aste", "él/ella": "ó", "nosotros": "amos", "vosotros": "asteis", "ellos/ellas": "aron"},
    "imperfect": {"yo": "aba", "tú": "abas", "él/ella": "aba", "nosotros": "ábamos", "vosotros": "abais", "ellos/ellas": "aban"},
    "future": {"yo": "aré", "tú": "arás", "él/ella": "ará", "nosotros": "aremos", "vosotros": "aréis", "ellos/ellas": "arán"},
    "conditional": {"yo": "aría", "tú": "arías", "él/ella": "aría", "nosotros": "aríamos", "vosotros": "aríais", "ellos/ellas": "arían"},
}

_ER_ENDINGS = {
    "present": {"yo": "o", "tú": "es", "él/ella": "e", "nosotros": "emos", "vosotros": "éis", "ellos/ellas": "en"},
    "preterite": {"yo": "í", "tú": "iste", "él/ella": "ió", "nosotros": "imos", "vosotros": "isteis", "ellos/ellas": "ieron"},
    "imperfect": {"yo": "ía", "tú": "ías", "él/ella": "ía", "nosotros": "íamos", "vosotros": "íais", "ellos/ellas": "ían"},
    "future": {"yo": "eré", "tú": "erás", "él/ella": "erá", "nosotros": "eremos", "vosotros": "eréis", "ellos/ellas": "erán"},
    "conditional": {"yo": "ería", "tú": "erías", "él/ella": "ería", "nosotros": "eríamos", "vosotros": "eríais", "ellos/ellas": "erían"},
}

_IR_ENDINGS = {
    "present": {"yo": "o", "tú": "es", "él/ella": "e", "nosotros": "imos", "vosotros": "ís", "ellos/ellas": "en"},
    "preterite": {"yo": "í", "tú": "iste", "él/ella": "ió", "nosotros": "imos", "vosotros": "isteis", "ellos/ellas": "ieron"},
    "imperfect": {"yo": "ía", "tú": "ías", "él/ella": "ía", "nosotros": "íamos", "vosotros": "íais", "ellos/ellas": "ían"},
    "future": {"yo": "iré", "tú": "irás", "él/ella": "irá", "nosotros": "iremos", "vosotros": "iréis", "ellos/ellas": "irán"},
    "conditional": {"yo": "iría", "tú": "irías", "él/ella": "iría", "nosotros": "iríamos", "vosotros": "iríais", "ellos/ellas": "irían"},
}

# Stem-changing verbs (e -> ie, o -> ue, e -> i)
STEM_CHANGES: dict[str, tuple[str, str]] = {
    # e -> ie
    "pensar": ("e", "ie"),
    "querer": ("e", "ie"),
    "entender": ("e", "ie"),
    "perder": ("e", "ie"),
    "cerrar": ("e", "ie"),
    "empezar": ("e", "ie"),
    "nevar": ("e", "ie"),
    "sentar": ("e", "ie"),
    # o -> ue
    "poder": ("o", "ue"),
    "dormir": ("o", "ue"),
    "volver": ("o", "ue"),
    "encontrar": ("o", "ue"),
    "morir": ("o", "ue"),
    "mover": ("o", "ue"),
    "recordar": ("o", "ue"),
    "resolver": ("o", "ue"),
    "sonar": ("o", "ue"),
    "contar": ("o", "ue"),
    # e -> i
    "pedir": ("e", "i"),
    "servir": ("e", "i"),
    "repetir": ("e", "i"),
    "seguir": ("e", "i"),
    "vestir": ("e", "i"),
}

# Irregular yo forms
IRREGULAR_YO: dict[str, str] = {
    "ser": "soy",
    "estar": "estoy",
    "ir": "voy",
    "tener": "tengo",
    "venir": "vengo",
    "hacer": "hago",
    "decir": "digo",
    "traer": "traigo",
    "caer": "caigo",
    "poner": "pongo",
    "salir": "salgo",
    "valer": "valgo",
    "saber": "sé",
    "ver": "veo",
    "dar": "doy",
    "conocer": "conozco",
    "conducir": "conduzco",
    "producir": "produzco",
    "traducir": "traduzco",
    "caber": "quepo",
    "haber": "he",
}

# Fully irregular verbs (present indicative only)
IRREGULAR_PRESENT: dict[str, dict[str, str]] = {
    "ser": {"yo": "soy", "tú": "eres", "él/ella": "es", "nosotros": "somos", "vosotros": "sois", "ellos/ellas": "son"},
    "estar": {"yo": "estoy", "tú": "estás", "él/ella": "está", "nosotros": "estamos", "vosotros": "estáis", "ellos/ellas": "están"},
    "ir": {"yo": "voy", "tú": "vas", "él/ella": "va", "nosotros": "vamos", "vosotros": "vais", "ellos/ellas": "van"},
    "tener": {"yo": "tengo", "tú": "tienes", "él/ella": "tiene", "nosotros": "tenemos", "vosotros": "tenéis", "ellos/ellas": "tienen"},
    "venir": {"yo": "vengo", "tú": "vienes", "él/ella": "viene", "nosotros": "venimos", "vosotros": "venís", "ellos/ellas": "vienen"},
    "decir": {"yo": "digo", "tú": "dices", "él/ella": "dice", "nosotros": "decimos", "vosotros": "decís", "ellos/ellas": "dicen"},
    "hacer": {"yo": "hago", "tú": "haces", "él/ella": "hace", "nosotros": "hacemos", "vosotros": "hacéis", "ellos/ellas": "hacen"},
    "haber": {"yo": "he", "tú": "has", "él/ella": "ha", "nosotros": "hemos", "vosotros": "habéis", "ellos/ellas": "han"},
}


def classify_verb(infinitive: str) -> Literal["ar", "er", "ir", "irregular"]:
    if infinitive in IRREGULAR_PRESENT:
        return "irregular"
    if infinitive.endswith("ar"):
        return "ar"
    if infinitive.endswith("er"):
        return "er"
    if infinitive.endswith("ir"):
        return "ir"
    return "irregular"


def conjugate(
    infinitive: str,
    mood: str = "indicative",
    tense: str = "present",
) -> ConjugationPattern:
    """Conjugate a Spanish verb for the given mood and tense.

    Supports indicative present, preterite, imperfect, future, conditional.
    """
    if mood != "indicative":
        # Fallback to present for unsupported moods
        return conjugate(infinitive, "indicative", "present")

    verb_class = classify_verb(infinitive)

    if verb_class == "irregular" and tense == "present":
        forms = IRREGULAR_PRESENT.get(infinitive, {})
        return ConjugationPattern(
            infinitive=infinitive,
            mood=mood,
            tense=tense,
            forms=dict(forms),
        )

    # Determine endings table
    if verb_class == "ar":
        endings = _AR_ENDINGS.get(tense, _AR_ENDINGS["present"])
        stem = infinitive[:-2]
    elif verb_class == "er":
        endings = _ER_ENDINGS.get(tense, _ER_ENDINGS["present"])
        stem = infinitive[:-2]
    elif verb_class == "ir":
        endings = _IR_ENDINGS.get(tense, _IR_ENDINGS["present"])
        stem = infinitive[:-2]
    else:
        endings = _AR_ENDINGS["present"]
        stem = infinitive

    # Apply stem changes for present tense
    if tense == "present" and infinitive in STEM_CHANGES:
        old_vowel, new_vowel = STEM_CHANGES[infinitive]
        # Replace last occurrence of old_vowel in stem
        idx = stem.rfind(old_vowel)
        if idx >= 0:
            stem = stem[:idx] + new_vowel + stem[idx + 1 :]

    # Build forms
    forms: dict[str, str] = {}
    for pronoun, ending in endings.items():
        forms[pronoun] = stem + ending

    # Apply irregular yo forms
    if tense == "present" and infinitive in IRREGULAR_YO:
        forms["yo"] = IRREGULAR_YO[infinitive]

    return ConjugationPattern(
        infinitive=infinitive,
        mood=mood,
        tense=tense,
        forms=forms,
    )


def detect_gender(noun: str) -> GenderAgreement:
    """Heuristic gender detection for Spanish nouns."""
    noun = noun.lower().strip()

    # Common masculine endings
    masculine_endings = ("o", "or", "ón", "ín", "és", "ma", "pa", "ta")
    # Common feminine endings
    feminine_endings = ("a", "dad", "tad", "tud", "ción", "sión", "ez", "eza", "umbre", "ie")

    # Exceptions: words ending in -a that are masculine
    masculine_a_exceptions = {
        "día", "mapa", "problema", "sistema", "tema", "idioma", "clima",
        "planeta", "poema", "programa", "fantasma", "drama", "esquema",
        "diagrama", "enigma", "sintagma", "lema", "emblema", "teorema",
    }

    # Words ending in -o that are feminine
    feminine_o_exceptions = {
        "mano", "moto", "foto", "radio", "polio",
    }

    if noun in masculine_a_exceptions:
        return GenderAgreement(
            lemma=noun,
            gender="masculine",
            definite_article_sg="el",
            definite_article_pl="los",
        )

    if noun in feminine_o_exceptions:
        return GenderAgreement(
            lemma=noun,
            gender="feminine",
            definite_article_sg="la",
            definite_article_pl="las",
        )

    # Check endings
    if noun.endswith(feminine_endings) and not noun.endswith(masculine_endings):
        return GenderAgreement(
            lemma=noun,
            gender="feminine",
            definite_article_sg="la",
            definite_article_pl="las",
        )

    if noun.endswith(masculine_endings):
        return GenderAgreement(
            lemma=noun,
            gender="masculine",
            definite_article_sg="el",
            definite_article_pl="los",
        )

    # Default: masculine for ambiguous
    return GenderAgreement(
        lemma=noun,
        gender="masculine",
        definite_article_sg="el",
        definite_article_pl="los",
    )


def pluralize(noun: str) -> str:
    """Pluralize a Spanish noun."""
    noun = noun.lower().strip()
    if noun.endswith(("s", "x", "z")):
        if noun.endswith("z"):
            return noun[:-1] + "ces"
        return noun
    if noun.endswith(("a", "e", "i", "o", "u")):
        return noun + "s"
    return noun + "es"


def agree_adjective(adjective: str, gender: Literal["masculine", "feminine"], number: Literal["singular", "plural"] = "singular") -> str:
    """Basic adjective agreement."""
    adj = adjective.lower().strip()
    if gender == "feminine" and number == "singular":
        if adj.endswith("o"):
            return adj[:-1] + "a"
    if gender == "masculine" and number == "plural":
        if adj.endswith(("o", "e")):
            return adj + "s"
        return adj + "es"
    if gender == "feminine" and number == "plural":
        if adj.endswith("o"):
            return adj[:-1] + "as"
        if adj.endswith("e"):
            return adj + "s"
        return adj + "es"
    return adj
