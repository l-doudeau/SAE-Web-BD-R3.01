from sqlalchemy import Integer,Column,Text,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Poney(Base):
    __tablename__ = "PONEYS"
    idpo = Column(Integer, primary_key = True)
    nomp = Column(Text)
    poidssup = Column(DECIMAL)
    
    def __init__(self, idpo,nomp,poidssup) -> None:
        self.idpo = idpo
        self.nomp = nomp
        self.poidssup = poidssup
    def __repr__(self) -> str:
        return str(self.idpo) + " " + self.nomp + " " + str(self.poidssup)
    