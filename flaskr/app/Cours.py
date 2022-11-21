from sqlalchemy import Integer, BOOLEAN, TEXT, DECIMAL,Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class Cours(Base):
    __tablename__ = "COURS"
    idc = Column(Integer, primary_key = True)
    nomc = Column(TEXT)
    descc = Column(TEXT)
    typec = Column(TEXT)
    prix = Column(DECIMAL)
    id = Column(Integer)

    
    def __init__(self, idc, nomc,descc,typec,prix, id) -> None:
        self.idc = idc
        self.nomc = nomc
        self.descc = descc
        self.typec = typec
        self.prix = prix
        self.id = id
        
    
    def __repr__(self) -> str:
        return str(self.idc) + " " + self.nomc + " : " + self.descc + " " + self.typec + " coute : " + str(self.prix) + " idMoniteur : " + str(self.id)
    