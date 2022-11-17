from sqlalchemy import Integer, BOOLEAN,Column, ForeignKey
from sqlalchemy.orm import declarative_base,relationship
Base = declarative_base()
class Client(Base):
    __tablename__ = "CLIENT"
    id = Column(Integer,primary_key = True)
    cotisationa = Column(BOOLEAN)
    
    
    def __init__(self, idp, cotisationA) -> None:
        self.id = idp
        self.cotisationa = cotisationA
    
    def __repr__(self) -> str:
        return str(self.id) + " " + "a cotisé" if self.cotisationa else str(self.id) + " " +"n'a pas cotisé"
    