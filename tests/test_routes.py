import pytest
import json
import os
import uuid
from run import create_app, cache
from app.routes import main as main_blueprint


@pytest.fixture
def app():
    app = create_app()
    unique_blueprint_name = f"main_{uuid.uuid4()}"
    main = main_blueprint
    main.name = unique_blueprint_name
    app.register_blueprint(main)
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        cache.clear()  # Clear cache before running tests
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_find_cheapest_no_phone_number(client):
    response = client.get('/find_cheapest')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Phone number parameter is required'}


def test_find_cheapest_cache_hit(client):
    phone_number = '1234567890'
    cache_key = f"cheapest_{phone_number}"
    # Ensure the cache contains the expected value
    cache.set(cache_key, {'operator': 'Operator A', 'price': 0.1})

    response = client.get(f'/find_cheapest?phone_number={phone_number}')
    assert response.status_code == 200
    assert response.get_json() == {'operator': 'Operator A', 'price': 0.1}


@pytest.fixture
def mock_data():
    return [
        {
            "name": "Operator A",
            "rates": [
                {"prefix": "123", "price": 0.1},
                {"prefix": "456", "price": 0.2}
            ]
        }
    ]


def prepare_cache_and_mock_data(mocker, mock_data):
    cache.clear()
    mocker.patch.object(cache, 'get', return_value=None)
    mocker.patch.object(cache, 'set')
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_data)))
    mocker.patch('os.path.exists', return_value=True)


def test_find_cheapest_cache_miss_and_found_in_trie(client, mocker, mock_data):
    phone_number = '1234567890'
    prepare_cache_and_mock_data(mocker, mock_data)

    response = client.get(f'/find_cheapest?phone_number={phone_number}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['operator'] == 'Operator A'
    assert data['price'] == 0.1


def test_find_cheapest_cache_miss_and_not_found_in_trie(client, mocker, mock_data):
    phone_number = '9999999999'
    prepare_cache_and_mock_data(mocker, mock_data)

    response = client.get(f'/find_cheapest?phone_number={phone_number}')
    assert response.status_code == 404
    assert response.get_json() == {'message': 'No suitable operator found'}
