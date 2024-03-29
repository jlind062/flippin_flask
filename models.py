from application import db


class Cities(db.Model):
    # fix for when using models to create table. don't know how or why but it works.
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city_codes = db.Column(db.String(300))
    last_updated = db.Column(db.TIMESTAMP)


class Users(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(50))
    last = db.Column(db.String(50))
    email = db.Column(db.String(75))
    username = db.Column(db.String(50))
    city = db.Column(db.Integer(), db.ForeignKey("cities.id"))
    password = db.Column(db.String(100))
    ip = db.Column(db.String(30))
    register_date = db.Column(db.TIMESTAMP, nullable=False)


class Listings(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    profit = db.Column(db.Float)
    resell_price = db.Column(db.Float)
    url = db.Column(db.String(200))
    scan_date = db.Column(db.TIMESTAMP)
    city = db.Column(db.Integer(), db.ForeignKey("cities.id"))
    source = db.Column(db.String(50))


# creates all model tables if run
if __name__ == "__main__":
    db.create_all()
