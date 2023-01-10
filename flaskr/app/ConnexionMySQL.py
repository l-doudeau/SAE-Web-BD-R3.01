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


engine = create_engine('mysql+mysqlconnector://faucher:Thierry45.@servinfo-mariadb/DBfaucher', convert_unicode=True)
#engine = create_engine('mysql+mysqlconnector://root:root@localhost/GRAND_GALOP', convert_unicode=True)
#engine = create_engine('mysql+mysqlconnector://doudeau:doudeau@servinfo-mariadb/DBdoudeau', convert_unicode=True)
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
def get_cours(id):
    return Cours.query.get(int(id))
def get_client(id):
    return Client.query.get(id)
def get_poney(id):
    return Poney.query.get(id)

def get_moniteur(id):
    return Moniteur.query.get(id)
def get_personne_email(email):
    return Personne.query.filter(Personne.adressemail == email).first()

# des que l'on fait une jointure avec d'autre tables, on a soit pas les infos soit avec le add_columns des tuples et on peut plus faire ligne.id par exemple

def get_info_all_moniteur(id,nom,prenom,naissance,telephone,adresseEmail):
    res = Moniteur.query
    if(id!= "" and id != "0"):
        res = res.filter(Moniteur.id == id)
    if(nom!= ""):
        print(res)
        res = res.filter(Moniteur.personne.has(Personne.nomp == nom))

    if(prenom!= ""):
        res = res.filter(Moniteur.personne.has(Personne.prenomp == prenom))

    if(naissance!= ""):
        jour = naissance.split("/")[0]
        mois = naissance.split("/")[1]
        annee = naissance.split("/")[2]
        date = datetime.date(int(annee),int(mois),int(jour))
        res = res.filter(Moniteur.personne.has(Personne.ddn == date))
    if(adresseEmail!= ""):
            res = res.filter(Moniteur.personne.has(Personne.adressemail == adresseEmail))

    if(telephone!= ""):
        res = res.filter(Moniteur.personne.has(Personne.numerotel == telephone))
   
    return res

def get_info_all_clients(id,nom,prenom,naissance,telephone,adresseEmail,a_paye):
    res = Client.query
    if(id!= "" and id != "0"):
        res = res.filter(Client.id == id)
    if(nom!= ""):
        res = res.filter(Client.personne.has(Personne.nomp == nom))

    if(prenom!= ""):
        res = res.filter(Client.personne.has(Personne.prenomp == prenom))

    if(naissance!= ""):
        jour = naissance.split("/")[0]
        mois = naissance.split("/")[1]
        annee = naissance.split("/")[2]
        date = datetime.date(int(annee),int(mois),int(jour))
        res = res.filter(Client.personne.has(Personne.ddn == date))
    if(adresseEmail!= ""):
            res = res.filter(Client.personne.has(Personne.adressemail == adresseEmail))

    if(telephone!= ""):
        res = res.filter(Client.personne.has(Personne.numerotel == telephone))
        
    if(a_paye != ""):
        if(a_paye == "Oui"):
            res = res.filter(Client.cotisationa == True)

        else:
            res = res.filter(Client.cotisationa == False)
    return res


def get_info_all_personnes(id,nom,prenom,naissance,adresseEmail,telephone):
    res = Personne.query
    if(id!= "" and id != "0"):
        res = res.filter(Personne.id == id)
    if(nom!= ""):
        res = res.filter(Personne.nomp == nom)

    if(prenom!= ""):
        res = res.filter(Personne.prenomp == prenom)

    if(naissance!= ""):
        jour = naissance.split("/")[0]
        mois = naissance.split("/")[1]
        annee = naissance.split("/")[2]
        date = datetime.date(int(annee),int(mois),int(jour))
        print(date)
        res = res.filter(Personne.ddn == date).all()
        print(res)
    if(adresseEmail!= ""):
            res = res.filter(Personne.adressemail == adresseEmail)

    if(telephone!= ""):
        res = res.filter(Personne.numerotel == telephone)
    return res

def get_info_all_poney(id,nom,poids):
    res = Poney.query
    print(nom)
    if(id != ""and id != "0"):
        res = res.filter(Poney.idpo == id)
        print(res)
    if(nom != ""):
        
        res = res.filter(Poney.nomp == nom)
    if(poids != "" and poids != "0"):
        res = res.filter(Poney.poidssup > poids)
    return res
def get_info_all_cours(idc,nomc,type,prix,nomMoniteur):
    res = Cours.query
    if(idc != ""  and idc != "0"):
        res = res.filter(Cours.idc == idc)
    if(nomc != ""):
        res = res.filter(Cours.nomc == nomc)

    if(type != ""):
        res = res.filter(Cours.typec == type)

    if(prix != ""):
        res = res.filter(Cours.prix == prix)

    if(nomMoniteur != ""):   
        res = res.filter(Cours.moniteur.personne.nomp == nomMoniteur)
    return res
def get_info_all_reservations(dateReservation,idp,idc,idpo,duree,a_cotise):
    res = Reserver.query
    if(dateReservation != ""):
        
        date = dateReservation.split(' ')[0]
        temps = dateReservation.split(' ')[1]
        jour = date.split("/")[0]
        mois = date.split("/")[1]
        annee = date.split("/")[2]
        heure = temps.split(":")[0]
        minute = temps.split(":")[1]
        seconde = 0 
        datetime1 = datetime.datetime(int(annee),int(mois),int(jour),int(heure),int(minute),int(seconde))
        res =  res.filter(Reserver.cours.has(Cours.jmahms == datetime1))
        
    if(idp != ""):
        res =  res.filter(Reserver.id == idp)
   
    if(idc != ""):
        res =   res.filter(Reserver.idc == idc)
    if(idpo != ""):
        
        res =   res.filter(Reserver.idpo == idpo)
    if(duree != ""):
        res =  res.filter(Reserver.duree == duree)
    if(a_cotise != ""):
        if(a_cotise == "Oui"):
            res  =  res.filter(Reserver.a_paye == True)
        else: 
            res =  res.filter(Reserver.a_paye == False)

    return res.all()


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
def update_client(id, cotisation):
    c = Client.query.get(id)
    c.cotisation = cotisation
    try : 
        db.session.commit()
        return True
    except : 
        db.session.rollback()
        return False
    
def update_reservation(jmahms,id,idc,est_paye):
    
    date = jmahms.split(' ')[0]
    temps = jmahms.split(' ')[1]
    jour = date.split("/")[0]
    mois = date.split("/")[1]
    annee = date.split("/")[2]
    heure = temps.split(":")[0]
    minute = temps.split(":")[1]
    seconde = 0 
    datetime1 = datetime.datetime(int(annee),int(mois),int(jour),int(heure),int(minute),int(seconde))
  
    reservation = Reserver.query.filter(Reserver.idc == idc and Reserver.id == id and Reserver.cours.has(Cours.jmahms == datetime1)).first()
    reservation.a_paye = True if est_paye == "true" else False
    try : 
        db.session.commit()
        
        return True
    except Exception as e : 
        db.session.rollback()
        print(e)
        return False
    
def isAdmin(id):
    a = Admin.query.get(id)
    return a != None

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
    reservation = Reserver.query.filter(Reserver.cours.has(Cours.jmahms == jmahms)).filter(Reserver.id == id).filter(Reserver.idpo == idpo).first()
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
    print(cours)
    db.session.delete(cours)
    try:
        db.session.commit()
        return True

    except Exception as e:
        print(e)
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
    if moniteur is not None:
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
def modifier_Personne(personne):
    p = Personne.query.get(personne.id)
    p.adressemail = personne.adressemail
    p.prenomp =  personne.prenomp
    p.nomp =  personne.nomp
    p.ddn =  datetime.datetime(int(personne.ddn.split("/")[2]),int(personne.ddn.split("/")[1]),int(personne.ddn.split("/")[0]))
    p.poids =  personne.poids
    p.code_postal =  personne.code_postal
    p.adresse =  personne.adresse
    p.ville =  personne.ville
    p.numerotel =  personne.numerotel
    p.mdp =  personne.mdp
    try :
        db.session.commit()
        return True
    except Exception as e: 
        print(e)
        db.session.rollback()
        return False

def modifier_poney(poney):
    po = Poney.query.get(poney.idpo)
    po.nomp = poney.nomp
    po.poidssup = poney.poidssup
    po.url_image = poney.url_image
    try :
        db.session.commit()
        return True
    except Exception as e: 
        print(e)
        db.session.rollback()
        return False

def modifier_cours(cours):
    c = Cours.query.get(cours.idc)
    c.nomc = cours.nomc
    c.descc = cours.descc
    c.typec = cours.typec
    c.prix = cours.prix
    try :
        db.session.commit()
        return True
    except Exception as e: 
        print(e)
        db.session.rollback()
        return False

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

def ajout_poney(nom,poids,url):
    """
    Il ajoute un poney à la base de données
    
    :param nom: chaîne de caractères
    :param poids: float
    """
    idpo = get_max_id_poney() + 1
    poney = Poney(idpo,nom,poids,url)
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


def ajouteCours(nomc, descc, typec, prix,jmahms,duree,id,url):
    """
    Il ajoute un nouveau cours à la base de données
    
    :param nomc: chaîne de caractères
    :param descc: chaîne de caractères
    :param typec: chaîne de caractères
    :param prix: float
    :return: une valeur booléenne.
    """
    liste_datetime = jmahms.split(" ")
    liste = liste_datetime[0].split("/")
    liste_time = liste_datetime[1].split(":")
    date_cours = datetime.datetime(int(liste[2]),int(liste[1]),int(liste[0]),int(liste_time[0]),int(liste_time[1]),0)
    cours = Cours(get_max_id_cours()+1, nomc, descc, typec, prix,duree,date_cours, id,url)
    db.session.add(cours)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
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
    
