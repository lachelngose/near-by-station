from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from Nearest.exception import DalEngineNotExistsError
from Nearest.entity import Base


class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None
    session = None
    metadata = MetaData()

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)

    def get_session(self):
        if not self.engine:
            raise DalEngineNotExistsError("Engine is null, please try 'db_init' first")

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def get_object_by_id(self, cls, id):
        return self.session.query(cls).get(id)

    def commit(self):
        self.session.commit()


dal = DataAccessLayer()
