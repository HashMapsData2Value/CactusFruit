"""
app.py

This file contains the main Flask application of the Cactus Fruit code challenge.

"""


# pylint: disable=import-error disable=broad-exception-caught disable=broad-exception-raised
import os
from logging.config import dictConfig
import requests
from flask import Flask, Response, jsonify
from flask_apscheduler import APScheduler
from algosdk import encoding
from utils import ReddisHelper


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

reddis_helper = ReddisHelper()

ALGORAND_API = os.getenv("ALGORAND_API") or ""


@app.route("/")
def hello_world():
    """
    Hello world route.
    """
    return "<h1>Welcome to Cactus Fruit!</h1>"


@app.route("/add/<account>")
def add_account(account: str):
    """
    Adds an account to the redis database.
    """
    try:
        app.logger.info(f"Beginning to add account {account}")
        if encoding.is_valid_address(account):
            if not reddis_helper.exists(account):
                if reddis_helper.set_val(account, -1):
                    app.logger.info(f"Successfully initialized account {account}")
                else:
                    app.logger.error(f"Failed to initialize account {account}")
                    raise Exception(f"Failed to initialize account {account}")
                refresh_account(account)
                return Response(f"Successfully added account {account}", status=200)
            return Response(f"Account already added {account}", status=200)
        app.logger.warning(f"Warning: Provided with invalid address: {account}")
        return Response(f"Address not valid: {account}", status=400)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return Response("Internal Error!", status=500)


@app.route("/list")
def list_accounts():
    """
    Returns a JSON-list of all accounts currently being tracked w/ balances.
    """
    d = {}
    for account in reddis_helper.accounts_list():
        d[account] = int(reddis_helper.get_val(account))
    return jsonify(d)


@scheduler.task("interval", id="update_on_schedule", seconds=60)
def refresh_all_account():
    """
    Refreshes the balances of the accounts in the redis database.
    Set to a schedule, every second as listed in the function decorator.
    """
    try:
        for account in reddis_helper.accounts_list():
            refresh_account(account)
    except Exception as e:
        app.logger.error(f"Error: {e}")


def refresh_account(account: str) -> bool:
    """
    Refreshes an acccount in the redis database, comparing it to the previous
    account balance. If the balance has changed, it will update the balance,
    append a refresh event to the redis stream and log it in Flask's log.
    """
    new_val = query_account_balance(account)
    old_val = reddis_helper.get_val(account)

    if old_val != new_val:
        if reddis_helper.set_val(account, new_val):
            success_message = (
                f"Address {account} amount changed from {old_val} to {new_val}!"
            )
            app.logger.info(success_message)
            reddis_helper.append_refresh(account, old_val, new_val)
            return True
        raise Exception(f"Failed to update account {account}")
    return False


def query_account_balance(account: str) -> int:
    """
    Queries the set Algorand API for the balance of an account.
    """
    res = requests.get(ALGORAND_API.format(account))
    if res.status_code == 200:
        data = res.json()
        if "amount" in data:
            return int(data["amount"])
        raise Exception("No amount in response")
    raise Exception(f"Bad response from algonde_api {res}")
