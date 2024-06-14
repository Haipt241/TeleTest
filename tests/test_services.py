import pytest
import json
import os
from unittest.mock import MagicMock
from app.services import Trie, TrieNode
from extensions import cache
from run import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app


@pytest.fixture
def trie():
    return Trie()


def test_initialize_trie_from_cache(app, mocker, trie):
    with app.app_context():
        cached_trie_data = [('123', 0.1, 'Operator A'), ('456', 0.2, 'Operator B')]
        mocker.patch.object(cache, 'get', return_value=cached_trie_data)
        mocker.patch.object(cache, 'set')

        trie.initialize_trie()

        assert trie.root.children['1'].children['2'].children['3'].is_end_of_word
        assert trie.root.children['1'].children['2'].children['3'].price == 0.1
        assert trie.root.children['1'].children['2'].children['3'].operator == 'Operator A'
        assert trie.root.children['4'].children['5'].children['6'].is_end_of_word
        assert trie.root.children['4'].children['5'].children['6'].price == 0.2
        assert trie.root.children['4'].children['5'].children['6'].operator == 'Operator B'

        cache.get.assert_called_once_with('trie_data')
        cache.set.assert_not_called()


def test_initialize_trie_from_json(app, mocker, trie):
    with app.app_context():
        cache.clear()
        mocker.patch.object(cache, 'get', return_value=None)
        mocker.patch.object(cache, 'set')

        mock_data = [
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

        mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_data)))
        mocker.patch('os.path.exists', return_value=True)

        trie.initialize_trie()

        assert trie.root.children['1'].children['2'].children['3'].is_end_of_word
        assert trie.root.children['1'].children['2'].children['3'].price == 0.1
        assert trie.root.children['1'].children['2'].children['3'].operator == 'Operator A'
        assert trie.root.children['4'].children['5'].children['6'].is_end_of_word
        assert trie.root.children['4'].children['5'].children['6'].price == 0.2
        assert trie.root.children['4'].children['5'].children['6'].operator == 'Operator A'
        assert trie.root.children['7'].children['8'].children['9'].is_end_of_word
        assert trie.root.children['7'].children['8'].children['9'].price == 0.15
        assert trie.root.children['7'].children['8'].children['9'].operator == 'Operator B'

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
