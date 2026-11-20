"""Debounced, IME-aware text input for Streamlit Components v2."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import streamlit as st

_HTML = """
<div class="live-input">
  <textarea spellcheck="false"></textarea>
  <div class="toolbar">
    <button type="button" class="copy-btn"></button>
  </div>
</div>
"""

_CSS = """
.live-input { display: flex; flex-direction: column; gap: 6px; }
textarea {
  display: block; box-sizing: border-box; width: 100%;
  padding: 12px; resize: vertical; border-radius: 8px;
  border: 1px solid var(--st-border-color, #888);
  color: var(--st-text-color); background: var(--st-background-color);
  font: inherit; font-size: 1.05rem; line-height: 1.7;
}
textarea:focus-visible { outline: 2px solid var(--st-primary-color); outline-offset: 1px; }
.toolbar { display: flex; justify-content: flex-end; }
.copy-btn {
  font: inherit; font-size: 0.85rem; cursor: pointer;
  padding: 4px 12px; border-radius: 6px;
  border: 1px solid var(--st-border-color, #888);
  color: var(--st-text-color); background: transparent;
}
.copy-btn:hover:not(:disabled) { border-color: var(--st-primary-color); }
.copy-btn:focus-visible { outline: 2px solid var(--st-primary-color); outline-offset: 1px; }
.copy-btn:disabled { opacity: 0.5; cursor: default; }
"""

_JS = """
const DEBOUNCE_MS = 400;

// Trim to `limit` Unicode code points (not UTF-16 units), matching Python's len().
function clampCodePoints(text, limit) {
  const points = Array.from(text);
  return points.length > limit ? points.slice(0, limit).join('') : text;
}

async function copyText(text, input) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    // Fallback for browsers or contexts that block the Clipboard API.
    const start = input.selectionStart, end = input.selectionEnd;
    input.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    input.setSelectionRange(start, end);
    return ok;
  }
}

export default function({ parentElement, data, setStateValue }) {
  const input = parentElement.querySelector('textarea');
  const copyBtn = parentElement.querySelector('.copy-btn');
  if (!input || !copyBtn) return;

  const incoming = String(data.value ?? '');
  const revision = String(Number(data.revision ?? 0));
  const limit = Math.max(1, Number(data.limit) || 50000);
  const height = Math.max(80, Number(data.height) || 200);

  input.placeholder = String(data.placeholder ?? '');
  input.setAttribute('aria-label', String(data.label ?? 'Input'));
  input.style.height = height + 'px';
  input.style.minHeight = height + 'px';
  copyBtn.setAttribute('aria-label', String(data.copyLabel ?? 'Copy'));

  // Per-element state survives reruns because the DOM node is reused.
  const s = input._live || (input._live = {
    timer: null, composing: false, pending: false, committed: null,
  });
  // Always use the newest setter from the latest render.
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

  const refreshCopy = () => { copyBtn.disabled = input.value.trim() === ''; };

  // A Python-side change (Clear, Swap, Example) has priority over typing.
  // Unrelated reruns keep whatever the user is typing.
  if (input.dataset.revision === undefined) {
    input.value = incoming;
    s.committed = incoming;
  } else if (input.dataset.revision !== revision) {
    if (s.timer) clearTimeout(s.timer);
    s.timer = null;
    s.composing = false;
    input.value = incoming;
    // Keep the component state in step so a later edit is not mistaken
    // for "no change".
    if (s.committed !== incoming) {
      s.committed = incoming;
      s.send('value', incoming);
    }
    setPending(false);
  }
  input.dataset.revision = revision;
  refreshCopy();

  s.copyIdle = String(data.copyLabel ?? 'Copy');
  if (!s.copyFlash) copyBtn.textContent = s.copyIdle;

  const onInput = (event) => {
    refreshCopy();
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
  const onCopy = async () => {
    const ok = await copyText(input.value, input);
    if (!ok) return;
    copyBtn.textContent = String(data.copiedLabel ?? 'Copied!');
    if (s.copyFlash) clearTimeout(s.copyFlash);
    s.copyFlash = setTimeout(() => {
      s.copyFlash = null;
      copyBtn.textContent = s.copyIdle;
    }, 1500);
  };

  input.addEventListener('input', onInput);
  input.addEventListener('compositionstart', onCompositionStart);
  input.addEventListener('compositionend', onCompositionEnd);
  input.addEventListener('blur', onBlur);
  copyBtn.addEventListener('click', onCopy);

  // Only listeners are removed here. A pending debounce timer is left
  // running on purpose so a rerun in the middle of typing cannot drop it.
  return () => {
    input.removeEventListener('input', onInput);
    input.removeEventListener('compositionstart', onCompositionStart);
    input.removeEventListener('compositionend', onCompositionEnd);
    input.removeEventListener('blur', onBlur);
    copyBtn.removeEventListener('click', onCopy);
  };
}
"""

_INPUT = st.components.v2.component(
    "odia_transliterate_live_input", html=_HTML, css=_CSS, js=_JS
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
    copy_label: str,
    copied_label: str,
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
            "copyLabel": copy_label,
            "copiedLabel": copied_label,
        },
        default={"value": value, "pending": False},
        on_value_change=on_change,
        on_pending_change=_noop,
    )
