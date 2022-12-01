"""
    Fichier qui regroupe la connexion ainsi que les reqûetes en SQLAlchemy.
"""

import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker,scoped_session
from .models import *
from secrets import token_urlsafe
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#engine = create_engine('mysql+mysqlconnector://faucher:Thierry45.@servinfo-mariadb/DBfaucher', convert_unicode=True)
#engine = create_engine('mysql+mysqlconnector://root:root@localhost/GRAND_GALOP', convert_unicode=True)
engine = create_engine('mysql+mysqlconnector://doudeau:doudeau@servinfo-mariadb/DBdoudeau', convert_unicode=True)
#engine = create_engine('mysql+mysqlconnector://doudeau:doudeau@localhost/GRAND_GALOP', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from .models import Personne,Client,Moniteur,Poney,Cours,Reserver
    Base.metadata.create_all(bind=engine)
    print("************************************** Database Initiated **************************************")


def ouvrir_connexion(user,passwd,host,database):
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://'+user+':'+passwd+'@'+host+'/'+database)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx,engine

db.metadata.clear()
init_db()

def get_personne(id):
    return Personne.query.get(int(id))

def get_client(id):
    return Client.query.get(id)

def get_moniteur(id):
    return Moniteur.query.get(id)
def get_personne_email(email):
    return Personne.query.filter(Personne.adressemail == email).first()

# des que l'on fait une jointure avec d'autre tables, on a soit pas les infos soit avec le add_columns des tuples et on peut plus faire ligne.id par exemple

def get_info_all_moniteur():
    return Moniteur.query.all()

def get_info_all_clients():
    return Client.query.all()


def get_info_all_personnes():
    return Personne.query.all()

def get_info_all_poney():
    return Poney.query.all()

def get_info_all_cours():
    return Cours.query.all()

def get_info_all_reservations():
    return Reserver.query.all()


def get_moniteur(id):
    return Moniteur.query.filter(Moniteur.id == id).first()
def get_client(id):
    return Client.query.filter(Client.id == id).first()

def deleteclient(id):
    """
    Il supprime un client de la base de données et renvoie True si la suppression a réussi et False si
    ce n'est pas le cas.
    
    :param id: l'identifiant du client à supprimer
    :return: La valeur de retour est une valeur booléenne.
    """
    reservations = Reserver.query.filter(Reserver.id == id)
    for reserv in reservations : 
        db.session.delete(reserv)
        db.session.commit()

    user = Client.query.get(id)
    db.session.delete(user)
    try : 
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False

def deletePoney(id):
    """
    Il supprime un poney et toutes ses réservations
    
    :param id: l'id du poney à supprimer
    :return: Un booléen
    """
    poney = Poney.query.get(id)
    poney_reservation = Reserver.query.filter(Reserver.idpo == id).all()
    for poney_reserv in poney_reservation:
        db.session.delete(poney_reserv)
        db.session.commit()
    db.session.delete(poney)
    try : 
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False

def deletereservation(date,id,idpo):
    """
    Il prend une date, un id et un idpo et supprime la réservation qui correspond à la date, l'id et
    l'idpo
    
    :param date: "01/01/2020 00:00:00"
    :param id: l'identifiant de l'utilisateur
    :param idpo: l'identifiant de l'utilisateur qui a effectué la réservation
    :return: une valeur booléenne.
    """
    liste_date_time = date.split(" ")
    liste_date = liste_date_time[0].split("/")
    liste_time = liste_date_time[1].split(":")

    jmahms = datetime.datetime(int(liste_date[2]),int(liste_date[1]),int(liste_date[0]),int(liste_time[0]),int(liste_time[1]),int(liste_time[2]))
    reservation = Reserver.query.filter(Reserver.jmahms == jmahms).filter(Reserver.id == id).filter(Reserver.idpo == idpo).first()
    db.session.delete(reservation)
    try : 
        
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False

def deletecours(idc):
    """
    Il supprime un cours de la base de données, mais s'il ne parvient pas à supprimer le cours, il
    annule la transaction et renvoie False
    
    :param idc: l'identifiant du cours à supprimer
    :return: Une valeur booléenne.
    """
    reservations = Reserver.query.filter(Reserver.idc == idc)
    for reserv in reservations : 
        db.session.delete(reserv)

    cours = Cours.query.get(idc)
    db.session.delete(cours)
    try:
        db.session.commit()
        return True

    except:
        db.session.rollback()
        return False
    
    
    
def delete_personne(id):
    personne = Personne.query.get(id)
    client = Client.query.filter(Client.id == id).first()
    moniteur = Moniteur.query.filter(Moniteur.id == id).first()
    cours = Cours.query.filter(Cours.id == id).all()
    
    if client is not None:
        deleteclient(id)
        db.session.commit()
    elif moniteur is not None:
        for c in cours:
            deletecours(c.idc)
            db.session.commit()
        db.session.delete(moniteur)
   
    db.session.delete(personne)
    try :
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False

    

def get_max_id_personne():
    return db.session.query(func.max(Personne.id)).first()[0]

def get_max_id_cours():
    return db.session.query(func.max(Cours.idc)).first()[0]
def get_max_id_poney():
    return db.session.query(func.max(Poney.idpo)).first()[0]
    
def ajout_client(idp, cotise):
    """
    Il ajoute un client à la base de données
    
    :param idp: intreservation
    :param cotise: booléen
    """
    
    if(cotise == "false"): 
        cotise = False
    else: 
        cotise = True
    client = Client(idp,cotise)
    db.session.add(client)
    
    try:
        db.session.commit()
        return True
    except:
        
        db.session.rollback()
        return False

def ajout_poney(nom,poids):
    """
    Il ajoute un poney à la base de données
    
    :param nom: chaîne de caractères
    :param poids: float
    """
    idpo = get_max_id_poney() + 1
    poney = Poney(idpo,nom,poids)
    db.session.add(poney)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def ajout_reservation(date,id,idpo,idc,duree,a_paye):
    """
    Il prend une date au format jj/mm/aaaa hh:mm:ss, la divise en une liste de chaînes, divise le
    premier élément de cette liste en une autre liste de chaînes, divise le deuxième élément de la
    première liste en une autre liste de chaînes, puis utilise ces listes pour créer un objet datetime
    
    :param date: une chaîne au format "jj/mm/aaaa hh:mm:ss"
    :param id: int
    :param idpo: int
    :param idc: int
    :param duree: time
    :param a_paye: booléen
    """
    liste_datetime = date.split(" ")
    liste = liste_datetime[0].split("/")
    liste_time = liste_datetime[1].split(":")
    date_Reservation = datetime.datetime(int(liste[2]),int(liste[1]),int(liste[0]),int(liste_time[0],int(liste_time[1]),int(liste_time[2])))
    reservation = Reserver(date_Reservation,id,idpo,idc,duree,a_paye)
    db.session.add(reservation)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def ajouteCours(nomc, descc, typec, prix, id):
    """
    Il ajoute un nouveau cours à la base de données
    
    :param nomc: chaîne de caractères
    :param descc: chaîne de caractères
    :param typec: chaîne de caractères
    :param prix: float
    :return: une valeur booléenne.
    """
    cours = Cours(get_max_id_cours()+1, nomc, descc, typec, prix, id)
    db.session.add(cours)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def ajoute_moniteur(idp):
    """
    Il ajoute un client à la base de données
    
    :param idp: int
    """
    moniteur = Moniteur(idp)
    db.session.add(moniteur)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
    
def delete_moniteur(id):
    """
    Il supprime un moniteur de la base de données et renvoie True si la suppression a réussi et False si
    ce n'est pas le cas.
    
    :param id: l'identifiant du client à supprimer
    :return: La valeur de retour est une valeur booléenne.
    """
    moniteur = Moniteur.query.get(id)
    cours = Cours.query.filter(Cours.id == id).all()
    
    for c in cours:
        deletecours(c.idc)
        db.session.commit()
    db.session.delete(moniteur)

    try :
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False
    
    
def ajoute_personne(nomp, prenomp, ddn, poids, adressemail, adresse, code_postal, ville, numerotel) : 
    idp = get_max_id_personne() +1
    mdp = token_urlsafe(6)
    liste = ddn.split("/")
    date_naissance = datetime.date(int(liste[2]),int(liste[1]),int(liste[0]))
    personne = Personne(idp, nomp, prenomp, date_naissance, poids, adressemail, adresse, code_postal, ville, numerotel, mdp)
    db.session.add(personne)
    try :
        db.session.commit()
        
        return idp
    except :
        db.session.rollback()
        return False
    
