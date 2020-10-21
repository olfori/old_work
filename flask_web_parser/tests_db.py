from app.models import SearchQuery, Ad, CRUD
from app import db


def add_ad():
    a = Ad(name='first test name', href='tst.com.ua', id=23145)
    db.session.add(a)
    db.session.commit()


def add_ad1():
    crud = CRUD(Ad, SearchQuery)
    crud.create_sq('attiny')
    crud.create_ad('fefe', '900 uah', 'hoirt.com', 103, 'attiny')


def del_ad():
    a = Ad.query.all()
    if len(a) > 0:
        db.session.delete(a[0])
        db.session.commit()


def del_all_ads():
    a = Ad.query.all()
    if len(a) > 0:
        for ad in a:
            db.session.delete(ad)
            db.session.commit()


# add_ad()
# del_ad()
# del_all_ads()

def add_sq():
    s = SearchQuery(name='attiny')
    db.session.add(s)
    db.session.commit()


def update_ad():
    s = SearchQuery.query.get(1)
    a = Ad.query.get(23146)
    a.search_query = s
    db.session.add(a)
    db.session.commit()


def show_all():
    ads = Ad.query.all()
    print(ads)
    sq = SearchQuery.query.all()
    print(sq)


def get_sq(sq):
    s = SearchQuery.query.filter_by(name=sq).first()
    if s:
        print(s.ads)
    else:
        print('В БД нет записи', sq)


def crud_tst1(ad):
    crud = CRUD(Ad, SearchQuery)
    # print(crud.read_all_sq())
    ads = crud.read_ads(ad)
    for ad_ in ads:
        print(ad_.name)


# add_ad()
# del_ad()
# add_sq()
# update_ad()
# add_ad1()
# get_sq('attiny')
# crud_tst1('attiny')
'''
crud = CRUD(Ad, SearchQuery)
crud.del_sq(13)
show_all()
'''


def operation1(iny) -> list:
    return iny


print(operation1('tyre'))
