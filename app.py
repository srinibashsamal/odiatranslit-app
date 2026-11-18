"""Streamlit front-end for Odia ↔ Roman transliteration.

Run locally:
    py -m pip install -r requirements.txt
    py -m streamlit run app.py
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

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
    live_copy_script,
    make_timestamp,
    package_version,
)

AUTHOR_URL = "https://github.com/srinibashsamal"

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
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
    """Initialise session-state defaults exactly once per browser session.

    ``reversible_pref`` stores the user's choice separately, because Streamlit
    drops the ``reversible`` widget state whenever the toggle is not drawn
    (Hunterian or Roman → Odia).
    """
    defaults: dict[str, object] = {
        "lang": "en",
        "direction": O2R,
        "scheme": "ISO15919",
        "source": "",
        "reversible_pref": False,
        "example_pick": None,
        "swap_error": None,
        "scheme_hint": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_examples(direction: str, scheme: str) -> dict[str, str]:
    """Return the example dictionary appropriate for the current direction.

    For Odia → Roman we always show the same Odia phrases.
    For Roman → Odia we show the scheme-specific Roman spellings.
    """
    if direction == O2R:
        return ODIA_EXAMPLES
    return ROMAN_EXAMPLES.get(scheme, {})


# ---------------------------------------------------------------------------
# Callbacks (run before the next script re-execution)
# ---------------------------------------------------------------------------


def load_example() -> None:
    """Copy the selected example into the input box and clear the picker."""
    pick = st.session_state.get("example_pick")
    if pick is None:
        return

    examples = get_examples(
        st.session_state.direction,
        st.session_state.scheme,
    )
    if pick in examples:
        st.session_state.source = examples[pick]
        st.session_state.scheme_hint = False

    # Reset so the same example can be chosen again later.
    st.session_state.example_pick = None


def clear_input() -> None:
    """Empty the input text area."""
    st.session_state.source = ""
    st.session_state.scheme_hint = False


def on_scheme_change() -> None:
    """Warn when the scheme changes while Roman input is present, because the
    existing Roman spelling belongs to the previous scheme."""
    st.session_state.scheme_hint = bool(
        st.session_state.direction == R2O and st.session_state.source.strip()
    )


def on_source_edit() -> None:
    """Dismiss the scheme hint as soon as the user starts editing the input."""
    st.session_state.scheme_hint = False


def on_direction_change() -> None:
    """A direction change makes any scheme hint irrelevant."""
    st.session_state.scheme_hint = False


def save_reversible() -> None:
    """Remember the toggle value so it survives the toggle being hidden."""
    st.session_state.reversible_pref = st.session_state.reversible


def swap_direction() -> None:
    """Move the current output into the input box and flip the direction.

    The output is recomputed from the *current* input rather than read from
    the output box, because live typing is debounced: a click on Swap can
    arrive before the rerun that would refresh the output box, and the stale
    output would then overwrite what the user just typed.

    Refuses to swap if the output would not fit in the input box, and turns
    reversible mode off, because the reverse mapping is done by the library.
    """
    ss = st.session_state
    reversible = effective_reversible(
        ss.direction, ss.scheme, ss.get("reversible", ss.reversible_pref)
    )
    try:
        output = convert(ss.source, ss.direction, ss.scheme, reversible)
    except Exception as exc:  # noqa: BLE001 - shown to the user, not raised
        ss.swap_error = ("failed", error_message(exc))
        return

    if not has_content(output):
        return
    if len(output) > MAX_CHARACTERS:
        ss.swap_error = ("too_long", len(output))
        return

    st.session_state.source = output
    st.session_state.direction = R2O if st.session_state.direction == O2R else O2R
    st.session_state.reversible_pref = False
    st.session_state.pop("reversible", None)
    st.session_state.scheme_hint = False


# ---------------------------------------------------------------------------
# UI building blocks
# ---------------------------------------------------------------------------


def render_sidebar(t: dict[str, str]) -> None:
    """Draw the collapsible sidebar (language selector, scheme info, links)."""
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
    """Draw the language selector at the top of the main page.

    It lives in the main page (not the sidebar) because the sidebar is
    collapsed by default on phones and the switch must stay discoverable.
    """
    st.radio(
        t["language"],
        LANGS,
        format_func=lambda code: LANG_LABELS[code],
        key="lang",
        horizontal=True,
        label_visibility="collapsed",
    )


def render_controls(t: dict[str, str]) -> tuple[str, str, bool]:
    """Render direction, scheme, example picker and reversible toggle.

    Args:
        t (dict[str, str]): UI strings for the currently selected language.

    Returns:
        tuple[str, str, bool]: direction, scheme, reversible
    """
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

    # Visual reminder of the currently selected scheme.
    st.markdown(
        f'<div class="scheme-info">'
        f"<b>{SCHEME_LABELS[scheme]}</b><br>{t[f'desc_{scheme}']}"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.scheme_hint:
        st.info(t["scheme_hint"], icon=":material/info:")

    # Odia script left in the box after switching to Roman → Odia.
    if direction == R2O and contains_odia(st.session_state.source):
        st.info(t["odia_in_roman_hint"], icon=":material/info:")

    # Reversible conversion is only meaningful for Odia → Roman
    # and only for schemes that support it.
    reversible = False
    if direction == O2R and scheme in REVERSIBLE_SCHEMES:
        # Restore the saved choice if Streamlit dropped the widget state
        # while the toggle was hidden.
        if "reversible" not in st.session_state:
            st.session_state.reversible = st.session_state.reversible_pref
        reversible = st.toggle(
            t["reversible"],
            key="reversible",
            on_change=save_reversible,
        )
    elif direction == O2R:
        # Show a disabled toggle so the user understands the limitation.
        st.toggle(
            t["reversible"],
            value=False,
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
    """Draw the side-by-side input / output text areas and their toolbars."""
    col_in, col_out = st.columns(2, gap="large")

    # ----- Input -----------------------------------------------------------
    with col_in:
        st.subheader(t["input"])
        source: str = st.text_area(
            t["input_aria"],
            key="source",
            placeholder=PLACEHOLDERS[direction],
            height=PANEL_HEIGHT,
            max_chars=MAX_CHARACTERS,
            label_visibility="collapsed",
            on_change=on_source_edit,
        )
        if len(source) >= MAX_CHARACTERS:
            st.warning(t["limit_reached"].format(limit=MAX_CHARACTERS))

        # Horizontal containers keep the toolbar on one line on phones
        # (st.columns would stack every item) and wrap only when needed.
        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/backspace: {t['btn_clear']}",
                help=t["clear"],
                disabled=not has_content(source),
                on_click=clear_input,
                key="btn_clear",
            )
            st.caption(count_label(source, t["chars"], t["words"]))

    # ----- Conversion (kept outside the columns so errors surface cleanly) -
    error: str | None = None
    try:
        output = convert(source, direction, scheme, reversible)
    except Exception as exc:  # noqa: BLE001 - surface library errors to the user
        output = ""
        error = error_message(exc)

    # Session state is the single source of truth for the output widget
    # (no ``value=`` argument), and the swap callback reads it from here.
    st.session_state["output_box"] = output

    # ----- Output ----------------------------------------------------------
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

        # Not ``disabled``: Firefox blocks text selection in disabled text
        # areas. The injected script makes this box read-only instead.
        st.text_area(
            t["output_aria"],
            key="output_box",
            height=PANEL_HEIGHT,
            label_visibility="collapsed",
        )

        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/swap_horiz: {t['btn_swap']}",
                help=t["swap"],
                disabled=not has_content(output),
                on_click=swap_direction,
                key="btn_swap",
            )
            st.download_button(
                f":material/download: {t['btn_dl']}",
                data=build_download_text(source, output, direction, scheme, reversible),
                file_name=f"transliteration_{make_timestamp(compact=True)}.txt",
                mime="text/plain",
                help=t["dl"],
                disabled=not has_content(output),
                on_click="ignore",
                key="btn_dl",
            )
            st.caption(count_label(output, t["chars"], t["words"]))


def render_extra_info(t: dict[str, str]) -> None:
    """Render the scheme comparison and the notes expander."""
    st.divider()
    st.subheader(t["cmp_title"])

    cols = st.columns(3)
    for col, name in zip(cols, ["ISO15919", "ITRANS", "Hunterian"], strict=True):
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
    """Render the four help / documentation tabs."""
    tab_how, tab_guide, tab_python, tab_about = st.tabs(
        [t["tab_how"], t["tab_guide"], t["tab_python"], t["tab_about"]]
    )

    with tab_how:
        st.markdown(t["how"])

    with tab_guide:
        for name in SCHEMES:
            st.markdown(f"### {SCHEME_LABELS[name]}\n{t[f'desc_{name}']}")

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


def inject_live_script(t: dict[str, str]) -> None:
    """Inject the JavaScript for live typing, floating copy buttons and the
    read-only output box.

    The script is placed inside a zero-height container so it does not affect
    layout.  We prefer the modern ``st.iframe`` helper when it exists;
    otherwise we fall back to ``components.html``.
    """
    html = live_copy_script(t["copy"], t["copied"])
    with st.container(key="live_js"):
        if hasattr(st, "iframe"):
            st.iframe(html, height=1)
        else:
            components.html(html, height=1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Orchestrate the whole page."""
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
    inject_live_script(t)


if __name__ == "__main__":
    main()
