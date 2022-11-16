from sqlalchemy import Integer, Boolean,Text,Column,Date,DECIMAL
from sqlalchemy.orm import declarative_base,relationship
Base = declarative_base()

class Personne(Base):
    __tablename__ = "PERSONNE"
    idp = Column(Integer, primary_key = True)
    nomp = Column(Text)
    prenomp = Column(Text)
    ddn = Column(Date)
    poids = Column(DECIMAL)
    adressemail = Column(Text)
    adresse = Column(Text)
    code_postal = Column(Integer)
    ville = Column(Text)
    numerotel = Column(Text)
    mdp = Column(Text)
    
    def __init__(self, idp, nomp,prenomp,ddn,poids,adressemail,adresse,code_postal,ville,numerotel,mdp) -> None:
        self.idp = idp
        self.nomp = nomp
        self.prenomp = prenomp
        self.ddn = ddn
        self.poids = poids
        self.adressemail = adressemail
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville
        self.numerotel = numerotel
        self.mdp = mdp
    
    def __repr__(self) -> str:
        return str(self.idp) + " " + self.nomp + " " + self.prenomp+ " " + str(self.ddn)+ " " + str(self.poids)+ " " + self.adressemail + " " + self.adresse+ " " + str(self.code_postal)+ " " + self.ville+ " " + self.numerotel+ " " + self.mdp
    