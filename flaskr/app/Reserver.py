from sqlalchemy import Integer,Column,DATETIME,TIME,BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Reserver(Base):
    __tablename__ = "RESERVER"
    jmahms = Column(DATETIME, primary_key = True)
    id = Column(Integer, primary_key=True)
    idc = Column(Integer, primary_key=True)
    idpo = Column(Integer)
    duree = Column(TIME)
    a_paye = Column(BOOLEAN)

    def __init__(self, jmahms,id,idc,idpo,duree,a_paye) -> None:
        self.jmahms = jmahms
        self.id = id
        self.idc = idc
        self.idpo = idpo
        self.duree = duree
        self.a_paye = a_paye
    
    def __repr__(self) -> str:
        return str(self.jmahms) + " " + str(self.id) + " " + str(self.idpo) + " " + str(self.duree) + " " + str(self.a_paye)
    