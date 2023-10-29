# Algorand Account Watcher
Algorand account watcher code challenge

## How to run

- `git pull git@github.com:HashMapsData2Value/AccountWatcher.git`
- `docker compose up`

# TODO

- [x] - Main Flask functionality
- [] - Logging
- [x] - Dockerization
- [] - Database
- [] - Message Queue?
- [] - Typing
- [x] - Linting
- [] - Testing
- [x] - GitHub Actions
- [] - Monitoring
- [] - Documentation (this readme, Swagger)
...

## Docker

The Flask server is containerized and is ran alongside a redis database using Docker Compose.

## CI/CD

GitHub Actions are used for CI/CD and can be found under the .github/workflows/ directory.