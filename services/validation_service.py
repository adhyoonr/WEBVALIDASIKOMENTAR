from models.sentiment import detect_sentiment
from models.toxic import detect_toxic
from models.spam import detect_spam
from utils.text_utils import normalize_text
import re

# Kata kasar tambahan untuk deteksi toxic lebih agresif
ADDITIONAL_TOXIC_KEYWORDS = [
    "goblok", "bodoh", "payah", "sampah", "idiot", "jelek", "memble", "tolol"
]

# Kata promosi/spam tambahan
PROMO_KEYWORDS = [
    "beli", "diskon", "promo", "gratis", "klik", "order sekarang", "cicilan", "voucher"
]

def detect_language(text):
    text = text.lower()
    indo_keywords = ["tidak", "yang", "dan", "itu", "saya", "kamu", "bagus", "jelek", "pelayanan", "produk"]
    words = set(re.findall(r'\b\w+\b', text))
    score = sum(1 for w in indo_keywords if w in words)
    return "id" if score >= 1 else "en"

def detect_mixed_sentiment(text):
    text = text.lower()
    mixed_indicators = ["tapi", "namun", "meskipun", "walaupun", "tetapi"]
    return any(word in text for word in mixed_indicators)

def validate_comment(text):
    normalized = normalize_text(text)
    language = detect_language(normalized)
    sentiment = detect_sentiment(normalized)
    toxic = detect_toxic(normalized)
    spam = detect_spam(normalized)
    mixed = detect_mixed_sentiment(normalized)

    lower_text = normalized.lower()

    # Deteksi toxic tambahan
    if any(word in lower_text for word in ADDITIONAL_TOXIC_KEYWORDS):
        toxic = True

    # Deteksi spam cerdas
    spam_score = 0.0
    if spam:
        spam_score += 0.3
    if any(p in lower_text for p in PROMO_KEYWORDS):
        spam_score += 0.3
    if re.search(r'http[s]?://', text) or re.search(r'www\.', text):
        spam_score += 0.3
    if re.search(r'@\w+', text):
        spam_score += 0.2
    if spam_score >= 0.4:
        spam = True

    # --- LOGIKA PRIORITAS TOXIC ---
    if toxic:
        return {
            "input": text,
            "state": {
                "language": language, "sentiment": sentiment, "toxic": toxic,
                "spam": spam, "mixed_sentiment": mixed, "risk_score": 1.0
            },
            "decision": "DITOLAK",
            "confidence": 1.0,
            "explanation": ["Komentar mengandung unsur toxic"]
        }

    # --- RISK SCORING ADAPTIF ---
    risk_score = 0.0
    explanation = []

    # Spam / promosi
    if spam:
        # Bobot spam adaptif: jika sentiment positif → lebih ringan
        if sentiment == "positive":
            risk_score += 0.3
            explanation.append("Komentar promosi positif")
        else:
            risk_score += 0.6
            explanation.append("Komentar spam/promosi agresif")

    # Sentimen negatif
    if sentiment == "negative":
        risk_score += 0.25
        explanation.append("Sentimen negatif")

    # Mixed sentiment
    if mixed:
        if sentiment == "neutral":
            risk_score += 0.2
            explanation.append("Komentar netral ambigu")
        else:
            risk_score += 0.2
            explanation.append("Sentimen campuran/kontradiktif")

    # Huruf kapital >3 kata → indikasi spam/emosi berlebihan
    caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
    if len(caps_words) >= 2:
        risk_score += 0.2
        explanation.append("Penggunaan huruf kapital berlebihan")

    # --- TENTUKAN KEPUTUSAN BERDASARKAN RISK SCORE ADAPTIF ---
    if risk_score >= 0.7:
        decision = "DITOLAK"
    elif risk_score >= 0.3:
        decision = "PERLU_REVIEW"
    else:
        decision = "DITERIMA"

    return {
        "input": text,
        "state": {
            "language": language,
            "sentiment": sentiment,
            "toxic": toxic,
            "spam": spam,
            "mixed_sentiment": mixed,
            "risk_score": round(risk_score, 2)
        },
        "decision": decision,
        "confidence": round(risk_score, 2),
        "explanation": explanation
    }
