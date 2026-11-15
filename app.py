import os

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "dev")

ORDERS = {
    "1001": {"item": "Headphones", "status": "SHIPPED"},
    "1002": {"item": "Keyboard", "status": "PACKED"},
}


@app.route("/health")
def health():
    # Lab switch: simulates a release that is broken in production
    if os.getenv("BREAK_HEALTH") == "true":
        return jsonify(status="DOWN", version=VERSION), 503

    return jsonify(status="UP", version=VERSION)


@app.route("/orders/<order_id>")
def get_order(order_id):
    order = ORDERS.get(order_id)

    if order is None:
        return jsonify(error="order not found"), 404

    return jsonify(id=order_id, **order)
