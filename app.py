from flask import Flask
from api.endpoints.accounts import Accounts

app = Flask(__name__)

accounts = Accounts()


@app.route('/reset', methods=['POST'])
def reset():
    return accounts.reset_state()


@app.route('/balance', methods=['GET'])
def get_balance():
    return accounts.get_balance()


@app.route('/event', methods=['POST'])
def handle_events():
    return accounts.process_event()


if __name__ == "__main__":
    app.run(debug=True)
