# Odia Transliterate

A small web app that converts **Odia script to Roman** and **Roman back to Odia**,
built with [Streamlit](https://streamlit.io) on top of the
[`odiatranslit`](https://pypi.org/project/odiatranslit/) library.

Supported schemes: **ISO 15919**, **ITRANS** and **Hunterian**.

<!-- Add a screenshot: save it as docs/screenshot.png and uncomment the next line -->
<!-- ![Screenshot](docs/screenshot.png) -->

## Features

- Odia â†’ Roman and Roman â†’ Odia, with a one-click **Swap** that turns the output into the new input
- Three schemes, each with a short description of when to use it
- **Reversible mode** (ISO 15919 and ITRANS, Odia â†’ Roman): English words are wrapped in escapes
  such as `:{Puri:}` (ISO) or `_{Puri_}` (ITRANS), so the text converts back exactly
- Live conversion while you type (debounced, and safe with Odia input methods that compose characters)
- Copy button inside each text box, and download of input + output as a `.txt` file
- Example texts, a side-by-side scheme comparison, and an English / à¬“à¬¡à¬¼à¬¿à¬† interface
- Works on phones: labelled toolbar buttons, a collapsible sidebar and a narrow-screen layout

## Run locally

Requires Python 3.10 or newer and Streamlit 1.56 or newer.

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

| File               | Purpose                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| `app.py`           | Streamlit UI: layout, widgets, session state, callbacks                  |
| `app_helpers.py`   | Conversion wrapper, character counting, download text, timestamps        |
| `app_constants.py` | UI strings (English and Odia), examples, CSS and the injected JavaScript |
| `requirements.txt` | Python dependencies                                                      |
| `CHANGES.md`       | Notes on the fixes and improvements made during review                   |

## Good to know

- **Hunterian is lossy.** Several Odia letters map to the same Roman letter, so Roman â†’ Odia
  cannot restore the original spelling. Use ISO 15919 or ITRANS with reversible mode when you
  need an exact round trip.
- **Input limit:** 50,000 code points. Longer pasted text is cut off by the browser, and the app
  shows a notice when the limit is reached.
- **Character counts** treat conjuncts and combining marks as one visible character, while the
  limit itself is measured in code points, so the two numbers can differ for Odia text.
- Odia text typed into the box in Roman â†’ Odia mode is passed through unchanged. The app shows a
  hint if it notices this.

## Credits

Transliteration is done by [`odiatranslit`](https://pypi.org/project/odiatranslit/) by
Srinibash Samal. This repository only provides the web interface.
