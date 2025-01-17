"""
    Fichier qui regroupe la connexion ainsi que les reqûetes en SQLAlchemy.
"""

import sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker,scoped_session
from .models import *
from secrets import token_urlsafe
from datetime import datetime, timedelta,date
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
    """
    Il renvoie un objet personne de la base de données, étant donné un identifiant
    
    :param id: L'identifiant de la personne que vous souhaitez obtenir
    :return: A Personne object
    """
    return Personne.query.get(int(id))

def get_cours(id):
    """
    Il prend un identifiant comme argument et renvoie un objet Cours avec cet identifiant
    
    :param id: L'identifiant du cours que vous souhaitez obtenir
    :return: Un seul objet Cours
    """
    return Cours.query.get(int(id))


def get_client(id):
    """
    Il renvoie un objet client de la base de données, étant donné l'identifiant du client
    
    :param id: L'identifiant du client à obtenir
    :return: Un objet Client
    """

    return Client.query.get(id)



def get_poney(id):
    """
    Il retourne un poney
    
    :param id: L'identifiant du poney que vous souhaitez obtenir
    :return: Un objet poney
    """
    return Poney.query.get(id)

def get_moniteur(id):
    """
    Il renvoie un objet moniteur de la base de données, étant donné l'identifiant du moniteur
    
    :param id: l'identifiant du moniteur
    :return: A Moniteur object
    """

    return Moniteur.query.get(id)

def place_libre(id):
    c = Cours.query.get(id)
    if(c.typec == "Collectif"):
        if(len(Reserver.query.filter(Reserver.idc == id).all()) == 10):
            return False
    else:
        if(len(Reserver.query.filter(Reserver.idc == id).all()) == 1):
            return False
    return True

def get_personne_email(email):
    """
    Il renvoie le premier objet personne dont l'adresse email est égale au paramètre email
    
    :param email: l'adresse e-mail de la personne que vous souhaitez obtenir
    :return: A Personne object
    """
    return Personne.query.filter(Personne.adressemail == email).first()

# des que l'on fait une jointure avec d'autre tables, on a soit pas les infos soit avec le add_columns des tuples et on peut plus faire ligne.id par exemple

def get_poneys_possible(cours,idpersonne):
    """
    Il renvoie une liste de poneys qui ne sont pas réservés pour un cours donné
    
    :param cours: le cours à réserver
    :param idpersonne: l'identifiant de la personne qui effectue la réservation
    :return: Une liste de poneys qui ne sont pas réservés pour la date et l'heure données.
    """
    personne = Personne.query.get(idpersonne)
    poneys = Poney.query.all()
    reservations = Reserver.query.all()
    for r in reservations:
        date_fin_plus_repos = r.cours.jmahms+timedelta(hours=3+r.cours.duree.hour)
        if r.cours.jmahms.date() == cours.jmahms.date() and r.cours.jmahms <= cours.jmahms <= date_fin_plus_repos:
            poneys.remove(r.poney)
    poneys2 = poneys.copy()
    for p in poneys:
        if p.poidssup<personne.poids:
            poneys2.remove(p)

    return poneys2

def get_info_all_moniteur(id,nom,prenom,naissance,telephone,adresseEmail):
    """
    Il prend un tas de chaînes, et si elles ne sont pas vides, il filtre la requête par eux
    
    :param id: entier
    :param nom: Chaîne
    :param prenom: "",
    :param naissance: "01/01/2000"
    :param telephone: "0"
    :param adresseEmail: "test@test.com"
    :return: Un objet de requête.
    """

    res = Moniteur.query
    if(id!= "" and id != "0"):
        res = res.filter(Moniteur.id == id)
    if(nom!= ""):
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
    """
    Il prend un tas de paramètres, puis les utilise pour filtrer une requête
    
    :param id: entier
    :param nom: Chaîne
    :param prenom: "",
    :param naissance: date de naissance
    :param telephone: "0"
    :param adresseEmail: "test@test.com"
    :param a_paye: une chaîne qui peut être "Oui" ou "Non"
    :return: Un objet requête
    """
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

def get_place(cours):
    """
    > Obtenir le nombre de places disponibles pour un cours donné
    
    :param cours: le cours
    :return: Le nombre de places disponibles pour un cours.
    """
    res = Reserver.query
    reservations = res.filter(Reserver.idc == cours.idc).all()
    
    if(cours.typec == "Individuel"):
        max = 1
    else:
        max=10
    return max-len(reservations)

def get_all_cours_a_reserver(id,typeActivite,dateR):
    """
    Il renvoie tous les cours qui ne sont pas réservés par l'utilisateur avec l'identifiant donné, et
    qui sont du type donné et qui sont postérieurs à la date donnée
    
    :param id: l'identifiant de l'utilisateur
    :param typeActivite: le type d'activité
    :param dateR: la date de la réservation
    :return: Une liste d'objets Cours
    """
    reservation = Reserver.query.filter(Reserver.id == id).all()
    res = Cours.query.filter(Cours.jmahms > datetime.now())
    if(typeActivite != ""):
        res = res.filter(Cours.typec == typeActivite)
    if(dateR != ""):
        jour = dateR.split("/")[0]
        mois = dateR.split("/")[1]
        annee = dateR.split("/")[2]
        date1 = date(int(annee),int(mois),int(jour))
        res = res.filter(Cours.jmahms > date1)
    cours = res.all()

    
    for r in reservation:
        if r.cours in cours:
            cours.remove(r.cours)
    return cours

def get_all_mes_reservations(id, typeActivite, dateReservation):
    """
    Il renvoie toutes les réservations d'un utilisateur, étant donné un type d'activité et une date
    
    :param id: l'identifiant de l'utilisateur
    :param typeActivite: le type d'activité (ex: "Yoga")
    :param date: une chaîne au format jj/mm/aaaa
    :return: Une liste d'objets Cours
    """

    reservation = Reserver.query.filter(Reserver.id == id).all()
    res = Cours.query.filter(Cours.jmahms > datetime.now())
    if(typeActivite != ""):
        res = res.filter(Cours.typec == typeActivite)
    if(dateReservation != ""):
        jour = dateReservation.split("/")[0]
        mois = dateReservation.split("/")[1]
        annee = dateReservation.split("/")[2]
        date1 = date(int(annee),int(mois),int(jour))
        res = res.filter(Cours.jmahms > date1)
    cours = res.all()
    mesReservation = []

    for r in reservation:
        if r.cours in cours:
            mesReservation.append(r.cours)
    return mesReservation
    
def get_info_all_personnes(id,nom,prenom,naissance,adresseEmail,telephone):
    """
    Il filtre la table Personne en fonction des paramètres qui lui sont transmis.
    
    :param id: "0"
    :param nom: "",
    :param prenom: "",
    :param naissance: "01/01/2000"
    :param adresseEmail: "test@test.com"
    :param telephone: "0"
    :return: Un objet de requête.
    """
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
        res = res.filter(Personne.ddn == date).all()
    if(adresseEmail!= ""):
            res = res.filter(Personne.adressemail == adresseEmail)

    if(telephone!= ""):
        res = res.filter(Personne.numerotel == telephone)
    return res

def get_info_all_poney(id,nom,poids):
    """
    Il prend trois paramètres et renvoie un objet de requête
    
    :param id: l'id du poney
    :param nom: le nom du poney
    :param poids: masse
    """
    res = Poney.query
    if(id != ""and id != "0"):
        res = res.filter(Poney.idpo == id)
    if(nom != ""):
        
        res = res.filter(Poney.nomp == nom)
    if(poids != "" and poids != "0"):
        res = res.filter(Poney.poidssup > poids)
    return res


def get_info_all_cours(idc,nomc,type,prix,nomMoniteur,jmahms,duree):
    """
    Cela prend un tas de paramètres, et s'ils ne sont pas vides, cela ajoute un filtre à la requête
    
    :param idc: l'identifiant du cours
    :param nomc: nom du cours
    :param type: type de cours
    :param prix: le prix du cours
    :param nomMoniteur: le nom de l'instructeur
    :param jmahms: "01/01/2020 00:00"
    :param duree: Durée du cours
    """
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
        
    if(jmahms != ""):
        date = jmahms.split(' ')[0]
        temps = jmahms.split(' ')[1]
        jour = date.split("/")[0]
        mois = date.split("/")[1]
        annee = date.split("/")[2]
        heure = temps.split(":")[0]
        minute = temps.split(":")[1]
        seconde = 0 
        datetime1 = datetime(int(annee),int(mois),int(jour),int(heure),int(minute),int(seconde))
        res =  res.filter(Cours.jmahms == datetime1)
    if(duree !=""):
        res =  res.filter(Cours.duree == duree)
    
    return res


def get_info_all_reservations(dateReservation,idp,idc,idpo,duree,a_cotise):
    """
    Il renvoie toutes les réservations qui correspondent aux critères donnés
    
    :param dateReservation: une chaîne au format "jj/mm/aaaa hh:mm"
    :param idp: identifiant de la personne qui a effectué la réservation
    :param idc: identifiant du client
    :param idpo: identifiant de la piscine
    :param duree: Durée du cours
    :param a_cotise: une valeur booléenne
    :return: Une liste d'objets Reserver.
    """
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
        datetime1 = datetime(int(annee),int(mois),int(jour),int(heure),int(minute),int(seconde))
        res =  res.filter(Reserver.cours.has(Cours.jmahms == datetime1))
        
    if(idp != ""):
        res =  res.filter(Reserver.id == idp)
   
    if(idc != ""):
        res =   res.filter(Reserver.idc == idc)
    if(idpo != ""):
        
        res =   res.filter(Reserver.idpo == idpo)
    if(duree != ""):
        res =  res.filter(Reserver.cours.has(Cours.duree == duree))
    if(a_cotise != ""):
        if(a_cotise == "Oui"):
            res  =  res.filter(Reserver.a_paye == True)
        else: 
            res =  res.filter(Reserver.a_paye == False)

    return res.all()


def get_moniteur(id):
    """
    Il renvoie le premier moniteur avec l'identifiant donné
    
    :param id: l'identifiant du moniteur
    :return: A Moniteur object
    """
    return Moniteur.query.filter(Moniteur.id == id).first()
def get_client(id):
    """
    Il renvoie le premier client avec l'identifiant donné.
    
    :param id: L'identifiant du client à obtenir
    :return: Un objet requête
    """
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
    except Exception as e:
        db.session.rollback()
        return repr(e)

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
    """
    Il met à jour la cotisation d'un client avec l'identifiant donné
    
    :param id: l'identifiant du client
    :param cotisation: la nouvelle valeur de cotisation
    :return: La valeur de retour est une représentation sous forme de chaîne de l'exception.
    """
    c = Client.query.get(id)
    c.cotisation = cotisation
    try : 
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return repr(e)
    

def update_reservation(id,idc,idpo,est_paye):
    """
    Il prend 3 paramètres et renvoie une valeur booléenne
    
    :param id: l'identifiant de la réservation
    :param idc: identifiant du client
    :param idpo: identifiant du poste
    :param est_paye: est une valeur booléenne
    :return: La valeur de retour est une représentation sous forme de chaîne de l'exception.
    """
    reservation = Reserver.query.filter(Reserver.id == id and Reserver.idc == idc and Reserver.idpo == idpo).first()
    reservation.a_paye = True if est_paye == "true" else False
    try : 
        db.session.commit()
        
        return True
    except Exception as e:
        db.session.rollback()
        return repr(e)
    
def isAdmin(id):
    """
    Si l'utilisateur est un administrateur, renvoie True, sinon renvoie False
    
    :param id: L'identifiant de l'utilisateur
    :return: La valeur de retour est un booléen.
    """
    a = Admin.query.get(id)
    return a != None

def deletereservation(idc,id):
    """
    Il prend une date, un id et un idpo et supprime la réservation qui correspond à la date, l'id et
    l'idpo
    
    :param date: "01/01/2020 00:00:00"
    :param id: l'identifiant de l'utilisateur
    :param idpo: l'identifiant de l'utilisateur qui a effectué la réservation
    :return: une valeur booléenne.
    """
    reservation = Reserver.query.get((id,idc))
    db.session.delete(reservation)
    try : 
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return repr(e)

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

    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
    
    
def delete_personne(id):
    """
    Si la personne est un client, supprimez le client, si la personne est un moniteur, supprimez tous
    les cours qu'il enseigne, puis supprimez le moniteur, puis supprimez la personne
    
    :param id: l'id de la personne à supprimer
    :return: La valeur de retour est une représentation sous forme de chaîne de l'exception.
    """
    print(id)
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
    except Exception as e:
        
        db.session.rollback()
        return repr(e)

    

def get_max_id_personne():
    """
    Elle renvoie la valeur maximale de la colonne id de la table Personne
    :return: La valeur maximale de l'identifiant dans la table Personne.
    """
    return db.session.query(func.max(Personne.id)).first()[0]

def get_max_id_cours():
    """
    Elle renvoie la valeur maximale de la colonne idc de la table Cours
    :return: La valeur idc maximale dans la table Cours.
    """
    return db.session.query(func.max(Cours.idc)).first()[0]
def get_max_id_poney():
    """
    Il renvoie l'identifiant maximum de la table Poney
    :return: L'identifiant maximum de la table Poney.
    """
    return db.session.query(func.max(Poney.idpo)).first()[0]
def modifier_Personne(personne):
    """
    Il prend un objet personne, trouve la personne dans la base de données et met à jour la base de
    données avec les nouvelles valeurs
    
    :param personne: 
    :return: La valeur de retour est une représentation sous forme de chaîne de l'exception.
    """
    p = Personne.query.get(personne.id)
    p.adressemail = personne.adressemail
    p.prenomp =  personne.prenomp
    p.nomp =  personne.nomp
    p.ddn =  datetime(int(personne.ddn.split("/")[2]),int(personne.ddn.split("/")[1]),int(personne.ddn.split("/")[0]))
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
        
        db.session.rollback()
        return repr(e)

def modifier_poney(poney):
    """
    Il prend un objet Poney comme argument, obtient l'objet Poney de la base de données avec le même
    identifiant, puis met à jour l'objet de base de données avec les valeurs de l'argument
    
    :param poney: l'objet qui contient les données à modifier
    :return: La valeur de retour est une représentation sous forme de chaîne de l'objet exception.
    """
    po = Poney.query.get(poney.idpo)
    po.nomp = poney.nomp
    po.poidssup = poney.poidssup
    po.url_image = poney.url_image
    try :
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)

def modifier_cours(cours):
    """
    Il prend un objet Cours comme argument et met à jour la base de données avec les nouvelles valeurs
    
    :param cours: l'objet qui contient les nouvelles données
    """
    c = Cours.query.get(cours.idc)
    c.nomc = cours.nomc
    c.descc = cours.descc
    c.typec = cours.typec
    c.prix = cours.prix
    c.jmahms = cours.jmahms
    c.duree = cours.duree
    c.url_image = cours.url_image
    try :
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)

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
    except Exception as e:
        
        db.session.rollback()
        return repr(e)

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
    except Exception as e:
        
        db.session.rollback()
        return repr(e)

def ajout_reservation(id,idpo,idc,a_paye):
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

    reservation = Reserver(id,idc,idpo,a_paye)
    db.session.add(reservation)
    try:
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)


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
    date_cours = datetime(int(liste[2]),int(liste[1]),int(liste[0]),int(liste_time[0]),int(liste_time[1]),0)
    cours = Cours(get_max_id_cours()+1, nomc, descc, typec, prix,duree,date_cours, id,url)
    db.session.add(cours)
    try:
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
       


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
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
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
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
    
def ajoute_personne(nomp, prenomp, ddn, poids, adressemail, adresse, code_postal, ville, numerotel) : 
    """
    Il ajoute une nouvelle personne à la base de données
    
    :param nomp: nom de famille
    :param prenomp: chaîne
    :param ddn: date de naissance
    :param poids: masse
    :param adressemail: vachar(50)
    :param adresse: chaîne
    :param code_postal: '75000'
    :param ville: vachar(50)
    :param numerotel: +33 6 12 34 56 78
    :return: L'identifiant de la personne ajoutée à la base de données.
    """
    idp = get_max_id_personne() +1
    mdp = token_urlsafe(6)
    liste = ddn.split("/")
    date_naissance = date(int(liste[2]),int(liste[1]),int(liste[0]))
    personne = Personne(idp, nomp, prenomp, date_naissance, poids, adressemail, adresse, code_postal, ville, numerotel, mdp)
    db.session.add(personne)
    try :
        db.session.commit()
        return idp
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
