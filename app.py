"""Streamlit front-end for Odia ↔ Roman transliteration.

Run locally:
    py -m pip install -r requirements.txt
    py -m streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from app_constants import (
    APP_ICON,
    CUSTOM_CSS,
    DEMO_TEXT,
    DIRECTIONS,
    GITHUB_URL,
    ISSUES_URL,
    LANG_LABELS,
    LANGS,
    MAX_CHARACTERS,
    O2R,
    ODIA_EXAMPLES,
    PACKAGE_NAME,
    PANEL_HEIGHT,
    PLACEHOLDERS,
    PYPI_URL,
    R2O,
    REVERSIBLE_SCHEMES,
    ROMAN_EXAMPLES,
    SCHEME_LABELS,
    SCHEMES,
    TEXT,
)
from app_helpers import (
    build_download_text,
    contains_odia,
    convert,
    count_label,
    demo_conversion,
    effective_reversible,
    error_message,
    has_content,
    make_timestamp,
    package_version,
)
from live_input import live_input

AUTHOR_URL = "https://github.com/srinibashsamal"
LIVE_INPUT_KEY = "live_source"

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Odia Transliterate",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="auto",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session-state helpers
# ---------------------------------------------------------------------------
def init_state() -> None:
    """Set session-state defaults once per session."""
    defaults: dict[str, object] = {
        "lang": "en",
        "direction": O2R,
        "scheme": "ISO15919",
        "source": "",
        "source_revision": 0,
        "reversible_pref": False,
        "example_pick": None,
        "swap_error": None,
        "scheme_hint": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_examples(direction: str, scheme: str) -> dict[str, str]:
    """Return examples for the current direction and scheme."""
    if direction == O2R:
        return ODIA_EXAMPLES
    return ROMAN_EXAMPLES.get(scheme, {})


def _saved_reversible() -> bool:
    """Return the last reversible preference."""
    try:
        return bool(st.session_state["reversible"])
    except KeyError:
        return bool(st.session_state.get("reversible_pref", False))


def _input_pending() -> bool:
    """True while typed text is not yet committed."""
    component = st.session_state.get(LIVE_INPUT_KEY) or {}
    return bool(component.get("pending", False))


def _clean_text(text: str) -> str:
    """Replace lone UTF-16 surrogates with U+FFFD."""
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "replace")


# ---------------------------------------------------------------------------
# Callbacks (run before the next script re-execution)
# ---------------------------------------------------------------------------
def load_example() -> None:
    """Load the selected example into the input box."""
    pick = st.session_state.get("example_pick")
    if pick is None:
        return
    examples = get_examples(
        st.session_state.direction,
        st.session_state.scheme,
    )
    if pick in examples:
        st.session_state.source = examples[pick]
        st.session_state.source_revision += 1
    st.session_state.scheme_hint = False
    st.session_state.example_pick = None


def clear_input() -> None:
    """Clear the input box."""
    st.session_state.source = ""
    st.session_state.source_revision += 1
    st.session_state.scheme_hint = False


def on_scheme_change() -> None:
    """Warn if scheme changes while Roman input is present."""
    st.session_state.scheme_hint = bool(
        st.session_state.direction == R2O and st.session_state.source.strip()
    )


def on_source_edit() -> None:
    """Commit debounced component value to session state."""
    component = st.session_state.get(LIVE_INPUT_KEY)
    if component is None:
        return
    value = component.get("value", "")
    if not isinstance(value, str):
        return
    value = _clean_text(value)
    truncated = len(value) > MAX_CHARACTERS
    if truncated:
        value = value[:MAX_CHARACTERS]
    if value != st.session_state.source:
        st.session_state.source = value
        st.session_state.scheme_hint = False
    if truncated:
        st.session_state.source_revision += 1


def on_direction_change() -> None:
    """Clear scheme hint on direction change."""
    st.session_state.scheme_hint = False


def save_reversible() -> None:
    """Persist reversible toggle value."""
    st.session_state.reversible_pref = st.session_state.reversible


def swap_direction() -> None:
    """Swap direction by moving current output into the input box."""
    ss = st.session_state
    if _input_pending():
        return
    reversible = effective_reversible(ss.direction, ss.scheme, _saved_reversible())
    try:
        output = convert(ss.source, ss.direction, ss.scheme, reversible)
    except Exception as exc:  # noqa: BLE001
        ss.swap_error = ("failed", error_message(exc))
        return

    if not has_content(output):
        return
    if len(output) > MAX_CHARACTERS:
        ss.swap_error = ("too_long", len(output))
        return

    ss.source = output
    ss.source_revision += 1
    ss.direction = R2O if ss.direction == O2R else O2R
    ss.reversible_pref = False
    ss.pop("reversible", None)
    ss.scheme_hint = False


# ---------------------------------------------------------------------------
# UI building blocks
# ---------------------------------------------------------------------------
def render_sidebar(t: dict[str, str]) -> None:
    """Render the sidebar."""
    with st.sidebar:
        st.markdown(f"### {APP_ICON} {t['title']}")

        st.divider()
        st.subheader(t["side_schemes"])
        st.markdown(t["side_schemes_table"])

        st.subheader(t["side_features"])
        st.markdown(t["side_features_list"])

        st.subheader(t["side_useful"])
        st.markdown(t["side_useful_list"])

        st.divider()
        st.markdown(f"**{t['sidebar_tip']}**")
        st.caption(t["tip_text"])

        st.divider()
        st.caption(t["powered"].format(pkg=PACKAGE_NAME, ver=package_version()))
        st.link_button(
            t["pypi"],
            PYPI_URL,
            icon=":material/inventory_2:",
            width="stretch",
        )
        st.link_button(
            t["github"],
            GITHUB_URL,
            icon=":material/code:",
            width="stretch",
        )
        st.link_button(
            t["issues"],
            ISSUES_URL,
            icon=":material/bug_report:",
            width="stretch",
        )


def render_language_switch(t: dict[str, str]) -> None:
    """Render the language selector."""
    st.radio(
        t["language"],
        LANGS,
        format_func=lambda code: LANG_LABELS[code],
        key="lang",
        horizontal=True,
        label_visibility="collapsed",
    )


def render_controls(t: dict[str, str]) -> tuple[str, str, bool]:
    """Render direction, scheme, examples and reversible toggle."""
    col_dir, col_scheme, col_example = st.columns(3)

    with col_dir:
        direction = st.radio(
            t["direction"],
            DIRECTIONS,
            format_func=lambda code: t[code],
            key="direction",
            horizontal=True,
            on_change=on_direction_change,
        )

    with col_scheme:
        scheme = st.selectbox(
            t["scheme"],
            SCHEMES,
            format_func=lambda code: SCHEME_LABELS[code],
            key="scheme",
            on_change=on_scheme_change,
        )

    examples = get_examples(direction, scheme)
    with col_example:
        st.selectbox(
            t["example"],
            list(examples),
            format_func=lambda key: t[f"ex_{key}"],
            index=None,
            placeholder=t["example_ph"],
            key="example_pick",
            on_change=load_example,
        )

    st.markdown(
        f'<div class="scheme-info">'
        f"<b>{SCHEME_LABELS[scheme]}</b><br>{t[f'desc_{scheme}']}"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.scheme_hint:
        st.info(t["scheme_hint"], icon=":material/info:")

    if direction == R2O and contains_odia(st.session_state.source):
        st.info(t["odia_in_roman_hint"], icon=":material/info:")

    reversible = False
    if direction == O2R and scheme in REVERSIBLE_SCHEMES:
        if "reversible" not in st.session_state:
            st.session_state.reversible = st.session_state.reversible_pref
        reversible = st.toggle(
            t["reversible"],
            key="reversible",
            on_change=save_reversible,
        )
    elif direction == O2R:
        st.toggle(
            t["reversible"],
            value=bool(st.session_state.reversible_pref),
            disabled=True,
            key="reversible_off",
        )
    return direction, scheme, reversible


def render_panels(
    t: dict[str, str],
    direction: str,
    scheme: str,
    reversible: bool,
) -> None:
    """Render input/output panels and toolbars."""
    col_in, col_out = st.columns(2, gap="large")

    with col_in:
        st.subheader(t["input"])
        result = live_input(
            value=st.session_state.source,
            revision=st.session_state.source_revision,
            placeholder=PLACEHOLDERS[direction],
            label=t["input_aria"],
            max_chars=MAX_CHARACTERS,
            height=PANEL_HEIGHT,
            copy_label=t["copy"],
            copied_label=t["copied"],
            on_change=on_source_edit,
            key=LIVE_INPUT_KEY,
        )
        pending = bool((result or {}).get("pending", False))
        source: str = st.session_state.source
        if len(source) >= MAX_CHARACTERS:
            st.warning(t["limit_reached"].format(limit=MAX_CHARACTERS))
        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/backspace: {t['btn_clear']}",
                help=t["clear"],
                disabled=not has_content(source),
                on_click=clear_input,
                key="btn_clear",
            )
            st.caption(count_label(source, t["chars"], t["words"]))

    error: str | None = None
    try:
        output = convert(source, direction, scheme, reversible)
    except Exception as exc:  # noqa: BLE001
        output = ""
        error = error_message(exc)

    actions_disabled = pending or not has_content(output)

    with col_out:
        st.subheader(t["output"])
        if error:
            st.error(t["conv_error"].format(err=error))

        swap_error = st.session_state.swap_error
        st.session_state.swap_error = None  # show the warning only once
        if swap_error:
            kind, detail = swap_error
            if kind == "too_long":
                st.warning(t["swap_too_long"].format(n=detail, limit=MAX_CHARACTERS))
            else:
                st.warning(t["swap_failed"].format(err=detail))

        st.code(output or " ", language=None, wrap_lines=True, height=PANEL_HEIGHT)

        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/swap_horiz: {t['btn_swap']}",
                help=t["swap"],
                disabled=actions_disabled,
                on_click=swap_direction,
                key="btn_swap",
            )
            st.download_button(
                f":material/download: {t['btn_dl']}",
                data=build_download_text(source, output, direction, scheme, reversible),
                file_name=f"transliteration_{make_timestamp(compact=True)}.txt",
                mime="text/plain",
                help=t["dl"],
                disabled=actions_disabled,
                on_click="ignore",
                key="btn_dl",
            )
            if pending:
                st.caption(t["updating"])
            else:
                st.caption(count_label(output, t["chars"], t["words"]))


def render_extra_info(t: dict[str, str]) -> None:
    """Render scheme comparison and notes."""
    st.divider()
    st.subheader(t["cmp_title"])

    cols = st.columns(len(SCHEMES))
    for col, name in zip(cols, SCHEMES, strict=True):
        with col:
            st.markdown(f"**{SCHEME_LABELS[name]}**")
            preview = demo_conversion(DEMO_TEXT, name)
            if preview is None:
                st.caption(t["demo_error"])
            else:
                st.code(preview, language=None)
            st.caption(t[f"cmp_{name}"])
    with st.expander(t["notes_title"]):
        st.markdown(t["notes"])


def render_tabs(t: dict[str, str]) -> None:
    """Render help and documentation tabs."""
    tab_how, tab_python, tab_about = st.tabs(
        [t["tab_how"], t["tab_python"], t["tab_about"]]
    )

    with tab_how:
        st.markdown(t["how"])

    with tab_python:
        st.code(f"pip install {PACKAGE_NAME}", language="bash")
        st.code(
            f"from {PACKAGE_NAME} import to_roman, from_roman\n\n"
            'print(to_roman("ଓଡ଼ିଆ", scheme="ISO15919"))\n'
            'print(from_roman("namaskAra", scheme="ITRANS"))',
            language="python",
        )

    with tab_about:
        powered = t["powered"].format(pkg=f"`{PACKAGE_NAME}`", ver=package_version())
        st.markdown(
            f"{powered}\n\nPyPI: {PYPI_URL}\n\nGitHub: {GITHUB_URL}\n\n{t['about']}"
        )


def render_footer(t: dict[str, str]) -> None:
    """Render the bilingual, theme-aware footer."""
    pypi_link = f'<a href="{PYPI_URL}" target="_blank">{PACKAGE_NAME}</a>'
    author_link = f'<a href="{AUTHOR_URL}" target="_blank">Srinibash</a>'
    footer = t["footer"].format(pypi_link=pypi_link, author_link=author_link)
    st.markdown(f'<div class="app-footer">{footer}</div>', unsafe_allow_html=True)


def main() -> None:
    """Build and render the full page."""
    init_state()
    t = TEXT[st.session_state.lang]

    render_sidebar(t)
    render_language_switch(t)

    st.title(f"{APP_ICON} {t['title']}")
    st.caption(t["tagline"])

    direction, scheme, reversible = render_controls(t)
    render_panels(t, direction, scheme, reversible)

    render_extra_info(t)
    st.divider()
    render_tabs(t)

    render_footer(t)


if __name__ == "__main__":
    main()
