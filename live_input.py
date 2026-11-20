"""Debounced, IME-aware text input for Streamlit Components v2."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import streamlit as st

# ---------------------------------------------------------------------------
# Live text input
# ---------------------------------------------------------------------------
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

// Trim to `limit` Unicode code points (not UTF-16 units), matching Python's len().
function clampCodePoints(text, limit) {
  const points = Array.from(text);
  return points.length > limit ? points.slice(0, limit).join('') : text;
}

export default function({ parentElement, data, setStateValue }) {
  const input = parentElement.querySelector('textarea');
  if (!input) return;

  const incoming = String(data.value ?? '');
  const revision = String(Number(data.revision ?? 0));
  const limit = Math.max(1, Number(data.limit) || 50000);
  const height = Math.max(80, Number(data.height) || 200);

  input.placeholder = String(data.placeholder ?? '');
  input.setAttribute('aria-label', String(data.label ?? 'Input'));
  input.style.height = height + 'px';
  input.style.minHeight = height + 'px';

  // Per-element state survives reruns because the DOM node is reused.
  const s = input._live || (input._live = {
    timer: null, composing: false, pending: false, committed: null,
  });
  s.send = setStateValue;

  const setPending = (flag) => {
    if (s.pending === flag) return;
    s.pending = flag;
    s.send('pending', flag);
  };

  const commit = () => {
    if (s.timer) clearTimeout(s.timer);
    s.timer = null;
    if (s.composing) return;  // never send half-composed IME text
    const value = clampCodePoints(input.value, limit);
    if (value !== input.value) input.value = value;
    if (value !== s.committed) {
      s.committed = value;
      s.send('value', value);
    }
    setPending(false);
  };

  const schedule = () => {
    if (s.timer) clearTimeout(s.timer);
    s.timer = setTimeout(commit, DEBOUNCE_MS);
  };

  // A Python-side change (Clear, Swap, Example) has priority over typing.
  if (input.dataset.revision === undefined) {
    input.value = incoming;
    s.committed = incoming;
  } else if (input.dataset.revision !== revision) {
    if (s.timer) clearTimeout(s.timer);
    s.timer = null;
    s.composing = false;
    input.value = incoming;
    if (s.committed !== incoming) {
      s.committed = incoming;
      s.send('value', incoming);
    }
    setPending(false);
  }
  input.dataset.revision = revision;

  const onInput = (event) => {
    if (s.composing || event.isComposing) {
      setPending(true);
      return;
    }
    const clamped = clampCodePoints(input.value, limit);
    if (clamped !== input.value) input.value = clamped;
    setPending(true);
    schedule();
  };
  const onCompositionStart = () => {
    s.composing = true;
    if (s.timer) clearTimeout(s.timer);
    s.timer = null;
    setPending(true);
  };
  const onCompositionEnd = () => {
    s.composing = false;
    setPending(true);
    schedule();
  };
  const onBlur = () => {
    s.composing = false;
    commit();
  };

  input.addEventListener('input', onInput);
  input.addEventListener('compositionstart', onCompositionStart);
  input.addEventListener('compositionend', onCompositionEnd);
  input.addEventListener('blur', onBlur);

  // Only listeners are removed; a pending debounce timer keeps running so a
  // rerun in the middle of typing cannot drop it.
  return () => {
    input.removeEventListener('input', onInput);
    input.removeEventListener('compositionstart', onCompositionStart);
    input.removeEventListener('compositionend', onCompositionEnd);
    input.removeEventListener('blur', onBlur);
  };
}
"""

_INPUT = st.components.v2.component(
    "odia_transliterate_live_input",
    html=_INPUT_HTML,
    css=_INPUT_CSS,
    js=_INPUT_JS,
)


def _noop() -> None:
    """No-op for pending changes."""


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
    """Mount the live input; returns ``value`` and ``pending``."""
    return _INPUT(
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
        on_pending_change=_noop,
    )


# ---------------------------------------------------------------------------
# Copy button (styled to match Streamlit's secondary buttons)
# ---------------------------------------------------------------------------
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

# Matches st.button: 2.5rem min-height, 0.5rem radius, 1px border.
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
    // Fallback for browsers or contexts that block the Clipboard API.
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'absolute';
    area.style.left = '-9999px';
    document.body.appendChild(area);
    area.select();
    let ok = false;
    try {{ ok = document.execCommand('copy'); }} catch (e) {{ ok = false; }}
    area.remove();
    return ok;
  }}
}}

export default function({{ parentElement, data }}) {{
  const btn = parentElement.querySelector('.copy-btn');
  if (!btn) return;
  const icon = btn.querySelector('.icon');
  const label = btn.querySelector('.label');

  const text = String(data.text ?? '');
  const idle = String(data.label ?? 'Copy');
  const done = String(data.copiedLabel ?? 'Copied!');

  const s = btn._copy || (btn._copy = {{ flash: null }});
  btn.disabled = Boolean(data.disabled) || text.trim() === '';
  btn.title = String(data.help ?? idle);
  btn.setAttribute('aria-label', btn.title);
  if (!s.flash) {{
    icon.innerHTML = ICON_COPY;
    label.textContent = idle;
  }}

  const onClick = async () => {{
    if (!(await writeClipboard(text))) return;
    icon.innerHTML = ICON_DONE;
    label.textContent = done;
    if (s.flash) clearTimeout(s.flash);
    s.flash = setTimeout(() => {{
      s.flash = null;
      icon.innerHTML = ICON_COPY;
      label.textContent = idle;
    }}, 1500);
  }};
  btn.addEventListener('click', onClick);
  return () => btn.removeEventListener('click', onClick);
}}
"""

_COPY = st.components.v2.component(
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
    help: str,
    disabled: bool = False,
    key: str = "btn_copy",
) -> Any:
    """Mount a copy-to-clipboard button sized like ``st.button``."""
    return _COPY(
        key=key,
        data={
            "text": text,
            "label": label,
            "copiedLabel": copied_label,
            "help": help,
            "disabled": disabled,
        },
        width="content",
    )
