import hmac
import hashlib
import time
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔐 PASTE YOUR REAL API DETAILS HERE
API_KEY = "wjPWKUE0kasjAGcqBk90vXbzkjbiOP"
API_SECRET = "DqRYKHrF6TiQ5wsBnqpnKBKp6WdiHZarQsEwTA1R8OgzFTApRjUJ8G7RoAcn"

BASE_URL = "https://api.delta.exchange"

def generate_signature(method, path, body, timestamp):
    message = method + path + str(timestamp) + body
    return hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    side = data["action"]   # buy or sell
    size = 0.001            # change position size later

    path = "/v2/orders"
    method = "POST"
    timestamp = str(int(time.time()))

    body = {
        "symbol": "BTCUSDT",
        "size": size,
        "side": side,
        "order_type": "market"
    }

    body_json = json.dumps(body)
    signature = generate_signature(method, path, body_json, timestamp)

    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, data=body_json)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
