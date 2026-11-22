from __future__ import annotations

import random
import streamlit as st

from app_constants import (
    FAVICON,
    CSS,
    # DEMO_TEXTS,
    JUKTAKHYARA_WORDS,
    DIRECTIONS,
    GITHUB_URL,
    ISSUES_URL,
    LANGUAGE_LABELS,
    MAX_CHARACTERS,
    ODIA_EXAMPLES,
    ODIA_TO_ROMAN,
    PACKAGE_NAME,
    PANEL_HEIGHT,
    PLACEHOLDERS,
    PYPI_URL,
    REVERSIBLE_SCHEMES,
    ROMAN_EXAMPLES,
    ROMAN_TO_ODIA,
    SCHEME_LABELS,
    SUPPORTED_LANGUAGES,
    TRANSLITERATION_SCHEMES,
    UI_TEXT,
)
from helpers import (
    build_download_file,
    format_text_counts,
    installed_package_version,
    transliterate_text,
)
import live_input as li

st.set_page_config(
    page_title="Odia Transliterate",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)
st.markdown(CSS, unsafe_allow_html=True)


def initialize_session_state() -> None:
    defaults: dict[str, object] = {
        "lang": "en",
        "direction": ODIA_TO_ROMAN,
        "scheme": "ISO15919",
        "source": "",
        "source_revision": 0,
        "reversible_pref": False,
        "example_pick": None,
        "swap_error": None,
        "scheme_hint": False,
    }
    for key, default_value in defaults.items():
        st.session_state.setdefault(key, default_value)


def load_example() -> None:
    chosen_eg = st.session_state.get("example_pick")

    if chosen_eg is None:
        return
    examples = (
        ODIA_EXAMPLES
        if st.session_state.direction == ODIA_TO_ROMAN
        else ROMAN_EXAMPLES.get(st.session_state.scheme, {})
    )
    if chosen_eg in examples:
        st.session_state.source = examples[chosen_eg]
        st.session_state.source_revision += 1
    st.session_state.scheme_hint = False
    st.session_state.example_pick = None


def clear_input() -> None:
    st.session_state.source = ""
    st.session_state.source_revision += 1
    st.session_state.scheme_hint = False


def on_scheme_change() -> None:
    st.session_state.scheme_hint = bool(
        st.session_state.direction == ROMAN_TO_ODIA and st.session_state.source.strip()
    )


LIVE_IP = "live_source"


def on_source_edit() -> None:
    input_state = st.session_state.get(LIVE_IP)
    if input_state is None:
        return

    entered_text = input_state.get("value", "")
    if not isinstance(entered_text, str):
        return

    cleaned_text = entered_text.encode("utf-16", "surrogatepass").decode(
        "utf-16", "replace"  # Normalize lone UTF-16 surrogates from browser input.
    )
    was_truncated = len(cleaned_text) > MAX_CHARACTERS
    if was_truncated:
        cleaned_text = cleaned_text[:MAX_CHARACTERS]

    if cleaned_text != st.session_state.source:
        st.session_state.source = cleaned_text
        st.session_state.scheme_hint = False
    if was_truncated:
        st.session_state.source_revision += 1


def swap_direction() -> None:
    input_state = st.session_state.get(LIVE_IP) or {}
    if input_state.get("pending", False):
        return

    saved_reversible = bool(
        st.session_state.get(
            "reversible", st.session_state.get("reversible_pref", False)
        )
    )
    use_reversible = (
        saved_reversible
        and st.session_state.direction == ODIA_TO_ROMAN
        and st.session_state.scheme in REVERSIBLE_SCHEMES
    )

    try:
        converted_text = transliterate_text(
            st.session_state.source,
            st.session_state.direction,
            st.session_state.scheme,
            use_reversible,
        )
    except Exception as exc:  # noqa: BLE001
        st.session_state.swap_error = (
            "failed",
            str(exc).strip() or type(exc).__name__,
        )
        return

    if not converted_text.strip():
        return
    if len(converted_text) > MAX_CHARACTERS:
        st.session_state.swap_error = ("too_long", len(converted_text))
        return

    st.session_state.source = converted_text
    st.session_state.source_revision += 1
    st.session_state.direction = (
        ROMAN_TO_ODIA if st.session_state.direction == ODIA_TO_ROMAN else ODIA_TO_ROMAN
    )
    st.session_state.reversible_pref = False
    st.session_state.pop("reversible", None)
    st.session_state.scheme_hint = False


def render_sidebar(labels: dict[str, str]) -> None:
    with st.sidebar:
        st.markdown(f"### {FAVICON} {labels['title']}")

        st.divider()
        st.subheader(labels["side_schemes"])
        st.markdown(labels["side_schemes_table"])

        st.subheader(labels["side_features"])
        st.markdown(labels["side_features_list"])

        st.subheader(labels["side_useful"])
        st.markdown(labels["side_useful_list"])

        st.divider()
        st.markdown(f"**{labels['sidebar_tip']}**")
        st.caption(labels["tip_text"])

        st.divider()
        st.caption(
            labels["powered"].format(pkg=PACKAGE_NAME, ver=installed_package_version())
        )
        st.link_button(
            labels["pypi"],
            PYPI_URL,
            icon=":material/inventory_2:",
            width="stretch",
        )
        st.link_button(
            labels["github"],
            GITHUB_URL,
            icon=":material/code:",
            width="stretch",
        )
        st.link_button(
            labels["issues"],
            ISSUES_URL,
            icon=":material/bug_report:",
            width="stretch",
        )


def render_controls(labels: dict[str, str]) -> tuple[str, str, bool]:
    dir_col, scheme_col, example_col = st.columns(3)

    with dir_col:
        direction = st.radio(
            labels["direction"],
            DIRECTIONS,
            format_func=lambda code: labels[code],
            key="direction",
            horizontal=True,
            on_change=lambda: st.session_state.update(scheme_hint=False),
        )

    with scheme_col:
        scheme = st.selectbox(
            labels["scheme"],
            TRANSLITERATION_SCHEMES,
            format_func=lambda code: SCHEME_LABELS[code],
            key="scheme",
            on_change=on_scheme_change,
        )

    examples = (
        ODIA_EXAMPLES if direction == ODIA_TO_ROMAN else ROMAN_EXAMPLES.get(scheme, {})
    )
    with example_col:
        st.selectbox(
            labels["example"],
            list(examples),
            format_func=lambda key: labels[f"ex_{key}"],
            index=None,
            placeholder=labels["example_ph"],
            key="example_pick",
            on_change=load_example,
        )

    st.markdown(
        f'<div class="scheme-info">'
        f"<b>{SCHEME_LABELS[scheme]}</b><br>{labels[f'desc_{scheme}']}"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.scheme_hint:
        st.info(labels["scheme_hint"], icon=":material/info:")

    if direction == ROMAN_TO_ODIA and any(
        "\u0b00" <= ch <= "\u0b7f" for ch in st.session_state.source
    ):
        st.info(labels["odia_in_roman_hint"], icon=":material/info:")

    reversible = False
    if direction == ODIA_TO_ROMAN and scheme in REVERSIBLE_SCHEMES:
        # Keep the previous toggle choice when switching away from a reversible scheme.
        if "reversible" not in st.session_state:
            st.session_state.reversible = st.session_state.reversible_pref
        reversible = st.toggle(
            labels["reversible"],
            key="reversible",
            on_change=lambda: st.session_state.update(
                reversible_pref=st.session_state.reversible
            ),
        )
    elif direction == ODIA_TO_ROMAN:
        st.toggle(
            labels["reversible"],
            value=bool(st.session_state.reversible_pref),
            disabled=True,
            key="reversible_off",
        )
    return direction, scheme, reversible


def render_panels(
    labels: dict[str, str],
    direction: str,
    scheme: str,
    reversible: bool,
) -> None:
    input_col, output_col = st.columns(2, gap="large")

    with input_col:
        st.subheader(labels["input"])
        input_state = li.live_input(
            value=st.session_state.source,
            revision=st.session_state.source_revision,
            placeholder=PLACEHOLDERS[direction],
            label=labels["input_area"],
            max_chars=MAX_CHARACTERS,
            height=PANEL_HEIGHT,
            on_change=on_source_edit,
            key=LIVE_IP,
        )

    pending = bool((input_state or {}).get("pending", False))
    source_text = st.session_state.source

    conversion_error: str | None = None
    try:
        converted_text = transliterate_text(source_text, direction, scheme, reversible)
    except Exception as exc:  # noqa: BLE001
        converted_text = ""
        conversion_error = str(exc).strip() or type(exc).__name__

    actions_disabled = pending or not bool(converted_text.strip())

    with output_col:
        st.subheader(labels["output"])
        if conversion_error:
            st.error(labels["conv_error"].format(err=conversion_error))

        # Show swap errors once.
        swap_error = st.session_state.swap_error
        st.session_state.swap_error = None
        if swap_error:
            err_kind, err_detail = swap_error
            if err_kind == "too_long":
                st.warning(
                    labels["swap_too_long"].format(n=err_detail, limit=MAX_CHARACTERS)
                )
            else:
                st.warning(labels["swap_failed"].format(err=err_detail))

        st.code(
            converted_text or " ",
            language=None,
            wrap_lines=True,
            height=PANEL_HEIGHT,
        )

    # Draw toolbars after both panels so they align on the same row.
    with input_col:
        if len(source_text) >= MAX_CHARACTERS:
            st.warning(labels["limit_reached"].format(limit=MAX_CHARACTERS))
        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/backspace: {labels['btn_clear']}",
                help=labels["clear"],
                disabled=not bool(source_text.strip()),
                on_click=clear_input,
                key="btn_clear",
            )
            li.copy_button(
                text=source_text,
                label=labels["btn_copy"],
                copied_label=labels["copied"],
                tooltip=labels["copy"],
                disabled=pending,
                key="btn_copy",
            )
            caption = (
                labels["updating"]
                if pending
                else format_text_counts(source_text, labels["chars"], labels["words"])
            )
            st.caption(caption)

    with output_col:
        download_filename, download_body = build_download_file(
            source_text, converted_text, direction, scheme, reversible
        )
        with st.container(horizontal=True, vertical_alignment="center"):
            st.button(
                f":material/swap_horiz: {labels['btn_swap']}",
                help=labels["swap"],
                disabled=actions_disabled,
                on_click=swap_direction,
                key="btn_swap",
            )
            st.download_button(
                f":material/download: {labels['btn_dl']}",
                data=download_body,
                file_name=download_filename,
                mime="text/plain",
                help=labels["dl"],
                disabled=actions_disabled,
                on_click="ignore",
                key="btn_dl",
            )
            caption = (
                labels["updating"]
                if pending
                else format_text_counts(
                    converted_text, labels["chars"], labels["words"]
                )
            )
            st.caption(caption)


def render_scheme_comparison(labels: dict[str, str]) -> None:
    st.divider()
    st.subheader(labels["cmp_title"])

    columns = st.columns(len(TRANSLITERATION_SCHEMES))
    # random_text = random.choice(DEMO_TEXTS)
    random_text = random.choice(JUKTAKHYARA_WORDS)

    for col, scheme_name in zip(columns, TRANSLITERATION_SCHEMES, strict=True):
        with col:
            st.markdown(f"**{SCHEME_LABELS[scheme_name]}**")
            try:
                preview = transliterate_text(random_text, ODIA_TO_ROMAN, scheme_name)
            except Exception:  # noqa: BLE001
                preview = None
            if preview is None:
                st.caption(labels["demo_error"])
            else:
                st.code(preview, language=None)
            st.caption(labels[f"cmp_{scheme_name}"])
    with st.expander(labels["notes_title"]):
        st.markdown(labels["notes"])


def render_help_tabs(labels: dict[str, str]) -> None:
    tab_how, tab_python, tab_about = st.tabs(
        [labels["tab_how"], labels["tab_python"], labels["tab_about"]]
    )

    with tab_how:
        st.markdown(labels["how"])

    with tab_python:
        st.code(f"pip install {PACKAGE_NAME}", language="bash")
        st.code(
            f"from {PACKAGE_NAME} import to_roman, from_roman\n\n"
            'print(to_roman("ଓଡ଼ିଆ", scheme="ISO15919"))\n'
            'print(from_roman("namaskAra", scheme="ITRANS"))',
            language="python",
        )

    with tab_about:
        powered = labels["powered"].format(
            pkg=f"`{PACKAGE_NAME}`", ver=installed_package_version()
        )
        st.markdown(
            f"{powered}\n\nPyPI: {PYPI_URL}\n\nGitHub: {GITHUB_URL}\n\n{labels['about']}"
        )


def main() -> None:
    initialize_session_state()
    labels = UI_TEXT[st.session_state.lang]

    render_sidebar(labels)
    st.radio(
        labels["language"],
        SUPPORTED_LANGUAGES,
        format_func=lambda code: LANGUAGE_LABELS[code],
        key="lang",
        horizontal=True,
        label_visibility="collapsed",
    )

    st.title(f"{FAVICON} {labels['title']}")
    st.caption(labels["tagline"])

    direction, scheme, reversible = render_controls(labels)
    render_panels(labels, direction, scheme, reversible)

    render_scheme_comparison(labels)
    st.divider()
    render_help_tabs(labels)

    package_link = f'<a href="{PYPI_URL}" target="_blank">{PACKAGE_NAME}</a>'
    dev_link = (
        f'<a href="https://github.com/srinibashsamal" target="_blank">Srinibash</a>'
    )

    footer = labels["footer"].format(pypi_link=package_link, author_link=dev_link)
    st.markdown(f'<div class="app-footer">{footer}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
