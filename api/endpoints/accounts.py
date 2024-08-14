from flask import jsonify, request

from api.services.account_service import Accounts
from app import app

accounts = Accounts()


@app.route('/balance', methods=['GET'])
def get_balance():
    account_id = request.args.get("account_id")
    result = accounts.get_balance(account_id)

    if result is None:
        # If account does not exist, returns 404 response code with balance 0.
        return jsonify(0), 404
    else:
        # Returns account balance with 200 response code.
        return jsonify(result), 200


@app.route('/reset', methods=['POST'])
def reset():
    accounts.reset_state()
    return jsonify("OK"), 200


@app.route('/event', methods=['POST'])
def handle_events():
    event = request.get_json()

    if "type" not in event:
        return jsonify({"error": "Invalid request"}), 400

    if "amount" not in event:
        return jsonify({"error": "Invalid request"}), 400

    result = accounts.process_event(event)

    event_type = event.get("type")

    if event_type == "deposit":
        return jsonify(result), 201
    elif event_type == "withdraw":
        if result is None:
            return jsonify(0), 404
        else:
            return jsonify(result), 201
    elif event_type == "transfer":
        if result is None:
            return jsonify(0), 404
        else:
            return jsonify(result), 201

    return jsonify(result), 201
