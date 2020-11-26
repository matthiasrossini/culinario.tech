# function within flask to allow secure & time sensitive token creation
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timedelta  # time from local server
from foody import db, login_manager
from flask import current_app
# UserMixin makes user mgmt easier, not quite sure how this works tho
from flask_login import UserMixin, current_user

###########
# Models  #
###########

# user_loader helper function for the login manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# This is actually to create the column in the database


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False)
    taken = db.Column(db.String(10), nullable=False)
    number_guests = db.Column(db.Integer)

    class Products(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        pname = db.Column(db.String(30), unique=True, nullable=False)
        pdescription = db.Column(db.String(500), nullable=False)
        pprice = db.Column(db.Integer, nullable=False)
        date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
        user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
        ptype = db.Column(db.String(30))
        pgluten_free = db.Column(db.String(30))
        plactose_free = db.Column(db.String(30))
        pvegetarian = db.Column(db.String(30))
        pvegan = db.Column(db.String(30))

# this is to insert in the database what the user has input


def register(form, table_number):
    table = Table(
        table_number=table_number,
        number_guests=form.number_guests.data,
        taken="yes"
    )
    db.session.add(table)
    db.session.commit()
