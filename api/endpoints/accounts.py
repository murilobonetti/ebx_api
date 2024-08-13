from flask import jsonify, request


class Accounts:
    def __init__(self):
        self.accounts = []

        # self.accounts = [
        #     {"id": "100", "balance": 150},
        #     {"id": "300", "balance": 3500},
        # ]

    def add_account(self, account_id, balance):
        new_account = {"id": account_id, "balance": balance}
        self.accounts.append(new_account)

    def get_account(self, account_id):
        for account in self.accounts:
            if account["id"] == account_id:
                return account
        return None

    def update_balance(self, account_id, amount, is_deposit):
        account = self.get_account(account_id)
        if account:
            if is_deposit:
                account["balance"] += amount
                return account["balance"]
            else:
                account["balance"] -= amount
                return account["balance"]
        return None

    def process_event(self):
        event = request.get_json()
        if "type" not in event:
            return self._invalid_request()

        if "amount" not in event:
            return self._invalid_request()

        event_type = event.get("type")
        destination = event.get("destination")
        origin = event.get("origin")
        amount = event.get("amount")

        if event_type == "deposit":
            return self.deposit_amount(destination, amount)
        else:
            return jsonify({"error": "Something went wrong!"})

    def deposit_amount(self, account_id, amount):
        account = self.get_account(account_id)
        if account is None:
            self.add_account(account_id, amount)
        else:
            self.update_balance(account_id, amount, is_deposit=True)

        account = self.get_account(account_id)
        result = {
            "destination": {
                "id": account["id"],
                "balance": account["balance"]
            }
        }

        return jsonify(result), 201

    def get_balance(self):
        account_id = request.args.get("account_id")

        account = self.get_account(account_id)

        # If account does not exist, returns 404 response code with balance 0.
        if account is None:
            return jsonify(0), 404

        # Returns account balance with 200 response code.
        return jsonify(account["balance"]), 200

    def _invalid_request(self):
        return jsonify({"error": "Invalid request"}), 400
