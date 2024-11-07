# Instructions to run the code

## Prerequisites

- Docker: Ensure Docker is installed and running on your machine.
- Make sure Docker is running.
- Python (for running unit tests): Python is required.

## Getting Started

Follow these steps to run the server locally:

1. **Run starter.sh**:
   The script makes the docker image and starts the server at port 8080 on your local machine
   Note for Windows Users:
   If you encounter a "command not found" error when running starter.sh, ensure the script’s line endings are set to LF instead of the default CRLF. You can change this in a text editor or with git by setting core.autocrlf to input before cloning the repository:

```
git config --global core.autocrlf input
```

2. **Use Postman or Curl**:
   Use any application to make calls to the API server. Keep in mind that there are only 2 valid APIs that are described in docs

   1. /v0/receipts/:id/points
   2. /v0/receipts/process

   Note: Using "v0" for API versioning is a strategic choice that simplifies future version upgrades and ensures a smoother transition as new versions are introduced. This approach allows for better flexibility and easier management of changes as the API evolves.

# Referencing the API Documentation

For detailed information on API endpoints, payload structures, and response formats, please refer to the API documentation located at [fetch-rewards-api-challenge/docs/api.md.](https://github.com/mohitreddy03/fetch-rewards-api-challenge/blob/main/docs/api.md)

# Tests

The code also includes few unit tests that can be run using the following command. You need to have python installed however.

```
python3 -m unittest tests.py
```
