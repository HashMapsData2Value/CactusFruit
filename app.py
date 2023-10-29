import json
import requests
#import redis
from flask import Flask
from flask_apscheduler import APScheduler
from algosdk import encoding

app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

#r = redis.Redis(host='localhost', port=6379, db=0)

accounts = {}
algonode_api = "https://mainnet-api.algonode.cloud/v2/accounts/{}"

@app.route('/')
def hello_world():
    return '<h1>Welcome to account watcher!</h1>'

@app.route('/add/<account>')
def add_account(account):
    if encoding.is_valid_address(account):
        if account not in accounts:
            accounts[account] = -1 #unless changed will mean -1 means uninitialized account
#        if r.set(account, -1):
            update_account(account) #TODO: Error handling here, or async?
            return "Accepted {}".format(account) #TODO: add proper HTTP code
#        return "Failed to store {}".format(account) #TODO: add proper HTTP code
    return "Address not valid: {}".format(account) #TODO: add proper HTTP code

@app.route('/list')
def list_accounts():
    return json.dumps(accounts) #TODO: 

@scheduler.task('interval', id='update_on_schedule', seconds=60)
def update_all_accounts():
    for account in accounts:
        update_account(account)


def update_account(account):
    try:
        amount = query_account_balance(account) #TODO: Error handling here
        if accounts[account] != amount:
            print("Address {} amount changed from {} to {}!".format(account, accounts[account], amount)) #TODO: replace with proper notification/logging
        accounts[account] = amount
        return True
    except:
        print("Failed to update account {}".format(account)) #TODO: replace with proper notification/logging

def query_account_balance(account):
    response = requests.get(algonode_api.format(account))
    if response.status_code == 200:
        data = response.json()
        if "amount" in data:
            return data['amount']
        raise Exception("No amount in response")
    return -1 #TODO: Error handling here