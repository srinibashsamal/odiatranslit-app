# Odia Transliterate

A small web app that converts **Odia script to Roman** and **Roman back to Odia**,
built with [Streamlit](https://streamlit.io) on top of the
[`odiatranslit`](https://pypi.org/project/odiatranslit/) library.

Supported schemes: **ISO 15919**, **Hunterian** and **ITRANS**.

<!-- Add a screenshot: save it as docs/screenshot.png and uncomment the next line -->
<!-- ![Screenshot](docs/screenshot.png) -->

## Features

- Odia → Roman and Roman → Odia, with a one-click **Swap** that turns the output into the new input
- Three schemes, each with a short description of when to use it
- **Reversible mode** (ISO 15919 and ITRANS, Odia → Roman): English words are wrapped in escapes
  such as `:{Puri:}` (ISO) or `_{Puri_}` (ITRANS), so the text converts back exactly
- Live conversion while you type, using a custom Streamlit component. Input is sent after a short
  pause, and never in the middle of a character being composed by an Odia input method (IME)
- Swap and Download stay disabled until your latest typing has been converted, so they never use
  an older input or output
- Copy buttons on both the input and the output, and download of input + output as a `.txt` file
- Example texts, a side-by-side scheme comparison, and an English / ଓଡ଼ିଆ interface
- Works on phones: labelled toolbar buttons, a collapsible sidebar and a narrow-screen layout

## Run locally

Requires Python 3.10 or newer and Streamlit 1.66 or newer.

```bash
git clone https://github.com/srinibashsamal/odiatranslit-app.git
cd odiatranslit-app

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Deploy

The easiest option is [Streamlit Community Cloud](https://streamlit.io/cloud): push this repo
to GitHub, create a new app, and select `app.py` as the entry point. Dependencies are read from
`requirements.txt`.

## Project layout

| File               | Purpose                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| `app.py`           | Streamlit UI: layout, widgets, session state, callbacks                 |
| `live_input.py`    | Live input component (debounce, IME handling, copy button, input limit) |
| `app_helpers.py`   | Conversion wrapper, character counting, download text, timestamps       |
| `app_constants.py` | UI strings (English and Odia), examples, schemes and page CSS           |
| `requirements.txt` | Python dependencies                                                     |
| `CHANGES.md`       | Notes on the fixes and improvements made during review                  |

## Good to know

- **Hunterian is lossy.** Several Odia letters map to the same Roman letter, so Roman → Odia
  cannot restore the original spelling. Use ISO 15919 or ITRANS with reversible mode when you
  need an exact round trip.
- **Input limit:** 50,000 code points. Longer pasted text is cut off in the browser, and the app
  shows a notice when the limit is reached.
- **Character counts** treat conjuncts, combining marks and emoji sequences (including flags) as one
  visible character, while the limit itself is measured in code points, so the two numbers can
  differ for Odia text.
- **Malformed characters** in pasted text (lone UTF-16 surrogates) are replaced with `�` so they
  cannot break the output or the download.
- Odia text typed into the box in Roman → Odia mode is passed through unchanged. The app shows a
  hint if it notices this.

## Credits

Transliteration is done by [`odiatranslit`](https://pypi.org/project/odiatranslit/) by
Srinibash Samal. This repository only provides the web interface.
