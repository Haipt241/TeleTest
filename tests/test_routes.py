import pytest
from app import create_app, db, cache
from app.models import Operator, Rate
from app.routes import main


@pytest.fixture
def app():
    app = create_app()
    app.register_blueprint(main)
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        print("Cache cleared!")
        yield app
        db.drop_all()


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


def test_find_cheapest_cache_miss_and_found_in_trie(client):
    phone_number = '1234567890'

    with client.application.app_context():
        operator = Operator(name='Operator A')
        db.session.add(operator)
        db.session.commit()
        rate = Rate(prefix='123', price_per_minute=0.1, operator_id=operator.id)
        db.session.add(rate)
        db.session.commit()

    response = client.get(f'/find_cheapest?phone_number={phone_number}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['operator'] == 'Operator A'
    assert data['price'] == 0.1


def test_find_cheapest_cache_miss_and_not_found_in_trie(client):
    phone_number = '9999999999'

    response = client.get(f'/find_cheapest?phone_number={phone_number}')
    assert response.status_code == 404
    assert response.get_json() == {'message': 'No suitable operator found'}
