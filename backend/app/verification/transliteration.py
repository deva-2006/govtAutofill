import re
import unicodedata

# Tamil consonant roots with inherent vowel / phonetic sounds
# In Tamil, 'த' can sound as 't', 'th', or 'd'. We map to 'd' or 't' with flexible normalization.
TAMIL_CONSONANT_MAP = {
    'க': 'k', 'ங': 'ng', 'ச': 's', 'ஞ': 'ny', 'ட': 't', 'ண': 'n',
    'த': 't', 'ந': 'n', 'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
    'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l', 'ற': 'r', 'ன': 'n',
    'ஜ': 'j', 'ஷ': 'sh', 'ஸ': 's', 'ஹ': 'h', 'க்ஷ': 'ksh'
}

# Special multi-character ligatures common in names
SPECIAL_NAME_MAPPINGS = {
    'தேவா': 'deva',
    'சங்கர்': 'sankar',
    'சுமதி': 'sumathi',
    'இளமாறன்': 'ilamaran',
    'கேசவன்': 'kesavan'
}

TAMIL_VOWELS = {
    'அ': 'a', 'ஆ': 'a', 'இ': 'i', 'ஈ': 'i', 'உ': 'u', 'ஊ': 'u',
    'எ': 'e', 'ஏ': 'e', 'ஐ': 'ai', 'ஒ': 'o', 'ஓ': 'o', 'ஔ': 'au'
}

TAMIL_DIACRITICS = {
    'ா': 'a', 'ி': 'i', 'ீ': 'i', 'ு': 'u', 'ூ': 'u',
    'ெ': 'e', 'ே': 'e', 'ை': 'ai', 'ொ': 'o', 'ோ': 'o', 'ௌ': 'au',
    '்': ''  # suppresses inherent vowel
}

TAMIL_INITIALS_MAP = {
    'ச': 's', 'கே': 'k', 'கா': 'k', 'கு': 'k', 'ப': 'p', 'ம': 'm',
    'த': 't', 'ர': 'r', 'வ': 'v', 'அ': 'a', 'இ': 'i', 'சு': 's'
}

def transliterate_tamil(text: str) -> str:
    """Translates Tamil text into phonetic Latin representation."""
    if not text:
        return ""
    
    t = text.strip()
    
    # Check known names first
    for k, v in SPECIAL_NAME_MAPPINGS.items():
        if k in t:
            t = t.replace(k, v)
            
    # Extract trailing initials like .ச, .கே, ச.
    initial = ""
    init_match = re.search(r'[\.]([அ-ஹ\w]+)$', t)
    if init_match:
        part = init_match.group(1)
        initial = TAMIL_INITIALS_MAP.get(part, part)
        t = t[:init_match.start()]
    else:
        init_match_pre = re.search(r'^([அ-ஹ\w]+)[\.]', t)
        if init_match_pre:
            part = init_match_pre.group(1)
            initial = TAMIL_INITIALS_MAP.get(part, part)
            t = t[init_match_pre.end():]

    out = []
    i = 0
    chars = list(t)
    while i < len(chars):
        c = chars[i]
        
        # Check special consonant clusters: ங்க -> nk/ng
        if c == 'ங' and i + 1 < len(chars) and chars[i+1] == '்':
            if i + 2 < len(chars) and chars[i+2] == 'க':
                out.append('nk')
                i += 3
                continue
                
        if c in TAMIL_VOWELS:
            out.append(TAMIL_VOWELS[c])
        elif c in TAMIL_CONSONANT_MAP:
            base = TAMIL_CONSONANT_MAP[c]
            # Check next char for diacritic
            if i + 1 < len(chars) and chars[i+1] in TAMIL_DIACRITICS:
                dia = TAMIL_DIACRITICS[chars[i+1]]
                out.append(base + dia)
                i += 2
                continue
            else:
                out.append(base + 'a')  # inherent vowel
        elif c in TAMIL_DIACRITICS:
            out.append(TAMIL_DIACRITICS[c])
        else:
            out.append(c)
        i += 1

    res = "".join(out).strip()
    if initial:
        res = f"{res} {initial}"
    return res.lower()

def normalize_phonetic(s: str) -> str:
    """Phonetically standardizes string for comparison."""
    if not s:
        return ""
    
    # Transliterate if Tamil
    if any('\u0B80' <= c <= '\u0BFF' for c in s):
        s = transliterate_tamil(s)
        
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    
    # Common phonetic collapses
    s = re.sub(r'sh', 's', s)
    s = re.sub(r'th', 't', s)
    s = re.sub(r'dh', 'd', s)
    s = re.sub(r'ee', 'i', s)
    s = re.sub(r'oo', 'u', s)
    s = re.sub(r'w', 'v', s)
    s = re.sub(r'ck', 'k', s)
    s = re.sub(r'c(?=[eiy])', 's', s)
    s = re.sub(r'c', 'k', s)
    
    tokens = [tok for tok in s.split() if tok]
    words = [t for t in tokens if len(t) > 1]
    inits = [t for t in tokens if len(t) == 1]
    
    return " ".join(words + sorted(inits))
