from services.validation_service import validate_comment
from datasets.validation_test_data import VALIDATION_DATASET

def run_validation_test():
    results = {"DITERIMA": 0, "PERLU_REVIEW": 0, "DITOLAK": 0}

    for text, expected in VALIDATION_DATASET:
        result = validate_comment(text)
        decision = result["decision"]
        results[decision] += 1

        print("Komentar :", text)
        print("Keputusan:", decision)
        print("Expected :", expected)
        print("Risk     :", result["confidence"])
        print("-" * 50)

    total = len(VALIDATION_DATASET)
    print("\nRingkasan Hasil Pengujian:")
    for k, v in results.items():
        print(f"{k}: {v} komentar ({(v/total)*100:.2f}%)")

if __name__ == "__main__":
    run_validation_test()
