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
        if access_token is not None:
            return access_token.value
        else:
            return ''

    def get_refresh_token(self, model):
        query = self._session.query(model)
        refresh_token = query.get(2) # refresh token ID
        if refresh_token is not None:
            return refresh_token.value
        else:
            return ''
    
    def update_tokens(self, model, new_access, new_refresh):
        
        # update access token
        access_token = self._session.query(model).get(1) # the access token ID
        access_token.value = new_access
        self._session.commit()
        self._session.refresh(access_token)
        
        # update refresh token
        refresh_token = self._session.query(model).get(2) # the refresh token ID
        refresh_token.value = new_refresh
        self._session.commit()
        self._session.refresh(refresh_token)
    
    def get_most_recent_song_URI(self, model):
        query = self._session.query(model)
        most_recent = query.get(1) # most recent song id
        if most_recent is not None:
            return most_recent.value    
        else:
            return ''
    
    def update_most_recent_song(self, model, song_uri):
        query = self._session.query(model)
        most_recent = query.get(1) # most recent song id
        
        # update if exists
        # else add
        if most_recent is not None:
            most_recent.value = song_uri
        else:
            most_recent = model(
                setting='MOST_RECENT_SONG',
                value=song_uri
            )
            self._session.add(most_recent)
        self._session.commit()
