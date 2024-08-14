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
        """
           Add a new account to the accounts list.

           :param:
           - account_id (str): Id of the account that should be created.
           - balance (int): Initial balance of the account.
        """
        new_account = {"id": account_id, "balance": balance}
        self.accounts.append(new_account)

    def get_account(self, account_id):
        """
           Look for the account with the provided account_id in the accounts
           list.

           :param:
           - account_id (str): Id of the account you want to retrieve.

           :returns: Account (dict) or None
        """
        for account in self.accounts:
            if account["id"] == account_id:
                return account
        return None

    def update_balance(self, account_id, amount, is_deposit):
        """
           Updates the balance of an account.

           :param:
           - account_id (str): Id of the account you want to retrieve.
           - amount (int): Amount that should be added or subtracted.
           - is_deposit (bool): Flag that indicates if it's a deposit or withdrawal.

           :returns: Account's balance (int) or None.
        """
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
        """
           Process the event received. This event can be the following:

               **Deposit:** An event type "deposit" can execute two different transactions.
               Create a new account if it does not exist or update
               the balance of an existing account.

               **Withdraw:** An event type "withdraw" will subtract the received amount
               from the "origin" account.

               **Transfer:** An event type "transfer" will update the balance of the
               "origin" account subtracting the amount received in the event and
               adding the same amount to the "destination" account.

           :parameter:
           - event (str): A JSON with the details of the transaction.

           :returns: dict or None.
        """
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
        """
            Make a deposit into an account. If the account does not exist
            creates one with the *amount* being the initial balance, otherwise,
            adds the *amount* received to the account.

            :param:
            - account_id (str): Id of the account to make the deposit.
            - amount (int): Amount that should be added.

            :returns: result (dict) or None.
        """
        account = self.get_account(account_id)

        if account:
            self.update_balance(account_id, amount, is_deposit=True)
        else:
            self.add_account(account_id, amount)

        account = self.get_account(account_id)
        result = {
            "destination": {
                "id": account["id"],
                "balance": account["balance"]
            }
        }

        return result

    def withdraw_amount(self, account_id, amount):
        """
            Make a withdrawal from an account subtracting the *amount* received
            from the account.

            :param:
            - account_id (str): Id of the account to make the deposit.
            - amount (int): Amount that should be added.

            :returns: result (dict) or None.
        """
        account = self.get_account(account_id)

        if account:
            new_balance = self.update_balance(
                account_id,
                amount,
                is_deposit=False
            )

            self.get_account(account_id)
            result = {
                "origin": {
                    "id": account["id"],
                    "balance": new_balance
                }
            }
            return result

        return None

    def transfer_amount(self, origin_id, amount, destination_id):
        """
            Make a transfer from an account to another subtracting the *amount* received
            from the *origin* account to the *destination* account.

            :param:
            - origin_id (str): Id of the origin account.
            - amount (int): Amount that should be transfered.
            - destination_id (str): Id of the destination account.

            :returns: result (dict) or None.
        """
        origin_account = self.get_account(origin_id)
        destination_account = self.get_account(destination_id)

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
        """
            Gets the balance from an account if it exists.

            :param:
            - account_id (str): Id of the account to get the balance.

            :returns: Account's balance (int) or None.
        """
        account = self.get_account(account_id)

        # Check if account exists and returns its balance, otherwise returns None
        if account:
            return account["balance"]
        else:
            return None
