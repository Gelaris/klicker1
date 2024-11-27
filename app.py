from flask import Flask, request, jsonify

app = Flask(__name__)

# Переменная для хранения количества тапов
tap_counter = 0

@app.route("/")
def index():
    return render_template("index.html")  # HTML для кликера

@app.route("/get_counter", methods=["GET"])
def get_counter():
    # Возвращаем текущее значение счетчика
    global tap_counter
    return jsonify({"taps": tap_counter})

@app.route("/update_counter", methods=["POST"])
def update_counter():
    # Обновляем значение счетчика
    global tap_counter
    data = request.json
    if "taps" in data:
        tap_counter = data["taps"]
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
