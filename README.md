# Routing of Telephone Calls

## Overview

This project provides an API to find the cheapest operator for a given phone number using a Trie data structure for efficient prefix-based search. The data is cached to enhance performance, and it reads from a JSON file if the cache is not available.

## Features

- Efficient prefix-based search using Trie.
- Caching for improved performance.
- RESTful API to find the cheapest operator for a phone number.
- JSON file for initial operator and rate data.

## Requirements

- Python 3.8+
- Flask
- Flask-Caching
- pytest
- pytest-mock
- gevent

## Installation

1. **Clone the repository:**

    ```sh
    git clone git@github.com:Haipt241/TeleTest.git
    cd yourrepository
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project with the following content:

    ```env
    FLASK_ENV=development
    FLASK_APP=run.py
    SECRET_KEY=your_secret_key_here
    CACHE_TYPE=FileSystemCache
    CACHE_DIR=./cache
    CACHE_DEFAULT_TIMEOUT=300
    ```

## Running the Application

1. **Start the server:**

    ```sh
    python run.py
    ```

    The server will start on `http://localhost:5002`.

## API Endpoints

- **Find the cheapest operator**

    ```
    GET /find_cheapest?phone_number=<phone_number>
    ```

    Example:

    ```sh
    curl "http://localhost:5002/find_cheapest?phone_number=1234567890"
    ```

## Running Tests

To run the tests, use:

```sh
pytest
