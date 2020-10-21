from app.models import User
from app import db


def add_user():
    u = User(username='admin')
    u.set_password('pass001')
    db.session.add(u)
    db.session.commit()


def del_user():
    u = User.query.all()
    if len(u) > 0:
        db.session.delete(u[0])
        db.session.commit()


# add_user()
# del_user()

users = User.query.all()
print(users)

h = 'hi10_0'
h = h[2:].split('_')[0]

print(h)
