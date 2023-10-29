import json
import requests

from flask import Flask
from flask_apscheduler import APScheduler
from algosdk import encoding

from utils import ReddisHelper

app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

reddis_helper = ReddisHelper() 

algonode_api = "https://mainnet-api.algonode.cloud/v2/accounts/{}"


@app.route("/")
def hello_world():
    return "<h1>Welcome to account watcher!</h1>"


@app.route("/add/<account>")
def add_account(account: str):
    if encoding.is_valid_address(account):
        if not reddis_helper.reddis_helper.exists(account):
            reddis_helper.set_val(account, -1)
            refresh_account(account)  # TODO: Error handling here, or async?
            return "Accepted {}".format(account)  # TODO: add proper HTTP code
    #        return "Failed to store {}".format(account) #TODO: add proper HTTP code
    return "Address not valid: {}".format(account)  # TODO: add proper HTTP code


@app.route("/list")
def list_accounts():
    d = {}
    for account in reddis_helper.accounts_list:
        d[account] = reddis_helper.get_amt(account)
    return json.dumps(d)



@scheduler.task("interval", id="update_on_schedule", seconds=60)
def refresh_all_account():
    for account in reddis_helper.accounts_list:
        refresh_account(account)
    print("Ran refresh_all_account") #TODO: proper logging


def refresh_account(account: str):
    try:
        new_amount = query_account_balance(account)  # TODO: Error handling here
        old_amount = reddis_helper.get_amt(account)

        if old_amount != new_amount:
            print(
                "Address {} amount changed from {} to {}!".format(
                    account, old_amount, new_amount
                )
            )  # TODO: replace with proper notification/logging
        reddis_helper.set_val(account, new_amount)
        return True
    except:
        print(
            "Failed to update account {}".format(account)
        )  # TODO: replace with proper notification/logging


def query_account_balance(account: str):
    response = requests.get(algonode_api.format(account))
    if response.status_code == 200:
        data = response.json()
        if "amount" in data:
            return data["amount"]
        raise Exception("No amount in response")
    return -1  # TODO: Error handling here


