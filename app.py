import requests

from flask import Flask, Response, jsonify
from flask_apscheduler import APScheduler
from logging.config import dictConfig

from algosdk import encoding

from utils import ReddisHelper


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

reddis_helper = ReddisHelper() 

ALGONODE_API = "https://testnet-api.algonode.cloud/v2/accounts/{}"

@app.route("/")
def hello_world():
    return "<h1>Welcome to account watcher!</h1>"

@app.route("/add/<account>")
def add_account(account: str):
    try:
        app.logger.info("Beginning to add account {}".format(account))
        if encoding.is_valid_address(account):
            if not reddis_helper.exists(account):
                if reddis_helper.set_val(account, -1):
                    app.logger.info("Successfully initialized account {}".format(account))
                else:
                    app.logger.error("Failed to initialize account {}".format(account))
                    raise Exception("Failed to initialize account {}".format(account))
                refresh_account(account)
                return Response("Successfully added account {}".format(account), status=200)
            return Response("Account already added {}".format(account), status=200)
        else:
            app.logger.warning("Warning: Provided with invalid address: {}".format(account))
            return Response("Address not valid: {}".format(account), status=400)
    except Exception as e:
        app.logger.error("Error: {}".format(e))
        return Response("Internal Error!", status=500)

@app.route("/list")
def list_accounts():
    d = {}
    for account in reddis_helper.accounts_list():
        d[account] = int(reddis_helper.get_val(account))
    return jsonify(d)

@scheduler.task("interval", id="update_on_schedule", seconds=60)
def refresh_all_account():
    try:
        for account in reddis_helper.accounts_list():
            refresh_account(account)
    except Exception as e:
        app.logger.error("Error: {}".format(e))

def refresh_account(account: str) -> bool:
    new_val = query_account_balance(account)
    old_val = reddis_helper.get_val(account)

    if old_val != new_val:
        if reddis_helper.set_val(account, new_val):
            success_message = "Address {} amount changed from {} to {}!".format(
                account, old_val, new_val
            )
            app.logger.info(success_message)
            if not reddis_helper.append_refresh(account, old_val, new_val):
                raise Exception("Failed to append refresh success for account {}".format(account))
            return True
        else:
            raise Exception("Failed to update account {}".format(account))
    return False

def query_account_balance(account: str) -> int:
    res = requests.get(ALGONODE_API.format(account))
    if res.status_code == 200:
        data = res.json()
        if "amount" in data:
            return int(data["amount"])
        raise Exception("No amount in response")
    raise Exception("Bad response from algonde_api {}".format(res))

