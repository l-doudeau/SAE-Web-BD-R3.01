from sqlalchemy import Integer, BOOLEAN,Column, ForeignKey
from sqlalchemy.orm import declarative_base,relationship
Base = declarative_base()
class Client(Base):
    __tablename__ = "CLIENT"
    idp = Column(Integer,primary_key = True)
    cotisationa = Column(BOOLEAN)

    
    def __init__(self, idp, cotisationA) -> None:
        self.idp = idp
        self.cotisationa = cotisationA
    
    def __repr__(self) -> str:
        return str(self.idp) + " " + "a cotisé" if self.cotisationa else str(self.idp) + " " +"n'a pas cotisé"
    