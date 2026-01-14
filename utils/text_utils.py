import re

def normalize_text(text):
    if not text:
        return ""
    # Ubah ke lowercase
    text = text.lower()
    # Normalisasi karakter berulang (misal: "baaaaagus" -> "bagus")
    text = normalize_repeated_chars(text)
    # Ganti simbol/tanda baca dengan spasi agar tidak menyatukan dua kata
    text = re.sub(r'[^\w\s]', ' ', text)
    # Bersihkan semua jenis whitespace (newline, tab, multiple spaces) menjadi satu spasi
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_repeated_chars(text):
    return re.sub(r'(.)\1{2,}', r'\1', text)