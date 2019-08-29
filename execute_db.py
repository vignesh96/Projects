from sqlalchemy import create_engine

class Postgres(object):

    def __init__(self, connection_args):
        self.connection_string = "postgresql://{user}:{password}@{host}:{port}/{database}"
        self.connection_args = connection_args
        self.engine = None

    def connect(self):
        self.engine = create_engine(self.connection_string.format(**self.connection_args))
        self.connection = self.engine.connect()
        self.connection = self.connection.execution_options(
            isolation_level="READ COMMITTED"
        )

