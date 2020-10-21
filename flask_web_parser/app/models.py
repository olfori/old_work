from app import db

# вспомагательная таблица в БД, связывает поисковые запросы и обьявл.
ads = db.Table('ads',
               db.Column('ad_id', db.Integer, db.ForeignKey(
                   'ad.id'), primary_key=True),
               db.Column('sq_id', db.Integer, db.ForeignKey(
                   'search_query.id'), primary_key=True)
               )


class SearchQuery(db.Model):                    # Поисковые запросы в БД
    id = db.Column(db.Integer, primary_key=True)    # id запроса
    name = db.Column(db.String(180), index=True, unique=True)  # название
    ads = db.relationship('Ad', secondary=ads, lazy='subquery',
                          backref=db.backref('search_query', lazy=True))

    def __repr__(self):
        return '<{0} {1}>'.format(self.name, len(self.ads))


class Ad(db.Model):                            # ОЛХ объявления в БД
    id = db.Column(db.Integer, primary_key=True)    # id
    name = db.Column(db.String(180), index=True)    # название обьявл
    price = db.Column(db.String(120))               # цена
    href = db.Column(db.String(180))                # ссылка
    date = db.Column(db.String(120))                # дата создания
    body = db.Column(db.Text)
    view_count = db.Column(db.Text)                 # список просмотров ;

    def __repr__(self):
        return '<{}>'.format(self.name[:25])


class CRUD():
    '''Класс основных операций с БД'''

    def __init__(self, ad, seach_query):
        self.ad = ad
        self.seach_query = seach_query

    def create_sq(self, sq):
        '''Создание записи в таблице поисковых запросов'''
        if sq:
            sq = sq.strip().lower()
            if self.seach_query.query.filter_by(name=sq).first():
                return
            s = self.seach_query(name=sq)
            db.session.add(s)
            db.session.commit()

    def read_all_sq(self):
        return self.seach_query.query.all()

    def list_sq(self):
        res = []
        for sq in self.read_all_sq():
            res.append([sq.name, len(sq.ads), '', sq.id])
        return res

    def del_sq(self, sq_id):
        if sq_id:
            s = self.seach_query.query.get(sq_id)
            if s:
                db.session.delete(s)
                db.session.commit()

    def create_ad(self, name, price, link, data_id, sq):
        '''Создание записи в таблице объяв'''
        sq = sq.strip().lower()
        s = self.seach_query.query.filter_by(name=sq).first()
        a = self.ad.query.get(data_id)
        if a:
            pass
        else:
            a = self.ad(
                id=data_id,
                name=name,
                price=price,
                href=link,
                date='',
                body='',
                view_count=''
            )
        s.ads.append(a)
        db.session.add(a)
        db.session.commit()

    def read_ads(self, sq):
        s = self.seach_query.query.filter_by(name=sq).first()
        res = []
        if s:
            for ad in s.ads:
                name, price = ad.name, ad.price
                link, data_id = ad.href, ad.id
                res.append([name, price, link, data_id])
        return res
