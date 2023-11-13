import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 取得目前檔案路徑
current_dir = os.path.dirname(__file__)

# windows: sqlite:///tmp/test.db
# mac: sqlite:////tmp/test.db
engine = create_engine('sqlite:////{}/sigoxhelper.db'.format(current_dir), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
    print('We are connecting to database successfully!')


