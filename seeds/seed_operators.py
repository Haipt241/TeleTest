import json
import os
from app import db
from app.models import Operator, Rate
from extensions import cache


def seed():
    # Clear cache before seeding
    cache.clear()
    print("Cache cleared!")

    seed_file = os.path.join(os.path.dirname(__file__), 'json/operators.json')

    if os.path.exists(seed_file):
        with open(seed_file, 'r') as f:
            operators = json.load(f)
        try:
            for operator_data in operators:
                operator_name = operator_data['name']
                existing_operator = Operator.query.filter_by(name=operator_name).first()

                if not existing_operator:
                    operator = Operator(name=operator_name)
                    db.session.add(operator)
                    db.session.commit()
                else:
                    operator = existing_operator

                for rate_data in operator_data['rates']:
                    prefix = rate_data['prefix']
                    price = rate_data['price']
                    existing_rate = Rate.query.filter_by(prefix=prefix, operator_id=operator.id).first()

                    if not existing_rate:
                        rate = Rate(prefix=prefix, price_per_minute=price, operator_id=operator.id)
                        db.session.add(rate)

            db.session.commit()
            print('Operators and rates seeded!')
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while seeding data: {e}")
    else:
        print(f'Seed file {seed_file} not found.')
