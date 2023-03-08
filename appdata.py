from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import create_engine

from datamodels import scoring_base

class appdata:

    _sqlASessionMaker = None
    _sqlAConnectionStr = None

    def __init__(self, sqlAConnectionStr:str):
        sqlAEngine = create_engine(sqlAConnectionStr, future=True)
        type(self)._sqlASessionMaker = sessionmaker(bind=sqlAEngine)
        scoring_base.metadata.create_all(sqlAEngine)

    @classmethod
    def getSQLSession(cls) -> session:
        return cls._sqlASessionMaker()


        