# Algorand Cactus Fruit

## How to run

Assuming you have git setup and Docker installed:

- `git pull git@github.com:HashMapsData2Value/CactusFruit.git`
- `docker compose up`
- `docker compose down` (when you are done)

You could also run it in detached mode (`docker compose up -d`) but then the logs would not be immediately visible.

Docker will first build the Dockerfile containing the Python Flask application. Then, it will setup a Redis database in the same network.

The Pyton Flask application will be exposed at localhost:8000 and your terminal will show the logs from the Flask server and the Redis server.

There are three route paths:

- `/` - Will respond with a Hello World prompt.
- `/list` - Will list out all the accounts it is currently tracking.
- `/add/{account address}` - Adds the account address, assuming it is a valid Base32 address.

As a suggestion, I would suggest running:

- `curl localhost:8000/add/HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA`
- `curl localhost:8000/list`

(Or just navigating in the browser.)

This will add the [AlgoDev TestNet Dispenser](https://dispenser.testnet.aws.algodev.network/) address. Whenever someone dispense Algo from that account a change will be registered. I recommend inputting their own address into the page, which will have them send testAlgo to themselves.

## Files
- app.py - The Python Flask application with which I completed the challenge.
- utils.py - Specifically contains the RedisHelper class, a class 
- test/test_utils.py - Contains tests for the RedisHelper utility class. (I did not bother creating more tests.)

## Regarding Redis

Redis is used for two things here:
- 1) To showcase the application connecting to a database for the account tracking. This is necessary unless you'd prefer storing the tracked state inside the Flask server itself.
- 2) To showcase the application connecting to a message queue/broker. When the server notices that the balance of an account has changed, beyond ***passing it onto the application log*** it will also send it to a Redis so-called "stream", an append-only log that can be consumed by other services.

## CI/CD

GitHub Actions is used for CI/CD and can be found under the .github/workflows/ directory.

### docker-build: 

Builds the Docker image to see that it can be built. Specifically the Flask application.

Note that, in addition to setting up the Redis DB, the compose file passes in the ALGORAND_API env variable that specifies AlgoNode's testnet.

### unittest 

Will run the Python unittests which can be found under `src/tests`. Only the `utils.py` file has test coverage.

Run it locally with `python -m unittest`.

### pylint

Runs a Python linter (pylint) which gives suggestions for the code.

I have disabled certain pylint checks since this is not for production use.

Run it locally with `python -m pylint ...`.

### black

Runs a Python formatter (black) which can automatically format the code.

Run it locally `python -m black .`.