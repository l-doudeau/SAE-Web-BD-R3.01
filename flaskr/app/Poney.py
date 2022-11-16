from sqlalchemy import Integer,Column,Text,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Poney(Base):
    __tablename__ = "PONEYS"
    idpo = Column(Integer, primary_key = True)
    nomp = Column(Text)
    poidsup = Column(DECIMAL)
    
    def __init__(self, idpo,nomp,poidsup) -> None:
        self.idpo = idpo
        self.nomp = nomp
        self.poidsup = poidsup
    def __repr__(self) -> str:
        return str(self.idpo) + " " + self.nomp + " " + self.poidsup
    