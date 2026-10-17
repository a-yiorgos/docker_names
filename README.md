# docker_names

A small FastAPI application for educational purposes that generates Docker-style container names by randomly combining adjectives and surnames (e.g., `clever_albattani`).

## Features & Behavior

- **GET `/name`**: Returns a randomly generated name combination joining an adjective and a surname with an underscore, alongside request metrics like call count, hostname, and timestamp in JSON format.
- **GET `/name/{foobar}`**: If `foobar` is a valid adjective, returns a JSON object with `foobar` paired with a random surname. If `foobar` is a valid surname, pairs it with a random adjective. Returns HTTP 404 in JSON if `foobar` is neither.
- **GET `/name/{foo_bar}`**: Checks if `foo_bar` is a valid adjective and surname combination. Returns `{"status": "OK", "name": "foo_bar"}` with HTTP 200 if valid, or HTTP 404 in JSON if invalid.

## Environment Variables

- `PORT`: Specifies the HTTP server port (defaults to `8000`).
- `BORING_WOZNIAK`: Controls whether the restricted combination `boring_wozniak` is permitted. Defaults to `"deny"`. Set to `"allow"` to enable `boring_wozniak`.
