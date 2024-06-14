import logging
from flask import Blueprint, request, jsonify
from app.services import Trie
from extensions import cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Trie for prefix search
trie = Trie()

# Create Blueprint for main route
main = Blueprint('main', __name__)


@main.route('/find_cheapest', methods=['GET'])
def find_cheapest():
    try:
        # Initialize Trie before searching
        trie.initialize_trie()

        # Get 'number' parameter from query string
        number = request.args.get('phone_number')
        if not number:
            raise ValueError("Phone number parameter is required")

        logger.info(f"Received request to find cheapest rate for number: {number}")

        # Try to get the result from cache
        cache_key = f"cheapest_{number}"
        cached_result = cache.get(cache_key)

        if cached_result:
            logger.info(f"Cache hit for number: {number}")
            return jsonify(cached_result), 200

        logger.info(f"Cache miss for number: {number}, searching trie")
        operator, price = trie.search(number)
        if operator:
            result = {'operator': operator, 'price': price}
            cache.set(cache_key, result)  # Cache the result
            logger.info(f"Found operator: {operator} with price: {price} for number: {number}")
            return jsonify(result), 200
        else:
            logger.warning(f"No suitable operator found for number: {number}")
            return jsonify({'message': 'No suitable operator found'}), 404
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
