from extensions import db


class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    rates = db.relationship('Rate', backref='operator', lazy=True)


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(16), index=True)
    price_per_minute = db.Column(db.Float)
    operator_id = db.Column(db.Integer, db.ForeignKey('operator.id'))
