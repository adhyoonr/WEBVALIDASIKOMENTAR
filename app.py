from services.validation_service import validate_comment
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")


# =========================
# MODE WEB
# =========================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    text = data.get("comment", "")
    result = validate_comment(text)
    return jsonify(result)


# =========================
# MODE CLI (TETAP ADA)
# =========================
def cli_mode():
    while True:
        text = input("Masukkan komentar (exit untuk keluar): ")
        if text.lower() == "exit":
            break

        result = validate_comment(text)
        print(result)
        print("-" * 50)


if __name__ == "__main__":
    print("Pilih mode:")
    print("1. CLI")
    print("2. Web UI")
    mode = input("Masukkan pilihan (1/2): ")

    if mode == "1":
        cli_mode()
    else:
        app.run(debug=True)
