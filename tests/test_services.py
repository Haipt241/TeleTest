import pytest
from unittest.mock import MagicMock
from app.services import Trie, TrieNode
from app.models import Rate, Operator
from extensions import cache
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def trie():
    return Trie()


def test_initialize_trie_from_cache(app, mocker, trie):
    with app.app_context():
        cached_trie_data = [('123', 0.1, 'Operator A'), ('456', 0.2, 'Operator B')]
        mocker.patch.object(cache, 'get', return_value=cached_trie_data)
        mocker.patch.object(cache, 'set')
        mocker.patch.object(Rate.query, 'all', return_value=[])

        trie.initialize_trie()

        assert trie.root.children['1'].children['2'].children['3'].is_end_of_word
        assert trie.root.children['1'].children['2'].children['3'].price == 0.1
        assert trie.root.children['1'].children['2'].children['3'].operator == 'Operator A'
        assert trie.root.children['4'].children['5'].children['6'].is_end_of_word
        assert trie.root.children['4'].children['5'].children['6'].price == 0.2
        assert trie.root.children['4'].children['5'].children['6'].operator == 'Operator B'

        cache.get.assert_called_once_with('trie_data')
        cache.set.assert_not_called()


def test_initialize_trie_from_db(app, mocker, trie):
    with app.app_context():
        cache.clear()
        mocker.patch.object(cache, 'get', return_value=None)
        mocker.patch.object(cache, 'set')
        # Setup database with mock data
        operator_a = Operator(name='Operator A')
        operator_b = Operator(name='Operator B')
        db.session.add_all([operator_a, operator_b])
        db.session.commit()

        rate_a = Rate(prefix='123', price_per_minute=0.1, operator_id=operator_a.id)
        rate_b = Rate(prefix='456', price_per_minute=0.2, operator_id=operator_b.id)
        db.session.add_all([rate_a, rate_b])
        db.session.commit()

        # Ensure that Rate.query.all() returns the correct data
        rates = Rate.query.all()
        mocker.patch.object(Rate.query, 'all', return_value=rates)

        trie.initialize_trie()

        assert trie.root.children['1'].children['2'].children['3'].is_end_of_word
        assert trie.root.children['1'].children['2'].children['3'].price == 0.1
        assert trie.root.children['1'].children['2'].children['3'].operator == 'Operator A'
        assert trie.root.children['4'].children['5'].children['6'].is_end_of_word
        assert trie.root.children['4'].children['5'].children['6'].price == 0.2
        assert trie.root.children['4'].children['5'].children['6'].operator == 'Operator B'

        cache.get.assert_called_once_with('trie_data')
        cache.set.assert_called_once()


def test_insert_and_search(trie):
    trie.insert('123', 0.1, 'Operator A')
    trie.insert('456', 0.2, 'Operator B')

    operator, price = trie.search('1234567890')
    assert operator == 'Operator A'
    assert price == 0.1

    operator, price = trie.search('4561237890')
    assert operator == 'Operator B'
    assert price == 0.2

    operator, price = trie.search('789')
    assert operator is None
    assert price == float('inf')
