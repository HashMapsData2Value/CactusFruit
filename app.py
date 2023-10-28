import json
import sched
import time
import requests
#import redis
from flask import Flask
from algosdk import encoding
app = Flask(__name__)

#r = redis.Redis(host='localhost', port=6379, db=0)

accounts = {}
algonode_api = "https://mainnet-api.algonode.cloud/v2/accounts/{}"

@app.route('/')
def hello_world():
    return 'Welcome to account watcher!'

@app.route('/add/<account>')
def add_account(account):
    if encoding.is_valid_address(account):
        if account not in accounts:
            accounts[account] = -1
#        if r.set(account, -1):
            return "Accepted {}".format(account) #TODO: add proper HTTP code
#        return "Failed to store {}".format(account) #TODO: add proper HTTP code
    return "Address not valid: {}".format(account) #TODO: add proper HTTP code

@app.route('/list')
def list_accounts():
    return json.dumps(accounts) #TODO: 

@app.route('/update') #TODO: remove so this can't be called by anyone, or put behind auth
def update_accounts():
    for account in accounts:
        amount = query_account_balance(account) #TODO: Error handling here
        if accounts[account] != amount:
            print("Address {} amount changed from {} to {}!".format(account, accounts[account], amount)) #TODO: replace with proper notification/logging
        accounts[account] = amount
        return "success" #TODO: add proper HTTP code

def query_account_balance(account):
    response = requests.get(algonode_api.format(account))
    if response.status_code == 200:
        data = response.json()
        if "amount" in data:
            return data['amount']
        raise Exception("No amount in response")
    return -1 #TODO: Error handling here


#s = sched.scheduler(time.monotonic, time.sleep)
#def run_update(a='default'):
#    print("running update_accounts()")
#    update_accounts()
#s.enter()
