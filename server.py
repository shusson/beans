from flask import Flask, request

app = Flask(__name__)


@app.route("/event", methods=["POST"])
def log_data():
    data = request.json
    print(data)
    return "Data received", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
