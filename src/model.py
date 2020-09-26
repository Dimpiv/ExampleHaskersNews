from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

base = declarative_base()


class Posts(base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String)
    created = Column(DateTime)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SqlTool(metaclass=SingletonMeta):
    def __init__(self):
        self.db = create_engine('sqlite:///:memory:', echo=False)
        session = sessionmaker(self.db)
        self.session_db = session()
        self.create_clear_base()

    def __del__(self):
        self.session_db.close()

    def create_clear_base(self):
        base.metadata.drop_all(self.db)
        base.metadata.create_all(self.db)

        from sqlalchemy import MetaData
        m = MetaData()
        m.reflect(self.db)
        for table in m.tables.values():
            print("CREATE\\CLEAR TABLE: {}".format(table.name))
            for column in table.c:
                print("Column name: {}".format(column.name))

    def add_posts(self, posts: list):
        """Clear Table posts and add new post in DataBase"""
        p = [Posts(title=row.get("title", ""), url=row.get("url", ""), created=datetime.now()) for row in posts]

        try:
            self.session_db.query(Posts).delete()
            self.session_db.commit()
        except Exception as err:
            self.session_db.rollback()
            print(err)

        try:
            self.session_db.add_all(p)
            self.session_db.commit()
        except Exception as err:
            self.session_db.rollback()
            print(err)

    def get_posts(self, lim: int) -> list:
        """Return list of posts in DataBase"""
        result = list()
        for row in self.session_db.query(Posts).limit(lim).all():
            result.append(dict(id=row.id,
                               title=row.title,
                               url=row.url,
                               created='{0:%Y-%m-%d %H:%M:%S}'.format(row.created)))
        return result

