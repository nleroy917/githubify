from sqlalchemy import Column, Integer, String
from .config import db

class Tokens(db.Model):
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True)
    token = Column(String(80))
    value = Column(String(80))
    
    def serialize(self):
        return {
            "id": self.id,
            "setting": self.token,
            "value": self.value
        }
        
class Spotify(db.Model):
    __tablename__ = 'spotify'
    
    id = Column(Integer, primary_key=True)
    setting = Column(String(80))
    value = Column(String(80))
    
    def serialize(self):
        return {
            "id": self.id,
            "setting": self.setting,
            "value": self.value
        }