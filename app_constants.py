"""Constants, UI text, and CSS for the Odia Transliterate Streamlit app.

This module centralises all configuration, bilingual UI strings (English and
Odia), example texts, and the page-level CSS.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_ICON: str = "🔤"
PACKAGE_NAME: str = "odiatranslit"
PYPI_URL: str = "https://pypi.org/project/odiatranslit/"
GITHUB_URL: str = "https://github.com/srinibashsamal/odiatranslit"
TOOL_URL: str = "https://odiatranslitor.streamlit.app/"
ISSUES_URL: str = f"{GITHUB_URL}/issues"

# Max input length in Unicode code points.
MAX_CHARACTERS: int = 50_000

# Fixed IST offset (no DST).
APP_UTC_OFFSET_MINUTES: int = 330
APP_TZ_NAME: str = "IST"

PANEL_HEIGHT: int = 220

PLACEHOLDERS: dict[str, str] = {
    "o2r": "ଏଠାରେ ଓଡ଼ିଆ ଟେକ୍ସଟ୍ ଲେଖନ୍ତୁ...\nType or paste Odia text here...",
    "r2o": ("Type or paste Roman text here...\ne.g. namaskAra  or  ōṛiā bhāṣā"),
}

DEMO_TEXT: str = "ଓଡ଼ିଆ ଭାଷା"

# ---------------------------------------------------------------------------
# Language and direction constants
# ---------------------------------------------------------------------------
LANGS: list[str] = ["en", "or"]
LANG_LABELS: dict[str, str] = {
    "en": "English",
    "or": "ଓଡ଼ିଆ",
}

O2R: str = "o2r"
R2O: str = "r2o"
DIRECTIONS: list[str] = [O2R, R2O]

DIRECTION_FILE_LABELS: dict[str, str] = {
    O2R: "Odia → Roman",
    R2O: "Roman → Odia",
}

SCHEMES: list[str] = ["ISO15919", "Hunterian", "ITRANS"]
REVERSIBLE_SCHEMES: set[str] = {"ISO15919", "ITRANS"}

SCHEME_LABELS: dict[str, str] = {
    "ISO15919": "ISO 15919",
    "Hunterian": "Hunterian",
    "ITRANS": "ITRANS",
}

# ---------------------------------------------------------------------------
# Example texts
# ---------------------------------------------------------------------------
ODIA_EXAMPLES: dict[str, str] = {
    "language": "ଓଡ଼ିଆ",
    "greeting": "ନମସ୍କାର",
    "jagannath": "ଜଗନ୍ନାଥ",
    "sentence": "ମୋ ଓଡ଼ିଶା ଅତି ସୁନ୍ଦର।",
}

ROMAN_EXAMPLES: dict[str, dict[str, str]] = {
    "ISO15919": {
        "language": "ōṛiā",
        "greeting": "namaskāra",
        "jagannath": "jagannātha",
        "sentence": "mō ōṛiśā ati sundara।",
    },
    "Hunterian": {
        "language": "oria",
        "greeting": "namaskara",
        "jagannath": "jagannatha",
        "sentence": "mo orisha ati sundara।",
    },
    "ITRANS": {
        "language": "o.DiA",
        "greeting": "namaskAra",
        "jagannath": "jagannAtha",
        "sentence": "mo o.DishA ati sundara।",
    },
}

# ---------------------------------------------------------------------------
# Bilingual UI strings
# ---------------------------------------------------------------------------
TEXT: dict[str, dict[str, str]] = {
    "en": {
        "title": "Odia Transliterate",
        "tagline": (
            "Convert Odia text to Roman script and Roman text "
            "back to Odia using ISO 15919, Hunterian or ITRANS."
        ),
        "language": "Language / ଭାଷା",
        "direction": "Conversion direction",
        O2R: "Odia → Roman",
        R2O: "Roman → Odia",
        "scheme": "Transliteration scheme",
        "reversible": "Enable reversible conversion",
        "example": "Try an example",
        "example_ph": "Select an example",
        "input": "Input",
        "output": "Output",
        "input_aria": "Enter or paste your text",
        "chars": "characters",
        "words": "words",
        "copy": "Copy to clipboard",
        "copied": "Copied!",
        "updating": "Updating…",
        "clear": "Clear input",
        "swap": "Use output as input and swap direction",
        "dl": "Download input and output as .txt",
        "tab_how": "How to use",
        "tab_guide": "Scheme guide",
        "tab_python": "Python usage",
        "tab_about": "About",
        "how": (
            "1. Choose a direction.\n"
            "2. Select a scheme.\n"
            "3. Type or paste text. The result updates automatically as you type.\n"
            "4. Use the copy buttons or download the result.\n"
            "5. Use the swap icon for reverse conversion.\n\n"
            "**Transliteration changes scripts; "
            "it does not translate meaning.**"
        ),
        "powered": "Powered by {pkg} v{ver}",
        "footer": (
            "Built with ❤️ using <b>Streamlit</b> + {pypi_link}<br>"
            "By {author_link} · MIT License"
        ),
        "conv_error": "Conversion failed: {err}",
        "demo_error": "Preview unavailable",
        "swap_too_long": (
            "The output is {n} code points long, which is more than the "
            "input limit of {limit}. Shorten the input before swapping."
        ),
        "swap_failed": "Could not swap: {err}",
        "btn_clear": "Clear",
        "btn_swap": "Swap",
        "btn_dl": "Download",
        "limit_reached": (
            "The input limit of {limit} code points has been reached. "
            "Anything beyond it has been cut off."
        ),
        "odia_in_roman_hint": (
            "The input contains Odia script, but the direction is Roman → "
            "Odia. Switch the direction to convert it to Roman."
        ),
        "scheme_hint": (
            "Scheme changed. Roman spellings differ between schemes, so "
            "re-check the input for the new scheme."
        ),
        "pypi": "PyPI",
        "github": "GitHub",
        "issues": "Report an issue",
        "sidebar_tip": "Tip",
        "tip_text": (
            "Results update automatically as you type. Use ISO 15919 or ITRANS "
            "with reversible mode for a lossless round trip."
        ),
        "about": (
            "Author: Srinibash Samal • MIT License\n\n"
            "Text is processed temporarily by the app and "
            "is not intentionally stored."
        ),
        "desc_ISO15919": (
            "Academic and linguistically precise transliteration using diacritics."
        ),
        "desc_Hunterian": (
            "Simpler Roman spelling suited to readable names, places and general text."
        ),
        "desc_ITRANS": (
            "Keyboard-friendly transliteration using ASCII-style sequences."
        ),
        "ex_language": "Odia language",
        "ex_greeting": "Greeting",
        "ex_jagannath": "Jagannath",
        "ex_sentence": "Sentence",
        "side_schemes": "Schemes",
        "side_schemes_table": (
            "| Scheme | Best for | Example |\n"
            "|--------|----------|---------|\n"
            "| **ISO 15919** | Academic writing, citations | ōṛiā bhāṣā |\n"
            "| **Hunterian** | Names, places, URLs, search | oria bhasha |\n"
            "| **ITRANS** | Typing Odia on English keyboard | o.DiA bhAShA |"
        ),
        "side_features": "Features",
        "side_features_list": (
            "- Bidirectional conversion\n"
            "- Lossless round-trip (ISO & ITRANS with reversible)\n"
            "- Mixed text safe (English, numbers, punctuation pass through)\n"
            "- Copy-friendly input & output"
        ),
        "side_useful": "Useful for",
        "side_useful_list": (
            "- Learners of Odia language\n"
            "- Researchers & linguists\n"
            "- Content creators & journalists\n"
            "- Name / place romanisation\n"
            "- Data cleaning & search indexing\n"
            "- Typing Odia without Odia keyboard"
        ),
        "cmp_title": "Scheme comparison (same Odia input)",
        "cmp_ISO15919": "Academic · Reversible",
        "cmp_Hunterian": "Names / Search · Lossy",
        "cmp_ITRANS": "Keyboard-friendly · Reversible",
        "notes_title": "📝 Notes & tips",
        "notes": (
            "**Reversible mode**  \n"
            "When enabled (ISO 15919 / ITRANS only), ambiguous characters "
            "are escaped so you can convert the Roman text back to the "
            "*exact* original Odia.  \n"
            "Example: English words inside Odia text are wrapped like "
            "`:{Puri:}` in ISO 15919 and `_{Puri_}` in ITRANS.\n\n"
            "**Hunterian limitations**  \n"
            "Several Odia letters map to the same Roman letter "
            "(e.g. ଣ, ଞ, ନ → `n`).  \n"
            "Decoding is best-effort and may not recover the original "
            "spelling.\n\n"
            "**Mixed text**  \n"
            "English words, numbers, and punctuation pass through "
            "unchanged.\n\n"
            "**Digits**  \n"
            "- ISO 15919 keeps Odia digits (୦–୯)\n"
            "- Hunterian converts them to ASCII\n"
            "- ITRANS converts them unless reversible=True\n\n"
            "**ITRANS shortcuts**  \n"
            "Accepts common alternatives such as `aa` for `A`, "
            "`ii` for `I`, etc."
        ),
    },
    "or": {
        "title": "ଓଡ଼ିଆ ଲିପ୍ୟନ୍ତର",
        "tagline": (
            "ISO 15919, Hunterian କିମ୍ବା ITRANS ବ୍ୟବହାର କରି ଓଡ଼ିଆ "
            "ଲେଖାକୁ ରୋମାନ୍‌ରେ ଏବଂ ରୋମାନ୍ ଲେଖାକୁ ଓଡ଼ିଆରେ ବଦଳାନ୍ତୁ।"
        ),
        "language": "Language / ଭାଷା",
        "direction": "ରୂପାନ୍ତର ଦିଗ",
        O2R: "ଓଡ଼ିଆ → ରୋମାନ୍",
        R2O: "ରୋମାନ୍ → ଓଡ଼ିଆ",
        "scheme": "ଲିପ୍ୟନ୍ତର ପଦ୍ଧତି",
        "reversible": "ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ରୂପାନ୍ତର ସକ୍ରିୟ କରନ୍ତୁ",
        "example": "ଏକ ଉଦାହରଣ ଦେଖନ୍ତୁ",
        "example_ph": "ଏକ ଉଦାହରଣ ବାଛନ୍ତୁ",
        "input": "ଇନପୁଟ୍",
        "output": "ଆଉଟପୁଟ୍",
        "input_aria": "ଆପଣଙ୍କ ଲେଖା ଟାଇପ୍ କିମ୍ବା ପେଷ୍ଟ କରନ୍ତୁ",
        "chars": "ଅକ୍ଷର",
        "words": "ଶବ୍ଦ",
        "copy": "କ୍ଲିପବୋର୍ଡକୁ କପି କରନ୍ତୁ",
        "copied": "କପି ହେଲା!",
        "updating": "ଅପଡେଟ୍ ହେଉଛି…",
        "clear": "ଇନପୁଟ୍ ଲିଭାନ୍ତୁ",
        "swap": "ଆଉଟପୁଟ୍‌କୁ ଇନପୁଟ୍ କରି ଦିଗ ବଦଳାନ୍ତୁ",
        "dl": "ଇନପୁଟ୍ ଓ ଆଉଟପୁଟ୍ .txt ଭାବେ ଡାଉନଲୋଡ୍ କରନ୍ତୁ",
        "tab_how": "ବ୍ୟବହାର ବିଧି",
        "tab_guide": "ପଦ୍ଧତି ଗାଇଡ୍",
        "tab_python": "ପାଇଥନ୍ ବ୍ୟବହାର",
        "tab_about": "ବିଷୟରେ",
        "how": (
            "1. ଏକ ଦିଗ ବାଛନ୍ତୁ।\n"
            "2. ଏକ ପଦ୍ଧତି ବାଛନ୍ତୁ।\n"
            "3. ଲେଖା ଟାଇପ୍ କିମ୍ବା ପେଷ୍ଟ କରନ୍ତୁ। "
            "ଟାଇପ୍ କରିବା ସହିତ ଫଳାଫଳ ଆପେ ଆପେ ବଦଳିବ।\n"
            "4. କପି ବଟନ୍ ବ୍ୟବହାର କରନ୍ତୁ କିମ୍ବା ଫଳାଫଳ ଡାଉନଲୋଡ୍ କରନ୍ତୁ।\n"
            "5. ଓଲଟା ରୂପାନ୍ତର ପାଇଁ ବଦଳ ଆଇକନ୍ ବ୍ୟବହାର କରନ୍ତୁ।\n\n"
            "**ଲିପ୍ୟନ୍ତର ଲିପି ବଦଳାଏ; ଏହା ଅର୍ଥ ଅନୁବାଦ କରେ ନାହିଁ।**"
        ),
        "powered": "{pkg} v{ver} ଦ୍ୱାରା ଚାଳିତ",
        "footer": (
            "<b>Streamlit</b> + {pypi_link} ସହ ❤️ ରେ ନିର୍ମିତ<br>{author_link} · MIT ଲାଇସେନ୍ସ"
        ),
        "conv_error": "ରୂପାନ୍ତର ବିଫଳ ହେଲା: {err}",
        "demo_error": "ପୂର୍ବାବଲୋକନ ଉପଲବ୍ଧ ନାହିଁ",
        "swap_too_long": (
            "ଆଉଟପୁଟ୍‌ରେ {n}ଟି କୋଡ୍ ପଏଣ୍ଟ ଅଛି, ଯାହା ଇନପୁଟ୍ ସୀମା {limit}ରୁ ଅଧିକ। "
            "ବଦଳାଇବା ପୂର୍ବରୁ ଇନପୁଟ୍ ଛୋଟ କରନ୍ତୁ।"
        ),
        "swap_failed": "ବଦଳାଯାଇପାରିଲା ନାହିଁ: {err}",
        "btn_clear": "ଲିଭାନ୍ତୁ",
        "btn_swap": "ଦିଗ ବଦଳାନ୍ତୁ",
        "btn_dl": "ଡାଉନଲୋଡ୍",
        "limit_reached": (
            "ଇନପୁଟ୍ ସୀମା {limit} କୋଡ୍ ପଏଣ୍ଟରେ ପହଞ୍ଚିଛି। " "ଏହାଠାରୁ ଅଧିକ ଲେଖା କଟିଯାଇଛି।"
        ),
        "odia_in_roman_hint": (
            "ଇନପୁଟ୍‌ରେ ଓଡ଼ିଆ ଲିପି ଅଛି, କିନ୍ତୁ ଦିଗ ରୋମାନ୍ → ଓଡ଼ିଆ ଅଛି। "
            "ରୋମାନ୍‌କୁ ବଦଳାଇବାକୁ ଦିଗ ବଦଳାନ୍ତୁ।"
        ),
        "scheme_hint": (
            "ପଦ୍ଧତି ବଦଳିଛି। ପ୍ରତ୍ୟେକ ପଦ୍ଧତିରେ ରୋମାନ୍ ବନାନ ଭିନ୍ନ, "
            "ତେଣୁ ନୂଆ ପଦ୍ଧତି ଅନୁଯାୟୀ ଇନପୁଟ୍ ପୁଣି ଯାଞ୍ଚ କରନ୍ତୁ।"
        ),
        "pypi": "PyPI",
        "github": "GitHub",
        "issues": "ସମସ୍ୟା ଜଣାନ୍ତୁ",
        "sidebar_tip": "ପରାମର୍ଶ",
        "tip_text": (
            "ଟାଇପ୍ କରିବା ସହିତ ଫଳାଫଳ ଆପେ ଆପେ ଅପଡେଟ୍ ହୁଏ। ସମ୍ପୂର୍ଣ୍ଣ ଓଲଟା ରୂପାନ୍ତର "
            "ପାଇଁ ISO 15919 କିମ୍ବା ITRANS ସହ ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ମୋଡ୍ "
            "ବ୍ୟବହାର କରନ୍ତୁ।"
        ),
        "about": (
            "ଲେଖକ: Srinibash Samal • MIT ଲାଇସେନ୍ସ\n\n"
            "ଲେଖା ଏହି ଆପ୍ ଦ୍ୱାରା ଅସ୍ଥାୟୀ ଭାବେ ପ୍ରକ୍ରିୟାକରଣ ହୁଏ, "
            "ଜାଣିଶୁଣି ସଂରକ୍ଷିତ ହୁଏ ନାହିଁ।"
        ),
        "desc_ISO15919": (
            "ଡାଇକ୍ରିଟିକ୍ ବ୍ୟବହାର କରି ଶୈକ୍ଷିକ ଓ ଭାଷାବୈଜ୍ଞାନିକ ସଠିକ୍ ଲିପ୍ୟନ୍ତର।"
        ),
        "desc_Hunterian": ("ନାମ, ସ୍ଥାନ ଓ ସାଧାରଣ ଲେଖା ପାଇଁ ସହଜ ରୋମାନ୍ ବନାନ।"),
        "desc_ITRANS": ("କିବୋର୍ଡ ଅନୁକୂଳ, ASCII ଧାଡ଼ି ଆଧାରିତ ଲିପ୍ୟନ୍ତର।"),
        "ex_language": "ଓଡ଼ିଆ ଭାଷା",
        "ex_greeting": "ନମସ୍କାର",
        "ex_jagannath": "ଜଗନ୍ନାଥ",
        "ex_sentence": "ବାକ୍ୟ",
        "side_schemes": "ପଦ୍ଧତି",
        "side_schemes_table": (
            "| ପଦ୍ଧତି | କେଉଁଥିପାଇଁ ଉପଯୁକ୍ତ | ଉଦାହରଣ |\n"
            "|--------|----------|---------|\n"
            "| **ISO 15919** | ଶୈକ୍ଷିକ ଲେଖା, ଉଦ୍ଧୃତି | ōṛiā bhāṣā |\n"
            "| **Hunterian** | ନାମ, ସ୍ଥାନ, URL, ସନ୍ଧାନ | oria bhasha |\n"
            "| **ITRANS** | ଇଂରାଜୀ କିବୋର୍ଡରେ ଓଡ଼ିଆ ଟାଇପିଂ | o.DiA bhAShA |"
        ),
        "side_features": "ବୈଶିଷ୍ଟ୍ୟ",
        "side_features_list": (
            "- ଦ୍ୱିମୁଖୀ ରୂପାନ୍ତର\n"
            "- ସମ୍ପୂର୍ଣ୍ଣ ଓଲଟା ରୂପାନ୍ତର (ISO ଓ ITRANS, ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ମୋଡ୍ ସହ)\n"
            "- ମିଶ୍ରିତ ଲେଖା ସୁରକ୍ଷିତ (ଇଂରାଜୀ, ସଂଖ୍ୟା, ବିରାମଚିହ୍ନ ଯଥାବତ୍ ରହେ)\n"
            "- କପି-ଅନୁକୂଳ ଇନପୁଟ୍ ଓ ଆଉଟପୁଟ୍"
        ),
        "side_useful": "କାହା ପାଇଁ ଉପଯୋଗୀ",
        "side_useful_list": (
            "- ଓଡ଼ିଆ ଭାଷା ଶିକ୍ଷାର୍ଥୀ\n"
            "- ଗବେଷକ ଓ ଭାଷାବିଜ୍ଞାନୀ\n"
            "- ବିଷୟବସ୍ତୁ ନିର୍ମାତା ଓ ସାମ୍ବାଦିକ\n"
            "- ନାମ / ସ୍ଥାନର ରୋମାନୀକରଣ\n"
            "- ଡାଟା ସଫା ଓ ସନ୍ଧାନ ସୂଚୀକରଣ\n"
            "- ଓଡ଼ିଆ କିବୋର୍ଡ ବିନା ଓଡ଼ିଆ ଟାଇପିଂ"
        ),
        "cmp_title": "ପଦ୍ଧତି ତୁଳନା (ସମାନ ଓଡ଼ିଆ ଇନପୁଟ୍)",
        "cmp_ISO15919": "ଶୈକ୍ଷିକ · ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ",
        "cmp_Hunterian": "ନାମ / ସନ୍ଧାନ · ତଥ୍ୟହ୍ରାସୀ",
        "cmp_ITRANS": "କିବୋର୍ଡ-ଅନୁକୂଳ · ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ",
        "notes_title": "📝 ଟିପ୍ପଣୀ ଓ ପରାମର୍ଶ",
        "notes": (
            "**ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ମୋଡ୍**  \n"
            "ସକ୍ରିୟ ଥିଲେ (କେବଳ ISO 15919 / ITRANS), ଅସ୍ପଷ୍ଟ ଅକ୍ଷରଗୁଡ଼ିକ "
            "ସୁରକ୍ଷିତ କରାଯାଏ, ଯାହାଫଳରେ ରୋମାନ୍ ଲେଖାକୁ *ହୁବହୁ* ମୂଳ ଓଡ଼ିଆକୁ "
            "ଫେରାଇ ପାରିବେ।  \n"
            "ଉଦାହରଣ: ଓଡ଼ିଆ ଲେଖା ଭିତରେ ଥିବା ଇଂରାଜୀ ଶବ୍ଦ ISO 15919 ରେ `:{Puri:}` "
            "ଏବଂ ITRANS ରେ `_{Puri_}` ଭଳି ଆବୃତ ହୁଏ।\n\n"
            "**Hunterian ର ସୀମା**  \n"
            "ଅନେକ ଓଡ଼ିଆ ଅକ୍ଷର ଗୋଟିଏ ରୋମାନ୍ ଅକ୍ଷରରେ ମିଶିଯାଆନ୍ତି "
            "(ଯଥା ଣ, ଞ, ନ → `n`)।  \n"
            "ଡିକୋଡିଂ ଯଥାସମ୍ଭବ ହୁଏ ଏବଂ ମୂଳ ବନାନ ଫେରିବ ବୋଲି ନିଶ୍ଚିତ ନୁହେଁ।\n\n"
            "**ମିଶ୍ରିତ ଲେଖା**  \n"
            "ଇଂରାଜୀ ଶବ୍ଦ, ସଂଖ୍ୟା ଓ ବିରାମଚିହ୍ନ ଯଥାବତ୍ ରହେ।\n\n"
            "**ଅଙ୍କ**  \n"
            "- ISO 15919 ଓଡ଼ିଆ ଅଙ୍କ (୦–୯) ରଖେ\n"
            "- Hunterian ସେଗୁଡ଼ିକୁ ASCII କରେ\n"
            "- ITRANS ସେଗୁଡ଼ିକୁ ବଦଳାଏ, reversible=True ନଥିଲେ\n\n"
            "**ITRANS ସଂକ୍ଷିପ୍ତ ରୂପ**  \n"
            "`A` ପାଇଁ `aa`, `I` ପାଇଁ `ii` ଭଳି ସାଧାରଣ ବିକଳ୍ପ ଗ୍ରହଣ କରେ।"
        ),
    },
}

# ---------------------------------------------------------------------------
# Page-level CSS (injected once via st.markdown)
# ---------------------------------------------------------------------------
CUSTOM_CSS: str = """
<style>
/* Wider main content area */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Scheme description call-out */
.scheme-info {
    border-left: 4px solid #ff7f0e;
    background: rgba(255, 127, 14, 0.08);
    border-radius: 0.35rem;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0 1rem;
}

/* Footer */
.app-footer {
    text-align: center;
    color: inherit;
    opacity: 0.65;
    font-size: 0.85rem;
    padding-top: 2rem;
}
.app-footer a {
    color: inherit;
    text-decoration: underline;
}

/* ---- Phones / narrow screens ---------------------------------------- */
@media (max-width: 640px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-size: 1.6rem !important;
        line-height: 1.25;
    }
    h2, h3 {
        font-size: 1.2rem !important;
    }
    .scheme-info {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0 0.75rem;
        font-size: 0.9rem;
    }
    /* Thumb-sized toolbar buttons */
    .st-key-btn_clear button,
    .st-key-btn_swap button,
    .st-key-btn_dl button {
        min-height: 2.75rem;
    }
    .app-footer {
        padding-top: 1rem;
    }
}
</style>
"""
