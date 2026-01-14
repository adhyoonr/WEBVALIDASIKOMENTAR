import re

POSITIVE_WORDS = [
    "bagus", "mantap", "keren", "baik", "suka", "puas"

    # slang & gaul positif
    "mantul", "bestie", "solid", "trusted", "trusted seller",
    "legit", "valid", "real", "no tipu", "jujur",
    "gak bohong", "ga bohong", "on point", "relate",

    # ekspresi puas
    "puas poll", "puas pol", "puas parah",
    "suka parah", "suka banget", "love it",
    "worth parah", "worth it banget",
    "fix bagus", "fix mantap", "fix rekomen",

    # kualitas + perasaan
    "kualitas oke", "kualitas top",
    "kualitas mantap", "kualitas bagus",
    "feel premium", "kelihatan mahal",
    "nyaman dipakai", "enak dipakai",

    # pelayanan & seller
    "seller baik", "admin baik",
    "admin ramah", "seller ramah",
    "fast reply", "gercep", "gerak cepat",
    "helpful", "supportive",

    # pengiriman
    "sampe cepat", "datang cepat",
    "dateng cepet", "aman sampai tujuan",
    "packing aman", "packing niat",

    # emosi positif singkat
    "👍", "🔥", "😍", "❤️", "🥰",
    "happy banget", "seneng banget",
    "seneng parah", "senang sekali",

    # ulasan umum
    "sesuai foto", "sesuai iklan",
    "ga zonk", "tidak zonk",
    "ga nyesel", "gak nyesel",
    "repeat order", "bakal order lagi",
    "langganan", "rekomendasi",

    # bahasa campur
    "so good", "very good", "nice product",
    "good quality", "good service",
    "nice seller", "excellent",
    "awesome", "amazing",

    # ekspresi santai
    "oke banget", "oke sih",
    "aman sih", "masih oke",
    "lumayan bagus", "cukup memuaskan"
]
NEGATIVE_WORDS = [
    "jelek", "buruk", "parah", "kecewa", "lambat", "kurang"
    
    # slang & gaul negatif
    "zonk", "zonk parah", "parah sih",
    "parah banget", "gak banget",
    "ga banget", "big no", "no way",
    "fail", "failed", "rip",

    # emosi negatif
    "kecewa parah", "kecewa berat",
    "emosi", "kesel", "dongkol",
    "nyebelin", "bete", "bad mood",

    # kualitas produk
    "kualitas jelek", "kualitas buruk",
    "tipu", "ketipu", "penipuan",
    "ga asli", "tidak asli",
    "murah tapi murahan",
    "cepet rusak", "gampang rusak",

    # pelayanan
    "admin ga jelas", "seller ga jelas",
    "admin jutek", "seller jutek",
    "slow banget", "lama banget",
    "respon lama", "tidak responsif",

    # pengiriman
    "nunggu lama", "nunggu banget",
    "dateng lama", "datang lama",
    "telat parah", "molor parah",
    "packing asal", "packing buruk",

    # ketidaksesuaian
    "tidak sesuai foto",
    "beda sama foto",
    "beda sama iklan",
    "ga sesuai ekspektasi",
    "tidak sesuai ekspektasi",

    # bahasa campur
    "bad quality", "bad service",
    "worst", "worst experience",
    "very bad", "not recommended",
    "disappointed",

    # reaksi singkat
    "👎", "😡", "😤", "😠", "🤬",

    # komentar keras (non-toxic)
    "gak layak", "tidak layak",
    "kapok beli", "kapok order",
    "ga mau beli lagi",
    "tidak akan beli lagi",

    # kritik singkat
    "overrated", "overprice",
    "kemahalan", "mahal doang",
    "ga sebanding", "tidak sebanding",
    "rugi", "buang duit",

    # ekspresi informal
    "ampas", "payah banget",
    "jelek sih", "buruk sih",
    "gak oke", "ga oke",
    "tidak oke", "no comment"
]

NEGATIVE_PATTERNS = [
    r"tidak\s+(bagus|baik|layak|pintar)",
    r"kurang\s+(baik|memuaskan)",
    r"terlalu\s+(buruk|lama)"
]

def detect_sentiment(text: str) -> str:
    text = text.lower() # Double safety
    score = 0

    for w in POSITIVE_WORDS:
        if w in text:
            score += 1

    for w in NEGATIVE_WORDS:
        if w in text:
            score -= 1

    for p in NEGATIVE_PATTERNS:
        if re.search(p, text):
            score -= 1

    if score >= 1:
        return "positive"
    elif score <= -1:
        return "negative"
    return "neutral"