from sqlalchemy import Integer, BOOLEAN,Column, ForeignKey
from sqlalchemy.orm import declarative_base,relationship
from .app import db
from flask_login import UserMixin


class Client(db.Model):
    id = db.Column(db.Integer,ForeignKey("personne.id"),primary_key = True)
    cotisationa = db.Column(db.BOOLEAN)
    personne = relationship("Personne")

    def __init__(self, idp, cotisationA) -> None:
        self.id = idp
        self.cotisationa = cotisationA
    
    def __repr__(self) -> str:
        return str(self.id) + " " + "a cotisé" if self.cotisationa else str(self.id) + " " +"n'a pas cotisé"

class Cours(db.Model):
    idc = db.Column(db.Integer, primary_key = True)
    nomc = db.Column(db.String(20))
    descc = db.Column(db.String(100))
    typec = db.Column(db.String(20))
    prix = db.Column(db.DECIMAL)
    moniteur_id = db.Column(db.Integer,ForeignKey("moniteur.id"))
    cours = relationship("Moniteur")
    
    def __init__(self, idc, nomc,descc,typec,prix) -> None:
        self.idc = idc
        self.nomc = nomc
        self.descc = descc
        self.typec = typec
        self.prix = prix
    
    def __repr__(self) -> str:
        return str(self.idc) + " " + self.nomc + " : " + self.descc + " " + self.typec + " coute : " + str(self.prix)

class Moniteur(db.Model):
    id = db.Column(db.Integer,ForeignKey("personne.id"), primary_key = True)
    personne = relationship("Personne")
    def __init__(self, idp) -> None:
        self.id = idp
    
    def __repr__(self) -> str:
        return str(self.id)


class Personne(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nomp = db.Column(db.String(20))
    prenomp = db.Column(db.String(20))
    ddn = db.Column(db.Date)
    poids = db.Column(db.DECIMAL)
    adressemail = db.Column(db.String(20))
    adresse = db.Column(db.String(20))
    code_postal = db.Column(db.Integer)
    ville = db.Column(db.String(20))
    numerotel = db.Column(db.String(20))
    mdp = db.Column(db.String(20))

   
    def __init__(self, idp, nomp,prenomp,ddn,poids,adressemail,adresse,code_postal,ville,numerotel,mdp) -> None:
        self.id         = idp
        self.nomp       = nomp
        self.prenomp    = prenomp
        self.ddn        = ddn
        self.poids      = poids
        self.adressemail = adressemail
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville
        self.numerotel = numerotel
        self.mdp = mdp
    
    def __repr__(self) -> str:
        return str(self.id) + " " + self.nomp + " " + self.prenomp+ " " + str(self.ddn)+ " " + str(self.poids)+ " " + self.adressemail + " " + self.adresse+ " " + str(self.code_postal)+ " " + self.ville+ " " + self.numerotel+ " " + self.mdp


class Poney(db.Model):
    idpo = db.Column(db.Integer, primary_key = True)
    nomp = db.Column(db.String(20))
    poidssup = db.Column(db.DECIMAL)
    
    def __init__(self, idpo,nomp,poidssup) -> None:
        self.idpo = idpo
        self.nomp = nomp
        self.poidssup = poidssup
    def __repr__(self) -> str:
        return str(self.idpo) + " " + self.nomp + " " + str(self.poidssup)


class Reserver(db.Model):
    jmahms = db.Column(db.DATETIME, primary_key = True)
    id = db.Column(db.Integer, primary_key=True)
    idc = db.Column(db.Integer,ForeignKey("cours.idc"), primary_key=True)
    idpo = db.Column(db.Integer,ForeignKey("poney.idpo"))
    duree = db.Column(db.TIME)
    a_paye = db.Column(db.BOOLEAN)
    poney = relationship("Poney")
    cours = relationship("Cours") 
    def __init__(self, jmahms,id,idc,idpo,duree,a_paye) -> None:
        self.jmahms = jmahms
        self.id = id
        self.idc = idc
        self.idpo = idpo
        self.duree = duree
        self.a_paye = a_paye
    
    def __repr__(self) -> str:
        return str(self.jmahms) + " " + str(self.id) + " " + str(self.idpo) + " " + str(self.duree) + " " + str(self.a_paye)

