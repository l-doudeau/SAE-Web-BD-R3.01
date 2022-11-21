"""
    Fichier qui regroupe la connexion ainsi que les reqûetes en SQLAlchemy.
"""

import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from .Personne import Personne
from .Client import  Client
from .Cours import Cours
from .Personne import Personne
from .Moniteur import Moniteur
from .Reserver import Reserver
from .Poney import Poney
from secrets import token_urlsafe
import datetime

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
connexion ,engine = ouvrir_connexion("doudeau","doudeau","localhost", "GRAND_GALOP")
#connexion ,engine = ouvrir_connexion("faucher","Thierry45.","servinfo-mariadb", "DBfaucher")
Session = sessionmaker(bind=engine)
session = Session()


def get_personne(session,id):
    return session.query(Personne).get(int(id))
def get_personne_email(session,email):
    return session.query(Personne).filter(Personne.adressemail == email).first()
def get_info_all_moniteu(session):
    return session.query(Moniteur)
def get_info_all_clients(session):
    return session.query(Personne.id,Personne.nomp,Personne.prenomp,Personne.ddn,Personne.adressemail,Personne.numerotel,Client.cotisationa).join(Client, Personne.id == Client.id)
def get_info_all_poney(session):
    return session.query(Poney)
def get_info_all_cours(session):
    return session.query(Cours)
def get_info_all_reservations(session):
    return session.query(Reserver.jmahms,Reserver.id,Reserver.idpo,Personne.nomp,Personne.prenomp,Cours.nomc,Poney.nomp,Reserver.duree,Reserver.a_paye).join(Client, Reserver.id == Client.id).join(Cours, Reserver.idc == Cours.idc).join(Poney, Reserver.idpo == Poney.idpo).join(Personne, Personne.id == Client.id).all()
def get_moniteur(session,id):
    return session.query(Moniteur).filter(Moniteur.id == id).first()
def get_client(session,id):
    return session.query(Client).filter(Client.id == id).first()

def deleteclient(session,id):
    """
    Il supprime un client de la base de données et renvoie True si la suppression a réussi et False si
    ce n'est pas le cas.
    
    :param session: l'objet de session
    :param id: l'identifiant du client à supprimer
    :return: La valeur de retour est une valeur booléenne.
    """
    user = session.query(Client).get(id)
    session.delete(user)
    if(session.commit()):
        session.rollback()
        return False
    return True

def deletePoney(session,id):
    """
    Il supprime un poney et toutes ses réservations
    
    :param session: l'objet de session
    :param id: l'id du poney à supprimer
    :return: Un booléen
    """
    poney = session.query(Poney).get(id)
    poney_reservation = session.query(Reserver).filter(Reserver.idpo == id).all()
    for poney_reserv in poney_reservation:
        session.delete(poney_reserv)
        session.commit()
    session.delete(poney)
    if(not session.commit()):
        session.rollback()
        return False
    return True

def deletereservation(session,date,id,idpo):
    """
    Il prend une date, un id et un idpo et supprime la réservation qui correspond à la date, l'id et
    l'idpo
    
    :param session: la session de la base de données
    :param date: "01/01/2020 00:00:00"
    :param id: l'identifiant de l'utilisateur
    :param idpo: l'identifiant de l'utilisateur qui a effectué la réservation
    :return: une valeur booléenne.
    """
    liste_date_time = date.split(" ")
    liste_date = liste_date_time[0].split("/")
    liste_time = liste_date_time[1].split(":")

    jmahms = datetime.datetime(int(liste_date[2]),int(liste_date[1]),int(liste_date[0]),int(liste_time[0]),int(liste_time[1]),int(liste_time[2]))
    reservation = session.query(Reserver).filter(Reserver.jmahms == jmahms).filter(Reserver.id == id).filter(Reserver.idpo == idpo).first()
    session.delete(reservation)
    if(session.commit()):
        session.rollback()
        return False
    return True

def deletecours(session, idc):
    """
    Il supprime un cours de la base de données, mais s'il ne parvient pas à supprimer le cours, il
    annule la transaction et renvoie False
    
    :param session: l'objet de session
    :param idc: l'identifiant du cours à supprimer
    :return: Une valeur booléenne.
    """
    cours = session.query(Cours).get(idc)
    session.delete(cours)
    if(session.commit()):
        session.rollback()
        return False
    return True

def get_max_id_personne(session):
    return session.query(func.max(Personne.id)).first()[0]
def get_max_id_cours(session):
    return session.query(func.max(Cours.idc)).first()[0]
def get_max_id_poney(session):
    return session.query(func.max(Poney.idpo)).first()[0]
def rollback(session):
    session.rollback()
    
def ajout_client(session,prenom,nom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel,cotise):
    """
    Il ajoute un client à la base de données
    
    :param session: bd
    :param prenom: chaîne de caractères
    :param nom: chaîne de caractères
    :param ddn: date
    :param poids: float
    :param adresseemail: chaîne de caractères
    :param adresse: chaîne de caractères
    :param code_postal: entier
    :param ville: chaîne de caractères
    :param numerotel: chaîne de caractères
    :param cotise: booléen
    """
    idp = get_max_id_personne(session) +1
    mdp = token_urlsafe(6)
    liste = ddn.split("/")
    date_naissance = datetime.date(int(liste[2]),int(liste[1]),int(liste[0]))
    personne = Personne(idp,prenom,nom,date_naissance,poids,adresseemail,adresse,code_postal,ville,numerotel,mdp)
    
    if(cotise == "false"): 
        cotise = False
    else: 
        cotise = True
    client = Client(idp,cotise)
    session.add(personne)
    
    if(not session.commit()):
        session.rollback()
    session.add(client)
    if(not session.commit()):
        session.rollback()

def ajout_poney(session,nom,poids):
    """
    Il ajoute un poney à la base de données
    
    :param session: bd
    :param nom: chaîne de caractères
    :param poids: float
    """
    idpo = get_max_id_poney(session) + 1
    poney = Poney(idpo,nom,poids)
    session.add(poney)
    if(not session.commit()):
        session.rollback()

def ajout_reservation(session,date,id,idpo,idc,duree,a_paye):
    """
    Il prend une date au format jj/mm/aaaa hh:mm:ss, la divise en une liste de chaînes, divise le
    premier élément de cette liste en une autre liste de chaînes, divise le deuxième élément de la
    première liste en une autre liste de chaînes, puis utilise ces listes pour créer un objet datetime
    
    :param session: bd
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
    session.add(reservation)
    if(not session.commit()):
        session.rollback()
    
def ajouteCours(session, nomc, descc, typec, prix):
    """
    Il ajoute un nouveau cours à la base de données
    
    :param session: bd
    :param nomc: chaîne de caractères
    :param descc: chaîne de caractères
    :param typec: chaîne de caractères
    :param prix: float
    :return: une valeur booléenne.
    """
    cours = Cours(get_max_id_cours(session)+1, nomc, descc, typec, prix)
    session.add(cours)
    try:
        session.commit()
        return True
    except:
        session.rollback()
        return False

def ajoute_moniteur(session,prenom,nom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel):
    """
    Il ajoute un client à la base de données
    
    :param session: bd
    :param prenom: chaîne de caractères
    :param nom: chaîne de caractères
    :param ddn: date
    :param poids: float
    :param adresseemail: chaîne de caractères
    :param adresse: chaîne de caractères
    :param code_postal: entier
    :param ville: chaîne de caractères
    :param numerotel: chaîne de caractères
    """
    idp = get_max_id_personne(session) +1
    mdp = token_urlsafe(6)
    liste = ddn.split("/")
    date_naissance = datetime.date(int(liste[2]),int(liste[1]),int(liste[0]))
    personne = Personne(idp,prenom,nom,date_naissance,poids,adresseemail,adresse,code_postal,ville,numerotel,mdp)
    moniteur = Moniteur(idp)
    session.add(personne)
    if(not session.commit()):
        session.rollback()
    session.add(moniteur)
    if(not session.commit()):
        session.rollback()
    
def delete_moniteur(session, id):
    """
    Il supprime un moniteur de la base de données et renvoie True si la suppression a réussi et False si
    ce n'est pas le cas.
    
    :param session: l'objet de session
    :param id: l'identifiant du client à supprimer
    :return: La valeur de retour est une valeur booléenne.
    """
    user = session.query(Moniteur).get(id)
    session.delete(user)
    if(session.commit()):
        session.rollback()
        return False
    return True