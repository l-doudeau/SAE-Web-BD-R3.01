from sqlalchemy import Integer,Column
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Moniteur(Base):
    __tablename__ = "MONITEUR"
    id = Column(Integer, primary_key = True)
    
    def __init__(self, idp) -> None:
        self.id = idp
    
    def __repr__(self) -> str:
        return str(self.id)
    