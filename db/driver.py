from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Driver():
    """
    driver for running db operations outside the main API
    """

    def __init__(self, db_uri):
        """
        Create new instance of the database driver object
        :param - db_uri: - uri for the database
        """
        self._db_uri = db_uri
        self._engine = create_engine(db_uri)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()
    
    def get_access_token(self, model):
        query = self._session.query(model)
        access_token = query.get(1) # access token ID
        return access_token.value

    def get_refresh_token(self, model):
        query = self._session.query(model)
        access_token = query.get(2) # refresh token ID
        return access_token.value        
    
    def __del__(self):
        self._session.close()