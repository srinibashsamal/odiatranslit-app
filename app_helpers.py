"""Helper functions for the Odia Transliterate Streamlit app.

Contains pure utilities for timestamps, download payloads, package-version
lookup, the core transliteration wrapper, character/word counting, and the
JavaScript injector used for live typing and in-field copy buttons.
"""

from __future__ import annotations

import json
import unicodedata
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version

from odiatranslit import from_roman, to_roman

from app_constants import (
    APP_TZ_NAME,
    APP_UTC_OFFSET_MINUTES,
    DIRECTION_FILE_LABELS,
    GITHUB_URL,
    JS_TEMPLATE,
    LIVE_DEBOUNCE_MS,
    O2R,
    PACKAGE_NAME,
    REVERSIBLE_SCHEMES,
    SCHEME_LABELS,
)

# Fixed-offset zone
_TZ = timezone(timedelta(minutes=APP_UTC_OFFSET_MINUTES), APP_TZ_NAME)

_ZWNJ = "\u200c"
_ZWJ = "\u200d"
_ODIA_VIRAMA = "\u0b4d"


def _now() -> datetime:
    """Return the current time in the app's configured time zone."""
    return datetime.now(_TZ)


def make_timestamp(
    *,
    date_only: bool = False,
    compact: bool = False,
    include_ms: bool = False,
) -> str:
    """Return a filesystem-safe timestamp string in the app's time zone.

    Args:
        date_only (bool, optional): If True, return only the date portion.
            Defaults to False.
        compact (bool, optional): If True, omit hyphens/colons (useful for
            filenames). Defaults to False.
        include_ms (bool, optional): If True (and not ``date_only``), append
            the milliseconds. Defaults to False.

    Returns:
        str: The formatted timestamp.

    Examples:
        >>> make_timestamp()  # doctest: +SKIP
        '2026-11-17_22-38-01'
        >>> make_timestamp(compact=True)  # doctest: +SKIP
        '20261117_223801'
        >>> make_timestamp(date_only=True, compact=True)  # doctest: +SKIP
        '20261117'
    """
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
    """Return the current time as ``YYYYMMDDTHHMMSS <TZ>``, e.g.
    ``20261118T094512 IST``.

    The zone name is included so the recorded time is unambiguous.
    """
    return _now().strftime("%Y%m%dT%H%M%S %Z")


def build_download_text(
    source: str,
    output: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> str:
    """Assemble the plain-text payload for the download button."""
    mode = "Reversible" if reversible else "Standard"
    return (
        f"Input:\n{source}\n\n"
        f"Output:\n{output}\n\n\n\n"
        f"Conversion: {DIRECTION_FILE_LABELS[direction]}\n"
        f"Scheme: {SCHEME_LABELS[scheme]}\n"
        f"Mode: {mode}\n"
        f"Conversion happened at: {make_conversion_stamp()}\n"
        f"Source: {GITHUB_URL}\n"
    )


@lru_cache(maxsize=1)
def package_version() -> str:
    """Return the installed version of ``odiatranslit``, or ``"unknown"``.

    Cached because the installed version cannot change while the app runs.
    """
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "unknown"


def effective_reversible(direction: str, scheme: str, reversible: bool) -> bool:
    """Return True only when reversible mode is meaningful for this setup
    (Odia → Roman with a scheme that supports it)."""
    return bool(reversible) and direction == O2R and scheme in REVERSIBLE_SCHEMES


def has_content(text: str) -> bool:
    """Return True if ``text`` has any non-whitespace content."""
    return bool(text and text.strip())


def contains_odia(text: str) -> bool:
    """Return True if ``text`` contains any character from the Odia block."""
    return any("\u0b00" <= ch <= "\u0b7f" for ch in text)


@lru_cache(maxsize=8)
def convert(
    text: str,
    direction: str,
    scheme: str,
    reversible: bool = False,
) -> str:
    """Transliterate ``text`` according to the chosen direction and scheme.

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
        empty or whitespace-only. Results are cached (small LRU) because the
        page reruns on every live keystroke.
    """
    if not has_content(text):
        return ""

    if direction == O2R:
        return to_roman(text, scheme=scheme, reversible=reversible)

    # Roman → Odia never uses the reversible flag.
    return from_roman(text, scheme=scheme)


@lru_cache(maxsize=16)
def demo_conversion(text: str, scheme: str) -> str | None:
    """Return the Odia → Roman conversion of a fixed demo text, or ``None``
    if the library fails. Cached because the inputs never change.
    """
    try:
        return convert(text, O2R, scheme)
    except Exception:  # noqa: BLE001 - a broken preview must not crash the page
        return None


def error_message(exc: BaseException) -> str:
    """Return a non-empty, readable message for ``exc``.

    ``str(exc)`` is empty for exceptions raised without arguments
    (e.g. ``ValueError()``), so fall back to the exception class name.
    """
    return str(exc).strip() or type(exc).__name__


def _is_odia_consonant(ch: str) -> bool:
    """Return True for Odia consonant letters (including ଡ଼ ଢ଼ ୟ ୱ)."""
    return "\u0b15" <= ch <= "\u0b39" or ch in "\u0b5c\u0b5d\u0b5f\u0b71"


def _joins_previous(ch: str, prev: str) -> bool:
    """Return True if ``ch`` belongs to the same visible character as the
    character before it."""
    if ch in (_ZWNJ, _ZWJ):
        return True
    if unicodedata.category(ch).startswith("M"):  # vowel signs, nukta, virama…
        return True
    # Consonant after a virama forms a conjunct, e.g. କ୍ଷ, ତ୍ର. Only Odia
    # consonants qualify, so କ୍a or କ୍अ are not merged.
    if prev == _ODIA_VIRAMA and _is_odia_consonant(ch):
        return True
    # Symbol/emoji after a ZWJ continues an emoji sequence (👨‍👩‍👧).
    if prev == _ZWJ and unicodedata.category(ch).startswith("S"):
        return True
    return prev == "\r" and ch == "\n"


def count_characters(text: str) -> int:
    """Count user-perceived characters rather than code points.

    ``len()`` counts code points, so ଓଡ଼ିଆ would count as 5. Here combining
    marks, zero-width joiners and virama conjuncts are folded into the
    character they belong to, so ଓଡ଼ିଆ counts as 3 and କ୍ଷ as 1.
    """
    count = 0
    prev = ""
    for ch in text:
        if not prev or not _joins_previous(ch, prev):
            count += 1
        prev = ch
    return count


def count_label(text: str, chars_label: str, words_label: str) -> str:
    """Return a human-readable ``"N characters • M words"`` caption.

    Empty or whitespace-only text is reported as zero words.
    """
    n_chars = count_characters(text)
    n_words = len(text.split()) if text.strip() else 0
    return f"{n_chars} {chars_label} • {n_words} {words_label}"


def live_copy_script(copy_tip: str, copied_tip: str) -> str:
    """Return the fully-substituted JavaScript that powers live typing,
    the floating copy buttons, and the read-only output box.

    The returned HTML fragment is injected via ``st.iframe`` (or
    ``components.html`` on older Streamlit versions).
    """
    tips_json = json.dumps({"copy": copy_tip, "copied": copied_tip})
    script = JS_TEMPLATE.replace("__TIPS__", tips_json).replace(
        "__DEBOUNCE__", str(LIVE_DEBOUNCE_MS)
    )
    # Strip so the string starts with "<script>" (some iframe helpers sniff
    # the first character to decide between a URL and an HTML string).
    return script.strip()
