import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from .Personne import Personne
from .Client import  Client
from .Personne import Personne
from .Moniteur import Moniteur
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
connexion ,engine = ouvrir_connexion("root","root","localhost", "GRAND_GALOP")
Session = sessionmaker(bind=engine)
session = Session()


def get_personne(session,id):
    return session.query(Personne).get(int(id))
def get_personne_email(session,email):
    return session.query(Personne).filter(Personne.adressemail == email).first()
def get_info_all_clients(session):
    return session.query(Personne.id,Personne.nomp,Personne.prenomp,Personne.ddn,Personne.adressemail,Personne.numerotel,Client.cotisationa).join(Client, Personne.id == Client.idP)
def get_moniteur(session,id):
    return session.query(Moniteur).filter(Moniteur.idP == id).first()
def get_client(session,id):
    return session.query(Client).filter(Client.idP == id).first()
def deleteclient(session,id):
    user = session.query(Client).get(id)
    session.delete(user)
    session.commit()
    return True
def get_max_id_personne(session):

    return session.query(func.max(Personne.id)).first()[0]
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