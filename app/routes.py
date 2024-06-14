from flask import request, jsonify, Blueprint
from app import cache
from app.services import Trie

trie = Trie()

main = Blueprint('main', __name__)


@main.route('/find_cheapest', methods=['GET'])
def find_cheapest():
    try:
        trie.initialize_trie()
        # Get 'number' parameter from query string
        number = request.args.get('phone_number')
        if not number:
            raise ValueError("Phone number parameter is required")

        # Try to get the result from cache
        cache_key = f"cheapest_{number}"
        cached_result = cache.get(cache_key)

        if cached_result:
            return jsonify(cached_result), 200

        operator, price = trie.search(number)
        if operator:
            result = {'operator': operator, 'price': price}
            cache.set(cache_key, result)  # Cache the result
            return jsonify(result), 200
        else:
            return jsonify({'message': 'No suitable operator found'}), 404
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
