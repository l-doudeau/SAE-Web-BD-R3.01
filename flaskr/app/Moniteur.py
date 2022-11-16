from sqlalchemy import Integer,Column
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Moniteur(Base):
    __tablename__ = "MONITEUR"
    idP = Column(Integer, primary_key = True)
    
    def __init__(self, idp) -> None:
        self.idP = idp
    
    def __repr__(self) -> str:
        return str(self.idP)
    