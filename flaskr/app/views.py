"""
    Fichier qui regroupe les différentes routes du site web avec leur utilité
"""

from flask import Flask, render_template, request,redirect,url_for
from .ConnexionMySQL import get_personne,session,get_moniteur,get_client,get_personne_email,\
    get_info_all_clients,deleteclient,ajout_client,ajout_poney,deletePoney,get_info_all_poney,\
        get_info_all_cours,get_info_all_reservations,deletereservation,ajout_reservation,rollback, ajouteCours, deletecours,\
        ajoute_personne

from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from secrets import token_urlsafe
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = token_urlsafe(16) #Générer une clé au hasard

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return get_personne(session,user_id)

@app.route("/")
@login_required
def index():
    """
    Si l'utilisateur est un moniteur, retourner la page d'index avec le rôle "Moniteur", si
    l'utilisateur est un client, retourner la page d'index avec le rôle "Client", sinon retourner la
    page d'index sans rôle
    :return: La page d'index avec le rôle de l'utilisateur.
    """
    if(get_moniteur(session,current_user.id)):
        return render_template("index.html",role="Moniteur")
    elif(get_client(session,current_user.id)):
        return render_template("index.html",role="Client")
    else:
        return render_template("index.html",role="")
    
@app.route("/logout")
def logout():
    """
    Il déconnecte l'utilisateur et le redirige vers la page d'index
    :return: la fonction de redirection.
    """
    logout_user()
    return redirect(url_for("index"))


@app.route('/login',methods=["POST","GET"])
def login():
    """
    Si la méthode de demande est POST, essayez d'obtenir l'email et le mot de passe à partir du
    formulaire de demande, si l'utilisateur existe, vérifiez si le mot de passe est correct, si c'est le
    cas, connectez l'utilisateur et redirigez vers la page d'index, sinon, revenez un message d'erreur
    :return: Une fonction qui ne prend aucun argument et renvoie une chaîne.
    """
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            user = get_personne_email(session, email)
            if user:
                if user.mdp == password:
                    login_user(user)
                    if(request.args.get("next")):
                        print(request.args.get("next"))
                        return redirect(request.args.get("next"))
                    return redirect(url_for("index"))
                else:
                    return render_template("login.html",error="Email ou mot de passe incorrect")
            else:
                return render_template("login.html",error="Email ou mot de passe incorrect")
        except(KeyError):
            print("salut")
            return render_template("login.html",error="Email ou mot de passe incorrect")
    return render_template("login.html")


@app.route('/Clients')
@login_required
def Clients():
    print(login_manager.login_message + "\n")
    return render_template('gerer_client.html')

@app.route('/Poneys')
@login_required
def Poneys():
    print(login_manager.login_message + "\n")
    return render_template('gerer_poneys.html')
@app.route('/Reservations')
@login_required
def Reservations():
    return render_template("gerer_reservations.html")

@app.route('/Cours')
@login_required
def Cours():
    return render_template('gerer_cours.html')

@app.route('/api/dataclients')
def data_client():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    lignes = get_info_all_clients(session)
    for ligne in lignes:

        data["data"].append({
            "idp": ligne[0],
            "nomp":ligne[1],
            "prenomp":ligne[2],
            "ddn":ligne[3],
            "adressemail":ligne[4],
            "numerotel":ligne[5],
            "cotisation":ligne[6]
        })
    return data

@app.route('/api/dataponeys')
def data_poneys():
    """
    Il renvoie un dictionnaire avec une seule clé, "data", dont la valeur est une liste de
    dictionnaires, chacun ayant trois clés, "idpo", "nomp" et "poidssup"
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    lignes = get_info_all_poney(session)
    for ligne in lignes:
        data["data"].append({
            "idpo": ligne.idpo,
            "nomp":ligne.nomp,
            "poidssup":ligne.poidssup
        })
    return data


@app.route('/api/datacours')
def data_cours():
    """
    Il renvoie un dictionnaire avec une clé "data" qui contient une liste de dictionnaires, chacun ayant
    les clés "idc", "nomc", "descc", "typec" et "prix"
    :return: Un dictionnaire avec une clé de données et une valeur d'une liste vide.
    """
    data = {"data":[]}
    lignes = get_info_all_cours(session)
    for ligne in lignes:
        data["data"].append({
            "idc": ligne.idc,
            "nomc":ligne.nomc,
            "descc":ligne.descc,
            "typec": ligne.typec,
            "prix": ligne.prix,
        })
    return data

    
@app.route('/api/datareservation',methods=["POST","GET"])
def data_reservations():
    """
    Il renvoie un dictionnaire avec une clé "data" qui contient une liste de dictionnaires. Chaque
    dictionnaire de la liste a les clés "jmahms", "id", "idpo", "nomp", "prenomp", "nomc", "nompo",
    "duree" et "a_paye"
    :return: Un dictionnaire avec une clé de "données" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    lignes = get_info_all_reservations(session)
    for ligne in lignes:
        data["data"].append({
            "jmahms": ligne.jmahms,
            "id":ligne.id,
            "idpo":ligne.idpo,
            "nomp":ligne.nomp,
            "prenomp":ligne.prenomp,
            "nomc": ligne.nomc,
            "nompo": ligne.nomp,
            "duree": str(ligne.duree),
            "a_paye": ligne.a_paye
        })
    return data



@app.route('/Client/<id>',methods=['POST',"GET"])
def Client(id):
    return render_template("index.html",id=id)#TODO

@app.route('/Poney/<id>',methods=['POST',"GET"])
def Poney(id):
    return render_template("index.html",id=id)#TODO
@app.route('/Reservation/<jmahms><id><idpo>',methods=['POST',"GET"])
def Reservation(jmahms,id,idpo):
    return render_template("index.html",id=id)#TODO


@app.route('/AddClient',methods=['POST'])
def AddClient():
    """
    Il prend les données de formulaire de la page html et les insère dans la base de données
    :return: Rien.
    """
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    ddn = request.form["date"]
    poids = int(request.form["poids"])
    adresseemail = request.form["adresseemail"]
    adresse = request.form["adresse"]
    code_postal = int(request.form["codepostal"])
    ville = request.form["ville"]
    numerotel = request.form["tel"]
    cotise = request.form["cotise"]
    ajout_client(session,prenom,nom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel,cotise)
    return ""

@app.route('/AddPoney',methods=['POST'])
def AddPoney():
    """
    Il ajoute un poney à la base de données
    :return: Rien.
    """
    nom = request.form["nom"]
    poids = int(request.form["poids"])
    ajout_poney(session,nom,poids)
    return ""

@app.route('/AddReservation',methods=['POST'])
def AddReservation():
    """
    Il prend les données du formulaire et les passe à la fonction ajout_reservation() qui est définie
    dans le fichier ajout_reservation.py
    :return: Rien.
    """
    jmahms = request.form["jmahms"]
    id = request.form["id"]
    idpo = request.form["idpo"]
    idc = request.form["idc"]
    duree = request.form["duree"]
    a_paye = request.form["a_paye"]
    ajout_reservation(session,jmahms,id,idpo,idc,duree,a_paye)
    return ""

@app.route('/AddCours',methods=['POST'])
def AddCours():
    """
    Il prend les données du formulaire de la requête, et les passe à la fonction ajouteCours
    :return: Rien.
    """
    nom = request.form["nom"]
    descc = request.form["descc"]
    prix = request.form["prix"]
    type = request.form["type"]
    ajouteCours(session, nom, descc, prix, type)
    return ""


@app.route('/AddPersonne',methods=['POST'])
def AddCours():
    """
    Il prend les données du formulaire de la requête, et les passe à la fonction ajoutePersonne
    :return: Rien.
    """
    nom = request.form["nom"]
    descc = request.form["descc"]
    prix = request.form["prix"]
    type = request.form["type"]
    ajoute_personne(session, nom, descc, prix, type)
    return ""


@app.route('/DeletePoney',methods=['POST'])
def DeletePoney():
    deletePoney(session,int(request.form["id"]))
    return ""

@app.route('/DeleteClient',methods=['POST'])
def DeleteClient():
    new_freq = request.get_data()
    id_brute = new_freq.decode("utf-8")
    id = id_brute.split("=")[1]
    deleteclient(session,id)
    return ""

@app.route('/DeleteReservation',methods=['POST'])
def DeleteReservation():
    deletereservation(session,request.form["jmahms"],request.form["id"],request.form["idpo"])
    return ""

@app.route('/deleteCours',methods=['POST'])
def deleteCours():
    deletecours(session,request.form["id"])
    return ""