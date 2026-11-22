from __future__ import annotations

FAVICON = "🔤"
PACKAGE_NAME = "odiatranslit"
PYPI_URL = "https://pypi.org/project/odiatranslit/"
GITHUB_URL = "https://github.com/srinibashsamal/odiatranslit"
TOOL_URL = "https://odiatranslitor.streamlit.app/"
ISSUES_URL = f"{GITHUB_URL}/issues"

MAX_CHARACTERS = 50_000  # Unicode code-point limit for the input box.
PANEL_HEIGHT = 220

# fmt: off

# DEMO_TEXTS = [
#     "ଓଡ଼ିଆ ଭାଷା ଆମ ମାତୃଭାଷା, ଏହା ଆମ ପରିଚୟ ଓ ଗର୍ବର ପ୍ରତୀକ।",
#     "ଓଡ଼ିଶା ହେଉଛି କଳା, ସଂସ୍କୃତି, ସାହିତ୍ୟ ଓ ପରମ୍ପରାର ପବିତ୍ର ଭୂମି।",
#     "ଆମ ଭାଷା ଆମ ସଂସ୍କୃତିର ମୂଳ, ତେଣୁ ଓଡ଼ିଆ କହିବା, ପଢ଼ିବା ଓ ଲେଖିବା ଆମ ପାଇଁ ଗର୍ବର ବିଷୟ।",
#     "ମୁଁ ଓଡ଼ିଆ, ମୋ ଭାଷା ଓଡ଼ିଆ, ମୋ ମାଟି ଓଡ଼ିଶା, ଏହା ମୋ ପାଇଁ ଗର୍ବ ଓ ସମ୍ମାନର ପରିଚୟ।",
# ]

JUKTAKHYARA_WORDS = [
    "ବ୍ରହ୍ମାଣ୍ଡ", "ପୁସ୍ତକ", "ସଂସ୍କାର", "ସଂସ୍କୃତି",
    "ପ୍ରଶ୍ନ", "ଦ୍ୱିତୀୟ", "ଲଜ୍ଜା", "ଗ୍ରନ୍ଥ",
    "କର୍ତ୍ତବ୍ୟ", "କର୍ତ୍ତବ୍ୟ", "ଉଜ୍ଜ୍ୱଳ", "ଉତ୍ତର",
    "ବ୍ୟକ୍ତିତ୍ୱ", "ଅଧ୍ୟୟନ", "ପୁରସ୍କାର", "ସମ୍ମାନ",
    "ଉଲ୍ଲାସ", "ଚିହ୍ନ", "ବିଦ୍ୟାଳୟ", "ପ୍ରସିଦ୍ଧ",
    "ଅବସ୍ଥା", "ସ୍ୱତନ୍ତ୍ର", "ସମ୍ପର୍କ", "ଯଜ୍ଞ",
    "ଆଶୀର୍ବାଦ", "ସମ୍ବନ୍ଧ", "ଶ୍ରଦ୍ଧା"
]

# fmt: on

SUPPORTED_LANGUAGES = ["en", "or"]
LANGUAGE_LABELS = {
    "en": "English",
    "or": "ଓଡ଼ିଆ",
}

ODIA_TO_ROMAN = "o2r"
ROMAN_TO_ODIA = "r2o"
DIRECTIONS = [ODIA_TO_ROMAN, ROMAN_TO_ODIA]

DIRECTION_FILE_LABELS = {
    ODIA_TO_ROMAN: "Odia → Roman",
    ROMAN_TO_ODIA: "Roman → Odia",
}

PLACEHOLDERS = {
    ODIA_TO_ROMAN: "ଏଠାରେ ଓଡ଼ିଆ ଲିପି ଲେଖନ୍ତୁ...\nType or paste Odia text here...",
    ROMAN_TO_ODIA: "Type or paste Roman text here...\ne.g. namaskAra  or  ōṛiā bhāṣā",
}

TRANSLITERATION_SCHEMES = ["ISO15919", "Hunterian", "ITRANS"]
REVERSIBLE_SCHEMES = {"ISO15919", "ITRANS"}
SCHEME_LABELS = {
    "ISO15919": "ISO 15919",
    "Hunterian": "Hunterian",
    "ITRANS": "ITRANS",
}

ODIA_EXAMPLES = {
    "language": "ଓଡ଼ିଆ",
    "greeting": "ନମସ୍କାର",
    "jagannath": "ଜୟ ଜଗନ୍ନାଥ",
    "sentence": "ମୋ ଓଡ଼ିଶା ଅତି ସୁନ୍ଦର।",
    "sanskrit": """ଯା କୁନ୍ଦେନ୍ଦୁ ତୁଷାରହାର ଧବଳା ଯା ଶୁଭ୍ର ବସ୍ତ୍ରାବୃତା,
ଯା ବୀଣା ବରଦଣ୍ଡ ମଣ୍ଡିତ କରା ଯା ଶ୍ୱେତ ପଦ୍ମାସନା ।
ଯା ବ୍ରହ୍ମାଚ୍ୟୁତ ଶଙ୍କର ପ୍ରଭୃତିଭିର୍ଦେବୈଃ ସଦା ପୂଜିତା,
ସା ମାଂ ପାତୁ ସରସ୍ୱତୀ ଭଗବତୀ ନିଃଶେଷ ଜାଡ୍ୟାପହା ॥""",
}

ROMAN_EXAMPLES: dict[str, dict[str, str]] = {
    "ISO15919": {
        "language": "ōṛiā",
        "greeting": "namaskāra",
        "jagannath": "jaẏa jagannātha",
        "sentence": "mō ōṛiśā ati sundara।",
        "sanskrit": """yā kundēndu tuṣārahāra dhabaḷā yā śubhra bastrābr̥tā,
yā bīṇā baradaṇḍa maṇḍita karā yā śwēta padmāsanā ।
yā brahmācẏuta śaṅkara prabhr̥tibhirdēbaiḥ sadā pūjitā,
sā māṁ pātu saraswatī bhagabatī niḥśēṣa jāḍẏāpahā ॥""",
    },
    "Hunterian": {
        "language": "oria",
        "greeting": "namaskara",
        "jagannath": "jaya jagannatha",
        "sentence": "mo orisha ati sundara।",
        "sanskrit": """ya kundendu tusharahara dhabala ya shubhra bastrabrita,
ya bina baradanda mandita kara ya shweta padmasana ।
ya brahmachyuta shangkara prabhritibhirdebaih sada pujita,
sa man patu saraswati bhagabati nihshesha jadyapaha ॥""",
    },
    "ITRANS": {
        "language": "o.DiA",
        "greeting": "namaskAra",
        "jagannath": "jaYa jagannAtha",
        "sentence": "mo o.DishA ati sundara।",
        "sanskrit": """yA kundendu tuShArahAra dhabaLA yA shubhra bastrAbRRitA,
yA bINA baradaNDa maNDita karA yA shweta padmAsanA ।
yA brahmAchYuta sha~Nkara prabhRRitibhirdebaiH sadA pUjitA,
sA mAM pAtu saraswatI bhagabatI niHsheSha jADYApahA ॥""",
    },
}

UI_TEXT: dict[str, dict[str, str]] = {
    "en": {
        "title": "Odia Transliterate",
        "tagline": (
            "Convert Odia text to Roman script and back using "
            "ISO 15919, Hunterian, or ITRANS."
        ),
        "language": "Language / ଭାଷା",
        "direction": "Conversion direction",
        ODIA_TO_ROMAN: "Odia → Roman",
        ROMAN_TO_ODIA: "Roman → Odia",
        "scheme": "Transliteration scheme",
        "reversible": "Enable reversible conversion",
        "example": "Try an example",
        "example_ph": "Select an example",
        "input": "Input",
        "output": "Output",
        "input_area": "Enter or paste your text",
        "chars": "characters",
        "words": "words",
        "copy": "Copy input to clipboard",
        "btn_copy": "Copy",
        "copied": "Copied!",
        "updating": "Updating…",
        "clear": "Clear input",
        "swap": "Use output as input and swap direction",
        "dl": "Download input and output as .txt",
        "tab_how": "How to use",
        "tab_python": "Python usage",
        "tab_about": "About",
        "how": (
            "1. Choose a direction.\n"
            "2. Choose a scheme.\n"
            "3. Type or paste text. The output updates as you type.\n"
            "4. Copy or download the result.\n"
            "5. Use the swap button to reverse the conversion.\n\n"
            "**Transliteration changes scripts. It does not translate meaning.**"
        ),
        "powered": "Uses {pkg} v{ver}",
        "footer": (
            "Built with ❤️ using <b>Streamlit</b> + {pypi_link}<br>"
            "By {author_link} · MIT License"
        ),
        "conv_error": "Conversion failed: {err}",
        "demo_error": "Preview unavailable",
        "swap_too_long": (
            "The output has {n} code points. The input limit is {limit}. "
            "Shorten the input before swapping."
        ),
        "swap_failed": "Could not swap: {err}",
        "btn_clear": "Clear",
        "btn_swap": "Swap",
        "btn_dl": "Download",
        "limit_reached": (
            "You reached the input limit of {limit} code points. "
            "The app cut off the extra text."
        ),
        "odia_in_roman_hint": (
            "The input contains Odia script, but the direction is Roman → "
            "Odia. Switch the direction to convert it to Roman."
        ),
        "scheme_hint": (
            "The scheme changed. Roman spellings differ by scheme, so "
            "check the input for the new scheme."
        ),
        "pypi": "PyPI",
        "github": "GitHub",
        "issues": "Report an issue",
        "sidebar_tip": "Tip",
        "tip_text": (
            "Results update as you type. For a lossless round trip, use "
            "ISO 15919 or ITRANS with reversible mode."
        ),
        "about": (
            "Author: Srinibash Samal • MIT License\n\n"
            "The app processes text temporarily and does not "
            "intentionally store it."
        ),
        "desc_ISO15919": (
            "Uses diacritics for linguistically precise academic transliteration."
        ),
        "desc_Hunterian": (
            "Uses simpler Roman spelling for readable names, places, and general text."
        ),
        "desc_ITRANS": (
            "Uses ASCII-style sequences for keyboard-friendly transliteration."
        ),
        "ex_language": "Odia language",
        "ex_greeting": "Greeting",
        "ex_jagannath": "Jagannath",
        "ex_sentence": "Sentence",
        "ex_sanskrit": "Shloka",
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
            "- Lossless round trips (ISO 15919 and ITRANS in reversible mode)\n"
            "- Mixed text safe (passes English, numbers, and punctuation through)\n"
            "- Easy to copy input and output"
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
        "notes_title": "Notes and tips",
        "notes": (
            "**Reversible mode**  \n"
            "When you enable reversible mode (ISO 15919 or ITRANS only), "
            "the converter escapes ambiguous characters. You can then convert "
            "the Roman text back to the *exact* original Odia.  \n"
            "Example: It wraps English words inside Odia text as `:{Puri:}` "
            "in ISO 15919 and `_{Puri_}` in ITRANS.\n\n"
            "**Hunterian limitations**  \n"
            "Several Odia letters map to the same Roman letter "
            "(such as ଣ, ଞ, ନ → `n`).  \n"
            "Decoding is best effort and may not recover the original "
            "spelling.\n\n"
            "**Mixed text**  \n"
            "English words, numbers, and punctuation pass through "
            "unchanged.\n\n"
            "**Digits**  \n"
            "- ISO 15919 keeps Odia digits (୦ to ୯)\n"
            "- Hunterian converts them to ASCII\n"
            "- ITRANS converts them unless `reversible=True`\n\n"
            "**ITRANS shortcuts**  \n"
            "ITRANS accepts common alternatives such as `aa` for `A` "
            "and `ii` for `I`."
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
        ODIA_TO_ROMAN: "ଓଡ଼ିଆ → ରୋମାନ୍",
        ROMAN_TO_ODIA: "ରୋମାନ୍ → ଓଡ଼ିଆ",
        "scheme": "ଲିପ୍ୟନ୍ତର ପଦ୍ଧତି",
        "reversible": "ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ରୂପାନ୍ତର ସକ୍ରିୟ କରନ୍ତୁ",
        "example": "ଏକ ଉଦାହରଣ ଦେଖନ୍ତୁ",
        "example_ph": "ଏକ ଉଦାହରଣ ବାଛନ୍ତୁ",
        "input": "ଇନପୁଟ୍",
        "output": "ଆଉଟପୁଟ୍",
        "input_area": "ଆପଣଙ୍କ ଲେଖା ଟାଇପ୍ କିମ୍ବା ପେଷ୍ଟ କରନ୍ତୁ",
        "chars": "ଅକ୍ଷର",
        "words": "ଶବ୍ଦ",
        "copy": "ଇନପୁଟ୍ କ୍ଲିପବୋର୍ଡକୁ କପି କରନ୍ତୁ",
        "btn_copy": "କପି",
        "copied": "କପି ହେଲା!",
        "updating": "ଅପଡେଟ୍ ହେଉଛି…",
        "clear": "ଇନପୁଟ୍ ଲିଭାନ୍ତୁ",
        "swap": "ଆଉଟପୁଟ୍‌କୁ ଇନପୁଟ୍ କରି ଦିଗ ବଦଳାନ୍ତୁ",
        "dl": "ଇନପୁଟ୍ ଓ ଆଉଟପୁଟ୍ .txt ଭାବେ ଡାଉନଲୋଡ୍ କରନ୍ତୁ",
        "tab_how": "ବ୍ୟବହାର ବିଧି",
        "tab_python": "ପାଇଥନ୍ ବ୍ୟବହାର",
        "tab_about": "ବିଷୟରେ",
        "how": (
            "1. ଏକ ଦିଗ ବାଛନ୍ତୁ।\n"
            "2. ଏକ ପଦ୍ଧତି ବାଛନ୍ତୁ।\n"
            "3. ଲେଖା ଟାଇପ୍ କିମ୍ବା ପେଷ୍ଟ କରନ୍ତୁ। "
            "ଟାଇପ୍ କରିବା ସହିତ ଫଳାଫଳ ଆପେ ଆପେ ବଦଳିବ।\n"
            "4. କପି ବଟନ୍ ବ୍ୟବହାର କରନ୍ତୁ କିମ୍ବା ଫଳାଫଳ ଡାଉନଲୋଡ୍ କରନ୍ତୁ।\n"
            "5. ଓଲଟା ରୂପାନ୍ତର ପାଇଁ ବଦଳ ଆଇକନ୍ ବ୍ୟବହାର କରନ୍ତୁ।\n\n"
            "**ଲିପ୍ୟନ୍ତର ଲିପି ବଦଳାଏ। ଏହା ଅର୍ଥ ଅନୁବାଦ କରେ ନାହିଁ।**"
        ),
        "powered": "{pkg} v{ver} ବ୍ୟବହାର କରେ",
        "footer": (
            "<b>Streamlit</b> + {pypi_link} ସହ ❤️ ରେ ନିର୍ମିତ<br>{author_link} · MIT ଲାଇସେନ୍ସ"
        ),
        "conv_error": "ରୂପାନ୍ତର ବିଫଳ ହେଲା: {err}",
        "demo_error": "ପୂର୍ବାବଲୋକନ ଉପଲବ୍ଧ ନାହିଁ",
        "swap_too_long": (
            "ଆଉଟପୁଟ୍‌ରେ {n}ଟି କୋଡ୍ ପଏଣ୍ଟ ଅଛି। ଇନପୁଟ୍ ସୀମା {limit}। ବଦଳାଇବା ପୂର୍ବରୁ ଇନପୁଟ୍ ଛୋଟ କରନ୍ତୁ।"
        ),
        "swap_failed": "ବଦଳାଯାଇପାରିଲା ନାହିଁ: {err}",
        "btn_clear": "ଲିଭାନ୍ତୁ",
        "btn_swap": "ଦିଗ ବଦଳାନ୍ତୁ",
        "btn_dl": "ଡାଉନଲୋଡ୍",
        "limit_reached": ("ଇନପୁଟ୍ ସୀମା {limit} କୋଡ୍ ପଏଣ୍ଟରେ ପହଞ୍ଚିଛି। ଆପ୍ ଅତିରିକ୍ତ ଲେଖା କାଟିଦେଇଛି।"),
        "odia_in_roman_hint": (
            "ଇନପୁଟ୍‌ରେ ଓଡ଼ିଆ ଲିପି ଅଛି, କିନ୍ତୁ ଦିଗ ରୋମାନ୍ → ଓଡ଼ିଆ ଅଛି। ରୋମାନ୍‌କୁ ବଦଳାଇବାକୁ ଦିଗ ବଦଳାନ୍ତୁ।"
        ),
        "scheme_hint": (
            "ପଦ୍ଧତି ବଦଳିଛି। ପ୍ରତ୍ୟେକ ପଦ୍ଧତିରେ ରୋମାନ୍ ବନାନ ଭିନ୍ନ, ତେଣୁ ନୂଆ ପଦ୍ଧତି ଅନୁଯାୟୀ ଇନପୁଟ୍ ପୁଣି ଯାଞ୍ଚ କରନ୍ତୁ।"
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
            "ଏହି ଆପ୍ ଲେଖାକୁ ଅସ୍ଥାୟୀ ଭାବେ ପ୍ରକ୍ରିୟାକରଣ କରେ ଏବଂ "
            "ଜାଣିଶୁଣି ସଂରକ୍ଷଣ କରେ ନାହିଁ।"
        ),
        "desc_ISO15919": ("ଡାଇକ୍ରିଟିକ୍ ବ୍ୟବହାର କରି ଶୈକ୍ଷିକ ଓ ଭାଷାବୈଜ୍ଞାନିକ ସଠିକ୍ ଲିପ୍ୟନ୍ତର।"),
        "desc_Hunterian": "ନାମ, ସ୍ଥାନ ଓ ସାଧାରଣ ଲେଖା ପାଇଁ ସହଜ ରୋମାନ୍ ବନାନ।",
        "desc_ITRANS": "କିବୋର୍ଡ ଅନୁକୂଳ, ASCII ଧାଡ଼ି ଆଧାରିତ ଲିପ୍ୟନ୍ତର।",
        "ex_language": "ଓଡ଼ିଆ ଭାଷା",
        "ex_greeting": "ନମସ୍କାର",
        "ex_jagannath": "ଜଗନ୍ନାଥ",
        "ex_sentence": "ବାକ୍ୟ",
        "ex_sanskrit": "ଶ୍ଳୋକ",
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
        "notes_title": "ଟିପ୍ପଣୀ ଓ ପରାମର୍ଶ",
        "notes": (
            "**ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ମୋଡ୍**  \n"
            "ଆପଣ ପ୍ରତ୍ୟାବର୍ତ୍ତନୀୟ ମୋଡ୍ ସକ୍ରିୟ କଲେ (କେବଳ ISO 15919 କିମ୍ବା ITRANS), "
            "କନଭର୍ଟର୍ ଅସ୍ପଷ୍ଟ ଅକ୍ଷରଗୁଡ଼ିକୁ ଏସ୍କେପ୍ କରେ। ତାପରେ ଆପଣ ରୋମାନ୍ ଲେଖାକୁ "
            "*ହୁବହୁ* ମୂଳ ଓଡ଼ିଆକୁ ଫେରାଇ ପାରିବେ।  \n"
            "ଉଦାହରଣ: ଏହା ଓଡ଼ିଆ ଲେଖା ଭିତରେ ଥିବା ଇଂରାଜୀ ଶବ୍ଦକୁ ISO 15919 ରେ "
            "`:{Puri:}` ଏବଂ ITRANS ରେ `_{Puri_}` ଭାବେ ଆବୃତ କରେ।\n\n"
            "**Hunterian ର ସୀମା**  \n"
            "ଅନେକ ଓଡ଼ିଆ ଅକ୍ଷର ଗୋଟିଏ ରୋମାନ୍ ଅକ୍ଷରରେ ମିଶିଯାଆନ୍ତି "
            "(ଯଥା ଣ, ଞ, ନ → `n`)।  \n"
            "ଡିକୋଡିଂ ଯଥାସମ୍ଭବ ହୁଏ ଏବଂ ମୂଳ ବନାନ ଫେରିବ ବୋଲି ନିଶ୍ଚିତ ନୁହେଁ।\n\n"
            "**ମିଶ୍ରିତ ଲେଖା**  \n"
            "ଇଂରାଜୀ ଶବ୍ଦ, ସଂଖ୍ୟା ଓ ବିରାମଚିହ୍ନ ଯଥାବତ୍ ରହେ।\n\n"
            "**ଅଙ୍କ**  \n"
            "- ISO 15919 ଓଡ଼ିଆ ଅଙ୍କ (୦ ରୁ ୯) ରଖେ\n"
            "- Hunterian ସେଗୁଡ଼ିକୁ ASCII କରେ\n"
            "- ITRANS ସେଗୁଡ଼ିକୁ ବଦଳାଏ, `reversible=True` ନଥିଲେ\n\n"
            "**ITRANS ସଂକ୍ଷିପ୍ତ ରୂପ**  \n"
            "ITRANS `A` ପାଇଁ `aa` ଏବଂ `I` ପାଇଁ `ii` ଭଳି ସାଧାରଣ ବିକଳ୍ପ ଗ୍ରହଣ କରେ।"
        ),
    },
}

CSS = """
<style>
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.scheme-info {
    border-left: 4px solid #ff7f0e;
    background: rgba(255, 127, 14, 0.08);
    border-radius: 0.35rem;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0 1rem;
}

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

/* Mobile layout */
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
    /* Keep action buttons easy to tap on phones. */
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
