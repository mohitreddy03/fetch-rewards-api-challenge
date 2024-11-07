# Instructions to run the code

## Prerequisites

- Docker installed on your machine.
- Make sure Docker is running.

## Getting Started

Follow these steps to run the server locally:

1. **Run starter.sh**:
   The script makes the docker image and starts the server at port 8080 on your local machine

2. **Use Postman or Curl**:
   Use any application to make calls to the API server. Keep in mind that there are only 2 valid APIs that are described in docs

   1. /v0/receipts/:id/points
   2. /v0/receipts/process

   Note: Using "v0" for API versioning is a strategic choice that simplifies future version upgrades and ensures a smoother transition as new versions are introduced. This approach allows for better flexibility and easier management of changes as the API evolves.

# Tests

The code also includes few unit tests that can be run using the following command. You need to have python installed however.

```
python -m unittest tests.py
```
