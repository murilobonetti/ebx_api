from flask import jsonify, request

from api.services.account_service import Accounts
from app import app

accounts = Accounts()


@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Gets the balance from a specific account.

    :return: Account balance with Response code 200 or 404.
    """
    account_id = request.args.get("account_id")
    result = accounts.get_balance(account_id)

    if result is None:
        return jsonify(0), 404
    else:
        return jsonify(result), 200


@app.route('/reset', methods=['POST'])
def reset():
    """
    Resets the API to its original state.

    :return: OK with Response code 200.
    """
    accounts.reset_state()
    return jsonify("OK"), 200


@app.route('/event', methods=['POST'])
def handle_events():
    """
    Handles the following events:

    - Account creation

    - Deposit

    - Withdraw

    - Transfer

    :return: Returns a JSON with the result of the transaction or an error.
    """
    event = request.get_json()

    if "type" not in event:
        return jsonify({"error": "Invalid request"}), 400

    if "amount" not in event:
        return jsonify({"error": "Invalid request"}), 400

    result = accounts.process_event(event)

    if result:
        return jsonify(result), 201
    else:
        return jsonify(0), 404
