from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version

from odiatranslit import from_roman, to_roman

from app_constants import (
    DIRECTION_FILE_LABELS,
    GITHUB_URL,
    ODIA_TO_ROMAN,
    PACKAGE_NAME,
    SCHEME_LABELS,
    TOOL_URL,
)

IST_TIMEZONE = timezone(timedelta(minutes=330), "IST")

_ZWNJ = "\u200c"
_ZWJ = "\u200d"
_ODIA_VIRAMA = "\u0b4d"


@lru_cache(maxsize=1)
def installed_package_version() -> str:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unknown"


def build_download_file(
    source_text: str,
    converted_text: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> tuple[str, str]:
    converted_at = datetime.now(IST_TIMEZONE)
    filename = f"odia-transliteration_{converted_at.strftime('%Y%m%d_%H%M%S')}.txt"
    title = "Odia Transliterate - Conversion Record"
    mode = "Reversible" if reversible else "Standard"

    metadata = [
        ("Direction", DIRECTION_FILE_LABELS[direction]),
        ("Scheme", SCHEME_LABELS[scheme]),
        ("Mode", mode),
        ("Converted", f"{converted_at.strftime('%Y-%m-%d %H:%M:%S %Z')} (UTC+5:30)"),
        ("Library", f"{PACKAGE_NAME} v{installed_package_version()}"),
        ("Tool", TOOL_URL),
        ("Source", GITHUB_URL),
    ]
    label_width = max(len(label) for label, _ in metadata) + 2
    metadata_block = "\n".join(
        f"{label:<{label_width}}: {value}" for label, value in metadata
    )

    body = (
        f"{title}\n{'=' * len(title)}\n\n"
        f"INPUT\n-----\n{source_text}\n\n"
        f"OUTPUT\n------\n{converted_text}\n\n\n\n"
        f"DETAILS\n-------\n{metadata_block}\n"
    )
    return filename, body


@lru_cache(maxsize=16)
def transliterate_text(
    source_text: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> str:
    if not source_text.strip():
        return ""
    if direction == ODIA_TO_ROMAN:
        return to_roman(source_text, scheme=scheme, reversible=reversible)
    return from_roman(source_text, scheme=scheme)


def _continues_grapheme(char: str, prev_char: str) -> bool:
    if char in (_ZWNJ, _ZWJ) or unicodedata.category(char).startswith("M"):
        return True
    if prev_char == _ODIA_VIRAMA and (
        "\u0b15" <= char <= "\u0b39" or char in "\u0b5c\u0b5d\u0b5f\u0b71"
    ):
        return True
    if prev_char == _ZWJ and unicodedata.category(char).startswith("S"):
        return True
    return prev_char == "\r" and char == "\n"


def count_visible_characters(text: str) -> int:
    """Count user-perceived characters, treating Odia conjuncts and emoji pairs as one."""
    total = 0
    prev_char = ""
    regional_run = 0

    for char in text:
        if "\U0001f1e6" <= char <= "\U0001f1ff":
            if regional_run % 2 == 0:
                total += 1
            regional_run += 1
        else:
            regional_run = 0
            if not prev_char or not _continues_grapheme(char, prev_char):
                total += 1
        prev_char = char

    return total


def format_text_counts(text: str, chars_label: str, words_label: str) -> str:
    char_count = count_visible_characters(text)
    word_count = len(text.split()) if text.strip() else 0
    return f"{char_count} {chars_label} • {word_count} {words_label}"
