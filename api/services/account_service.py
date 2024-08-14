class Accounts:
    def __init__(self):
        self.accounts = [
            {"id": "300", "balance": 0}
        ]

    def reset_state(self):
        self.accounts = [
            {"id": "300", "balance": 0}
        ]

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

    def process_event(self, event):

        event_type = event.get("type")
        destination = event.get("destination")
        origin = event.get("origin")
        amount = event.get("amount")

        if event_type == "deposit":
            return self.deposit_amount(destination, amount)
        elif event_type == "withdraw":
            return self.withdraw_amount(origin, amount)
        elif event_type == "transfer":
            return self.transfer_amount(origin, amount, destination)
        else:
            return {"error": "Something went wrong!"}

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

        return result

    def withdraw_amount(self, account_id, amount):
        account = self.get_account(account_id)

        # Check if account exists, if not returns None
        if account is None:
            return None

        new_balance = self.update_balance(account_id, amount, is_deposit=False)

        self.get_account(account_id)
        result = {
            "origin": {
                "id": account["id"],
                "balance": new_balance
            }
        }
        return result

    def transfer_amount(self, origin_id, amount, destination_id):
        origin_account = self.get_account(origin_id)
        destination_account = self.get_account(destination_id)

        # Check if both accounts exist, if not returns None
        if origin_account is None or destination_account is None:
            return None

        # Update balance of both accounts
        origin_account["balance"] -= amount
        destination_account["balance"] += amount

        result = {
            "origin": {
                "id": origin_id,
                "balance": origin_account["balance"]
            },
            "destination": {
                "id": destination_id,
                "balance": destination_account["balance"]
            }
        }
        return result

    def get_balance(self, account_id):
        account = self.get_account(account_id)

        if account is None:
            return None

        return account["balance"]
