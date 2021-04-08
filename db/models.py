from sqlalchemy import Column, Integer, String
from .config import db

class Settings(db.Model):
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    setting = Column(String(80))
    value = Column(String(80))
    
    def serialize(self):
        return {
            "id": self.id,
            "setting": self.setting,
            "value": self.value
        }