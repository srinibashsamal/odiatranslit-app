"""Debounced text input and clipboard copy button for Streamlit Components v2."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import streamlit as st

_INPUT_HTML = '<textarea spellcheck="false"></textarea>'

_INPUT_CSS = """
textarea {
  display: block; box-sizing: border-box; width: 100%;
  padding: 12px; resize: vertical; border-radius: 8px;
  border: 1px solid var(--st-border-color, #888);
  color: var(--st-text-color); background: var(--st-background-color);
  font: inherit; font-size: 1.05rem; line-height: 1.7;
}
textarea:focus-visible { outline: 2px solid var(--st-primary-color); outline-offset: 1px; }
"""

_INPUT_JS = """
const DEBOUNCE_MS = 400;

// Clamp by Unicode code points instead of UTF-16 units to match Python's len().
function clampCodePoints(text, limit) {
  const codePoints = Array.from(text);
  return codePoints.length > limit ? codePoints.slice(0, limit).join('') : text;
}

export default function({ parentElement, data, setStateValue }) {
  const textarea = parentElement.querySelector('textarea');
  if (!textarea) return;

  const incoming = String(data.value ?? '');
  const revision = String(Number(data.revision ?? 0));
  const limit = Math.max(1, Number(data.limit) || 50000);
  const height = Math.max(80, Number(data.height) || 200);

  textarea.placeholder = String(data.placeholder ?? '');
  textarea.setAttribute('aria-label', String(data.label ?? 'Input'));
  textarea.style.height = height + 'px';
  textarea.style.minHeight = height + 'px';

  // Store state on the DOM node so it survives Streamlit reruns.
  const editorState = textarea._live || (textarea._live = {
    timer: null, composing: false, pending: false, committed: null,
  });
  editorState.send = setStateValue;

  const setPending = (flag) => {
    if (editorState.pending === flag) return;
    editorState.pending = flag;
    editorState.send('pending', flag);
  };

  const commit = () => {
    if (editorState.timer) clearTimeout(editorState.timer);
    editorState.timer = null;
    // Wait until IME composition finishes before sending text.
    if (editorState.composing) return;
    const value = clampCodePoints(textarea.value, limit);
    if (value !== textarea.value) textarea.value = value;
    if (value !== editorState.committed) {
      editorState.committed = value;
      editorState.send('value', value);
    }
    setPending(false);
  };

  const schedule = () => {
    if (editorState.timer) clearTimeout(editorState.timer);
    editorState.timer = setTimeout(commit, DEBOUNCE_MS);
  };

  // Python-side updates (Clear, Swap, Example) override local typing.
  if (textarea.dataset.revision === undefined) {
    textarea.value = incoming;
    editorState.committed = incoming;
  } else if (textarea.dataset.revision !== revision) {
    if (editorState.timer) clearTimeout(editorState.timer);
    editorState.timer = null;
    editorState.composing = false;
    textarea.value = incoming;
    if (editorState.committed !== incoming) {
      editorState.committed = incoming;
      editorState.send('value', incoming);
    }
    setPending(false);
  }
  textarea.dataset.revision = revision;

  const onInput = (event) => {
    if (editorState.composing || event.isComposing) {
      setPending(true);
      return;
    }
    const clamped = clampCodePoints(textarea.value, limit);
    if (clamped !== textarea.value) textarea.value = clamped;
    setPending(true);
    schedule();
  };
  const onCompositionStart = () => {
    editorState.composing = true;
    if (editorState.timer) clearTimeout(editorState.timer);
    editorState.timer = null;
    setPending(true);
  };
  const onCompositionEnd = () => {
    editorState.composing = false;
    setPending(true);
    schedule();
  };
  const onBlur = () => {
    editorState.composing = false;
    commit();
  };

  textarea.addEventListener('input', onInput);
  textarea.addEventListener('compositionstart', onCompositionStart);
  textarea.addEventListener('compositionend', onCompositionEnd);
  textarea.addEventListener('blur', onBlur);

  // Remove listeners only. Keep any active timer so mid-typing reruns do not drop it.
  return () => {
    textarea.removeEventListener('input', onInput);
    textarea.removeEventListener('compositionstart', onCompositionStart);
    textarea.removeEventListener('compositionend', onCompositionEnd);
    textarea.removeEventListener('blur', onBlur);
  };
}
"""

_INPUT_COMPONENT = st.components.v2.component(
    "odia_transliterate_live_input",
    html=_INPUT_HTML,
    css=_INPUT_CSS,
    js=_INPUT_JS,
)


def live_input(
    *,
    value: str,
    revision: int,
    placeholder: str,
    label: str,
    max_chars: int,
    height: int,
    on_change: Callable[[], None],
    key: str = "live_source",
) -> Any:
    return _INPUT_COMPONENT(
        key=key,
        data={
            "value": value,
            "revision": revision,
            "placeholder": placeholder,
            "label": label,
            "limit": max_chars,
            "height": height,
        },
        default={"value": value, "pending": False},
        on_value_change=on_change,
        on_pending_change=lambda: None,
    )


_ICON_COPY = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18q-.82 0-1.41-.59T7 16V4'
    "q0-.82.59-1.41T9 2h9q.82 0 1.41.59T20 4v12q0 .82-.59 1.41T18 18zm0-2h9V4H9zm-4 6"
    'q-.82 0-1.41-.59T3 20V6h2v14h11v2zm4-6V4z"/></svg>'
)
_ICON_DONE = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="m9.55 18-5.7-5.7 1.43-1.43 4.27 4.28 9.18-9.18 1.42 1.43z"/></svg>'
)

_COPY_HTML = '<button type="button" class="copy-btn"><span class="icon"></span><span class="label"></span></button>'

# Match st.button height, border radius, and border width.
_COPY_CSS = """
.copy-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;
  box-sizing: border-box; min-height: 2.5rem; margin: 0;
  padding: 0.25rem 0.75rem; border-radius: 0.5rem;
  border: 1px solid var(--st-border-color, rgba(250, 250, 250, 0.2));
  background: var(--st-secondary-background-color, transparent);
  color: var(--st-text-color); font: inherit; font-size: 1rem;
  line-height: 1.6; white-space: nowrap; cursor: pointer; user-select: none;
}
.copy-btn:hover:not(:disabled) {
  border-color: var(--st-primary-color); color: var(--st-primary-color);
}
.copy-btn:focus-visible { outline: 2px solid var(--st-primary-color); outline-offset: 1px; }
.copy-btn:disabled { opacity: 0.4; cursor: not-allowed; }
@media (max-width: 640px) { .copy-btn { min-height: 2.75rem; } }
.icon { display: inline-flex; width: 1.1rem; height: 1.1rem; }
.icon svg { width: 100%; height: 100%; fill: currentColor; }
"""

_COPY_JS = f"""
const ICON_COPY = {_ICON_COPY!r};
const ICON_DONE = {_ICON_DONE!r};

async function writeClipboard(text) {{
  try {{
    await navigator.clipboard.writeText(text);
    return true;
  }} catch (err) {{
    // Fall back to execCommand when the browser blocks the Clipboard API.
    const fallbackArea = document.createElement('textarea');
    fallbackArea.value = text;
    fallbackArea.setAttribute('readonly', '');
    fallbackArea.style.position = 'absolute';
    fallbackArea.style.left = '-9999px';
    document.body.appendChild(fallbackArea);
    fallbackArea.select();
    let copied = false;
    try {{ copied = document.execCommand('copy'); }} catch (e) {{ copied = false; }}
    fallbackArea.remove();
    return copied;
  }}
}}

export default function({{ parentElement, data }}) {{
  const button = parentElement.querySelector('.copy-btn');
  if (!button) return;
  const iconSpan = button.querySelector('.icon');
  const labelSpan = button.querySelector('.label');

  const text = String(data.text ?? '');
  const idleLabel = String(data.label ?? 'Copy');
  const copiedLabel = String(data.copiedLabel ?? 'Copied!');

  const copyState = button._copy || (button._copy = {{ flash: null }});
  button.disabled = Boolean(data.disabled) || text.trim() === '';
  button.title = String(data.help ?? idleLabel);
  button.setAttribute('aria-label', button.title);
  if (!copyState.flash) {{
    iconSpan.innerHTML = ICON_COPY;
    labelSpan.textContent = idleLabel;
  }}

  const onClick = async () => {{
    if (!(await writeClipboard(text))) return;
    iconSpan.innerHTML = ICON_DONE;
    labelSpan.textContent = copiedLabel;
    if (copyState.flash) clearTimeout(copyState.flash);
    copyState.flash = setTimeout(() => {{
      copyState.flash = null;
      iconSpan.innerHTML = ICON_COPY;
      labelSpan.textContent = idleLabel;
    }}, 1500);
  }};
  button.addEventListener('click', onClick);
  return () => button.removeEventListener('click', onClick);
}}
"""

_COPY_COMPONENT = st.components.v2.component(
    "odia_transliterate_copy_button",
    html=_COPY_HTML,
    css=_COPY_CSS,
    js=_COPY_JS,
)


def copy_button(
    *,
    text: str,
    label: str,
    copied_label: str,
    tooltip: str,
    disabled: bool = False,
    key: str = "btn_copy",
) -> Any:
    return _COPY_COMPONENT(
        key=key,
        data={
            "text": text,
            "label": label,
            "copiedLabel": copied_label,
            "help": tooltip,
            "disabled": disabled,
        },
        width="content",
    )
