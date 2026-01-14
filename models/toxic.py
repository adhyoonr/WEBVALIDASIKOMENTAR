from utils.text_utils import normalize_text

TOXIC_WORDS = [
    "bodoh", "tolol", "goblok", "sampah", "bangsat",
    "tidak punya otak", "ga punya otak", "brengsek", "hina", "cok", "jancok", "gila lu"
]

def detect_toxic(text):
    # Bersihkan teks sehingga spasi antar kata selalu tunggal
    clean_text = normalize_text(text)

    for phrase in TOXIC_WORDS:
        # Karena clean_text sudah bersih, phrase "tidak punya otak" akan cocok
        if phrase in clean_text: 
            return True

    return False