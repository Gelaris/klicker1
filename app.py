from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Отдаём HTML-файл кликера

@app.route("/data", methods=["POST"])
def save_data():
    data = request.json  # Получаем данные от Web App
    print(f"Received data: {data}")  # Выводим в консоль (можно сохранить в базу данных)
    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
