# Algorand Account Watcher
Algorand account watcher code challenge

## How to run

- `git pull git@github.com:HashMapsData2Value/AccountWatcher.git`
- `docker compose up`

# TODO

- [x] - Main Flask functionality
- [x] - Logging
- [x] - Dockerization
- [x] - Database
- [x] - Message Queue?
- [x] - Typing
- [x] - Linting
- [] - Testing
- [x] - GitHub Actions
- [x] - Documentation (docstrings, this readme, Swagger)
...

## Docker

The Flask server is containerized and is ran alongside a redis database using Docker Compose.

## CI/CD

GitHub Actions are used for CI/CD and can be found under the .github/workflows/ directory.


## Example Valid Algorand Addresses

- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ (FeeSink)
- HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA (Algorand Testnet Dispenser)