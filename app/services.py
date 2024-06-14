from app.models import Rate
from extensions import cache


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.price = None
        self.operator = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def initialize_trie(self):
        # Try to get trie data from cache
        cached_trie_data = cache.get('trie_data')
        if cached_trie_data:
            for prefix, price, operator in cached_trie_data:
                self.insert(prefix, price, operator)
        else:
            # Load data from database into Trie
            rates = Rate.query.all()
            trie_data = []
            for rate in rates:
                self.insert(rate.prefix, rate.price_per_minute, rate.operator.name)
                trie_data.append((rate.prefix, rate.price_per_minute, rate.operator.name))
            cache.set('trie_data', trie_data)

    def insert(self, prefix, price, operator):
        node = self.root
        for char in prefix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.price = price
        node.operator = operator

    def search(self, number):
        node = self.root
        best_price = float('inf')
        best_operator = None

        for char in number:
            if char in node.children:
                node = node.children[char]
                if node.is_end_of_word:
                    if node.price < best_price:
                        best_price = node.price
                        best_operator = node.operator
            else:
                break

        return best_operator, best_price
