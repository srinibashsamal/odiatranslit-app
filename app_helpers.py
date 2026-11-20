"""Helper functions for the Odia Transliterate Streamlit app.

Contains pure utilities for timestamps, download payloads, package-version
lookup, the core transliteration wrapper, character/word counting, and the
small text utilities used by the front end.
"""

from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version

from odiatranslit import from_roman, to_roman

from app_constants import (
    APP_TZ_NAME,
    APP_UTC_OFFSET_MINUTES,
    DIRECTION_FILE_LABELS,
    TOOL_URL,
    GITHUB_URL,
    O2R,
    PACKAGE_NAME,
    REVERSIBLE_SCHEMES,
    SCHEME_LABELS,
)

_TZ = timezone(timedelta(minutes=APP_UTC_OFFSET_MINUTES), APP_TZ_NAME)

_ZWNJ = "\u200c"
_ZWJ = "\u200d"
_ODIA_VIRAMA = "\u0b4d"


def _now() -> datetime:
    """Current time in the app time zone."""
    return datetime.now(_TZ)


def make_timestamp(
    *,
    date_only: bool = False,
    compact: bool = False,
    include_ms: bool = False,
) -> str:
    """Filesystem-safe timestamp in the app time zone."""
    now = _now()
    if date_only:
        fmt = "%Y%m%d" if compact else "%Y-%m-%d"
        return now.strftime(fmt)

    fmt = "%Y%m%d_%H%M%S" if compact else "%Y-%m-%d_%H-%M-%S"
    stamp = now.strftime(fmt)
    if include_ms:
        stamp = f"{stamp}_{now.strftime('%f')[:3]}"
    return stamp


def make_conversion_stamp() -> str:
    """Current time as ``YYYY-MM-DD HH:MM:SS <TZ>``."""
    return _now().strftime("%Y-%m-%d %H:%M:%S %Z")


def _section(title: str) -> str:
    """Return a plain-text heading underlined to its own length."""
    return f"{title}\n{'-' * len(title)}\n"


def build_download_text(
    source: str,
    output: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> str:
    """Assemble the plain-text payload for the download button."""
    title = "Odia Transliterate - Conversion Record"
    mode = "Reversible" if reversible else "Standard"
    details = [
        ("Direction", DIRECTION_FILE_LABELS[direction]),
        ("Scheme", SCHEME_LABELS[scheme]),
        ("Mode", mode),
        ("Converted", make_conversion_stamp()),
        ("Library", f"{PACKAGE_NAME} v{package_version()}"),
        ("Tool", TOOL_URL),
        ("Source", GITHUB_URL),
    ]
    width = max(len(label) for label, _ in details) + 2
    detail_lines = "\n".join(f"{label:<{width}}: {value}" for label, value in details)
    return (
        f"{title}\n{'=' * len(title)}\n\n"
        f"{_section('INPUT')}{source}\n\n"
        f"{_section('OUTPUT')}{output}\n\n\n"
        f"{_section('DETAILS')}{detail_lines}\n"
    )


@lru_cache(maxsize=1)
def package_version() -> str:
    """Installed version of ``odiatranslit``, or ``"unknown"``."""
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unknown"


def effective_reversible(direction: str, scheme: str, reversible: bool) -> bool:
    """``True`` only when reversible mode applies (O2R + supported scheme)."""
    return bool(reversible) and direction == O2R and scheme in REVERSIBLE_SCHEMES


def has_content(text: str) -> bool:
    """``True`` if ``text`` has non-whitespace content."""
    return bool(text and text.strip())


def contains_odia(text: str) -> bool:
    """``True`` if ``text`` contains any Odia-block character."""
    return any("\u0b00" <= ch <= "\u0b7f" for ch in text)


@lru_cache(maxsize=16)
def convert(
    text: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> str:
    """Transliterate ``text`` for the given direction and scheme.

    Args:
        text (str): Source text (Odia or Roman).
        direction (str): Either ``O2R`` (Odia → Roman) or ``R2O``
            (Roman → Odia).
        scheme (str): One of ``"ISO15919"``, ``"Hunterian"``, ``"ITRANS"``.
        reversible (bool, optional): When True and the scheme supports it,
            produce a lossless mapping that can be round-tripped exactly.
            Ignored for Roman → Odia. Defaults to False.

    Returns:
        str: The transliterated string, or an empty string when ``text`` is
        empty or whitespace-only.
    """
    if not has_content(text):
        return ""

    if direction == O2R:
        return to_roman(text, scheme=scheme, reversible=reversible)

    return from_roman(text, scheme=scheme)


@lru_cache(maxsize=16)
def demo_conversion(text: str, scheme: str) -> str | None:
    """Odia → Roman demo conversion, or None on failure."""
    try:
        return to_roman(text, scheme=scheme)
    except Exception:  # noqa: BLE001
        return None


def error_message(exc: BaseException) -> str:
    """Readable message for an exception."""
    return str(exc).strip() or type(exc).__name__


def _is_odia_consonant(ch: str) -> bool:
    """``True`` for Odia consonant letters (including ଡ଼ ଢ଼ ୟ ୱ)."""
    return "\u0b15" <= ch <= "\u0b39" or ch in "\u0b5c\u0b5d\u0b5f\u0b71"


def _is_regional_indicator(ch: str) -> bool:
    """``True`` for a Unicode regional indicator."""
    return "\U0001f1e6" <= ch <= "\U0001f1ff"


def _joins_previous(ch: str, prev: str) -> bool:
    """``True`` if ``ch`` belongs to the same visible character as prev."""
    if ch in (_ZWNJ, _ZWJ):
        return True
    if unicodedata.category(ch).startswith("M"):
        return True
    if prev == _ODIA_VIRAMA and _is_odia_consonant(ch):
        return True
    if prev == _ZWJ and unicodedata.category(ch).startswith("S"):
        return True
    if prev == "\r" and ch == "\n":
        return True
    return False


def count_characters(text: str) -> int:
    """Count user-perceived characters (not code points)."""
    count = 0
    prev = ""
    consecutive_indicators = 0
    for ch in text:
        if _is_regional_indicator(ch):
            if consecutive_indicators % 2 == 0:
                count += 1
            consecutive_indicators += 1
        else:
            consecutive_indicators = 0
            if not prev or not _joins_previous(ch, prev):
                count += 1
        prev = ch
    return count


def count_label(text: str, chars_label: str, words_label: str) -> str:
    """Return ``"N characters • M words"`` caption."""
    n_chars = count_characters(text)
    n_words = len(text.split()) if text.strip() else 0
    return f"{n_chars} {chars_label} • {n_words} {words_label}"
