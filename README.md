# Routing of Telephone Calls

## Overview

This project provides an API to find the cheapest operator for a given phone number using a Trie data structure for efficient prefix-based search. The data is cached to enhance performance, and it falls back to the database if the cache is not available.

## Features

- Efficient prefix-based search using Trie.
- Caching for improved performance.
- RESTful API to find the cheapest operator for a phone number.
- Database seeding with initial operator and rate data.

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Caching
- pytest
- pytest-mock
- gevent

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/yourrepository.git
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
    SQLALCHEMY_DATABASE_URI=sqlite:///app.db
    CACHE_TYPE=FileSystemCache
    CACHE_DIR=./cache
    CACHE_DEFAULT_TIMEOUT=300
    ```

## Database Setup

1. **Initialize the database:**

    ```sh
    flask db init
    ```

2. **Create database migrations:**

    ```sh
    flask db migrate -m "Initial migration."
    ```

3. **Apply the migrations:**

    ```sh
    flask db upgrade
    ```

4. **Seed the database:**

    Ensure you have a seed file `json/operators.json` with your initial data. Example:

    ```json
    [
        {
            "name": "Operator A",
            "rates": [
                {"prefix": "123", "price": 0.1},
                {"prefix": "456", "price": 0.2}
            ]
        },
        {
            "name": "Operator B",
            "rates": [
                {"prefix": "789", "price": 0.15}
            ]
        }
    ]
    ```

    Then run the seed command:

    ```sh
    python manage_db.py seed operators
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
