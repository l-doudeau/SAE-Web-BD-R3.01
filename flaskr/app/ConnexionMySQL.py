import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker,scoped_session
from .models import *
from secrets import token_urlsafe
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://faucher:Thierry45.@servinfo-mariadb/DBfaucher', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from .models import Personne,Client,Moniteur,Poney,Cours,Reserver
    Base.metadata.create_all(bind=engine)
    print("****************************************************************************Database Initiated********************************************")


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
#connexion ,engine = ouvrir_connexion("root","root","localhost", "GRAND_GALOP")
#connexion ,engine = ouvrir_connexion("faucher","Thierry45.","servinfo-mariadb", "DBfaucher")
#Session = sessionmaker(bind=engine)
#session = Session()
init_db()

def get_personne(id):
    return Personne.query.get(int(id))

def get_personne_email(session,email):
    return session.query(Personne).filter(Personne.adressemail == email).first()
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
    user = session.query(Client).get(id)
    session.delete(user)
    if(session.commit()):
        session.rollback()
        return False
    return True
def deletePoney(session,id):
    poney = session.query(Poney).get(id)
    session.delete(poney)
    if(not session.commit()):
        session.rollback()
        return False
    return True
def deletereservation(session,date,id,idpo):
    print(date,id,idpo+"\n\n\n")
    liste_date_time = date.split(" ")
    liste_date = liste_date_time[0].split("/")
    liste_time = liste_date_time[1].split(":")

    jmahms = datetime.datetime(int(liste_date[2]),int(liste_date[1]),int(liste_date[0]),int(liste_time[0]),int(liste_time[1]),int(liste_time[2]))
    print(jmahms)
    print(session.query(Reserver).filter(Reserver.jmahms == jmahms).filter(Reserver.id == id).filter(Reserver.idpo == idpo).all())
    reservation = session.query(Reserver).filter(Reserver.jmahms == jmahms).filter(Reserver.id == id).filter(Reserver.idpo == idpo).first()
    print(reservation)
    session.delete(reservation)
    if(session.commit()):
        session.rollback()
        return False
    return True

def get_max_id_personne(session):
    return session.query(func.max(Personne.id)).first()[0]
def get_max_id_poney(session):
    return session.query(func.max(Poney.idpo)).first()[0]
def rollback(session):
    session.rollback()
def ajout_client(session,prenom,nom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel,cotise):

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
    idpo = get_max_id_poney(session) + 1
    poney = Poney(idpo,nom,poids)
    session.add(poney)
    if(not session.commit()):
        session.rollback()

def ajout_reservation(session,date,id,idpo,idc,duree,a_paye):
    liste_datetime = date.split(" ")
    liste = liste_datetime[0].split("/")
    liste_time = liste_datetime[1].split(":")
    date_Reservation = datetime.datetime(int(liste[2]),int(liste[1]),int(liste[0]),int(liste_time[0],int(liste_time[1]),int(liste_time[2])))
    reservation = Reserver(date_Reservation,id,idpo,idc,duree,a_paye)
    session.add(reservation)
    if(not session.commit()):
        session.rollback()

