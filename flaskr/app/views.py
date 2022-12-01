from .app import app,login_manager
from .models import * 
from .ConnexionMySQL import *
from flask import render_template
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask import Flask,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


@login_manager.user_loader
def load_user(user_id):
    return get_personne(user_id)

@app.route("/")
@login_required
def index():
    if(get_moniteur(current_user.id)):
        return render_template("index.html",role="Moniteur")
    elif(get_client(current_user.id)):
        return render_template("index.html",role="Client")
    else:
        return render_template("index.html",role="")
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/TEST")
def test():
    return render_template("accueil.html")

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            user = get_personne_email(email)
            print(user)
            if user:
                if user.mdp == password:
                    login_user(user)
                    print(user)
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
    return render_template('gerer_client.html')

@app.route('/Moniteurs')
@login_required
def Moniteurs():
    print(login_manager.login_message + "\n")
    return render_template('gerer_moniteur.html')

@app.route('/Cours')
@login_required
def cours():
    return render_template('gerer_cours.html')

@app.route('/Poneys')
@login_required
def Poneys():
    print(login_manager.login_message + "\n")
    return render_template('gerer_poneys.html')

@app.route('/Personnes')
@login_required
def Personnes():
    return render_template('gerer_personne.html')


@app.route('/Reservations')
@login_required
def Reservations():
    return render_template("gerer_reservations.html")

@app.route('/api/dataclients')
def data_client():
    data = {"data":[]}
    clients = get_info_all_clients()
    for client in clients:

        data["data"].append({
            "idp": client.id,
            "nomp":client.personne.nomp,
            "prenomp":client.personne.prenomp,
            "ddn":client.personne.ddn,
            "adressemail":client.personne.adressemail,
            "numerotel":client.personne.numerotel,
            "cotisation":client.cotisationa
        })
    return data

@app.route('/api/dataponeys')
def data_poneys():
    data = {"data":[]}
    lignes = get_info_all_poney()
    for ligne in lignes:
        data["data"].append({
            "idpo": ligne.idpo,
            "nomp":ligne.nomp,
            "poidssup":ligne.poidssup
        })
    return data


@app.route('/api/datacours')
def data_cours():
    data = {"data":[]}
    lignes = get_info_all_cours()
    for ligne in lignes:
        data["data"].append({
            "idc": ligne.idc,
            "nomc":ligne.nomc,
            "descc":ligne.descc,
            "typec": ligne.typec,
            "prix": ligne.prix,
            "id" : ligne.id
        })
    return data

@app.route('/api/datamoniteurs')
def data_moniteurs():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    lignes = get_info_all_moniteur()
    for ligne in lignes:
        data["data"].append({
            "idp": ligne.id,
            "nomp":ligne.personne.nomp,
            "prenomp":ligne.personne.prenomp,
            "ddn":ligne.personne.ddn,
            "adressemail":ligne.personne.adressemail,
            "numerotel":ligne.personne.numerotel,
        })
    return data

    
@app.route('/api/datareservation',methods=["POST","GET"])
def data_reservations():
    data = {"data":[]}
    lignes = get_info_all_reservations()
    for ligne in lignes:
        data["data"].append({
            "jmahms": ligne.jmahms,
            "id":ligne.id,
            "idpo":ligne.idpo,
            "nomp":ligne.personne.nomp,
            "prenomp":ligne.personne.prenomp,
            "nomc": ligne.cours.nomc,
            "nompo": ligne.poney.nomp,
            "duree": str(ligne.duree),
            "a_paye": ligne.a_paye
        })
    return data

@app.route('/api/datapersonnes')
def data_personne():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    personnes = get_info_all_personnes()
    for personne in personnes:
        if get_moniteur(personne.id) is not None : 
            role = "Moniteur" 
            if get_client(personne.id) is not None:
                role  +=  " Client"
        elif get_client(personne.id) is not None:
            role = "Client"
        else :
            role = ""

        data["data"].append({
            "idp": personne.id,
            "nomp":personne.nomp,
            "prenomp":personne.prenomp,
            "ddn":personne.ddn,
            "adressemail":personne.adressemail,
            "numerotel":personne.numerotel,
            "est": role
        })
    return data



@app.route('/Client/<id>',methods=['POST',"GET"])
def Client(id):
    return render_template("index.html",id=id)#TODO

@app.route('/Personne/<id>',methods=['POST',"GET"])
def Personne(id):
    return render_template("index.html",id=id)#TODO

@app.route('/Poney/<id>',methods=['POST',"GET"])
def Poney(id):
    return render_template("index.html",id=id)#TODO
@app.route('/Reservation/<jmahms><id><idpo>',methods=['POST',"GET"])
def Reservation(jmahms,id,idpo):
    return render_template("index.html",id=id)#TODO

@app.route('/Moniteur/<id>',methods=['POST',"GET"])
def Moniteur(id):
    return render_template("index.html",id=id)#TODO


@app.route('/AddClient',methods=['POST'])
def AddClient():
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
    id = ajoute_personne(nom,prenom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel)
    ajout_client(id,cotise)
    return ""

@app.route('/AddPoney',methods=['POST'])
def AddPoney():
    nom = request.form["nom"]
    poids = int(request.form["poids"])
    ajout_poney(nom,poids)
    return ""
@app.route('/AddReservation',methods=['POST'])
def AddReservation():
    jmahms = request.form["datepicker"]
    id = request.form["id"]
    idpo = request.form["idpo"]
    idc = request.form["idc"]
    duree = request.form["duree"]
    a_paye = request.form["a_paye"]
    ajout_reservation(jmahms,id,idpo,idc,duree,a_paye)
    return ""

@app.route('/DeletePoney',methods=['POST'])
def DeletePoney():
    deletePoney(int(request.form["id"]))
    return ""
@app.route('/DeleteClient',methods=['POST'])
def DeleteClient():
    new_freq = request.get_data()
    id_brute = new_freq.decode("utf-8")
    id = id_brute.split("=")[1]
    deleteclient(id)
    return ""

@app.route('/DeleteReservation',methods=['POST'])
def DeleteReservation():
    deletereservation(request.form["jmahms"],request.form["id"],request.form["idpo"])
    return ""

@app.route('/AddMoniteur',methods=['POST'])
def AddMoniteur():
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

    id = ajoute_personne(prenom, nom, ddn, poids, adresseemail, adresse, code_postal, ville, numerotel)
    ajoute_moniteur(id)
    return ""

@app.route('/AddCours',methods=['POST'])
def AddCours():
    """
    Il prend les données du formulaire de la requête, et les passe à la fonction ajouteCours
    :return: Rien.
    """
    nom = request.form["nom"]
    descc = request.form["descc"]
    type = request.form["type"]
    prix = request.form["prix"]
    id = request.form["id"]
    if type == "1" : 
        type = "Individuel"
    elif type == "2":
        type = "Collectif"
    ajouteCours(nom, descc, type, prix, id)
    return ""

@app.route('/AddPersonne',methods=['POST'])
def AddPersonne():
    """
    Il prend les données du formulaire de la requête, et les passe à la fonction ajoutePersonne
    :return: Rien.
    """
    nomp = request.form["nom"]
    prenomp = request.form["prenom"]
    ddn = request.form["datepicker"]
    poids = request.form["poids"]
    adressemail = request.form["adresseemail"]
    adresse = request.form["adresse"]
    code_postal = request.form["codepostal"]
    ville = request.form["ville"]
    numerotel = request.form["tel"]
    est_client = request.form["est_client"]
    est_moniteur = request.form["est_moniteur"]
    
    id = ajoute_personne( nomp, prenomp, ddn, poids, adressemail, adresse, code_postal, ville, numerotel)
    if est_client == "true" : 
        ajout_client(id, False)
    if est_moniteur == "true" :
        ajoute_moniteur(id)   
         
    return ""

@app.route('/DeleteMoniteur', methods=['POST'])
def DeleteMoniteur():
    id = int(request.form["id"])
    delete_moniteur(id)
    return ""   

@app.route('/deleteCours',methods=['POST'])
def deleteCours():
    deletecours(request.form["id"])
    return ""

@app.route('/deletePersonne',methods=['POST'])
def deletePersonne():
    delete_personne(request.form["id"])
    return ""