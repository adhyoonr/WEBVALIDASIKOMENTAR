from utils.text_utils import normalize_text
from collections import Counter

SPAM_KEYWORDS = ["promo", "diskon", "gratis", "klik", "beli", "subscribe", "link", "hadiah", "gacor"]

def detect_spam(text):
    # Gunakan teks yang sudah dinormalisasi
    normalized_text = normalize_text(text)
    words = normalized_text.split()
    
    if not words:
        return False

    counter = Counter(words)

    # Cek repetisi kata yang sama
    if max(counter.values()) >= 3:
        return True

    # Cek jumlah kata kunci spam
    cta_count = sum(1 for w in words if w in SPAM_KEYWORDS)
    if cta_count >= 2:
        return True

    # Cek densitas spam
    if cta_count / len(words) > 0.3:
        return True

    return False