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
    Personne = []
    Cours = []
    Poneys = []
    for p in get_info_all_personnes("","","","","",""):
        Personne.append(str(p.id) + " " + p.nomp + " " + p.prenomp)
    for c in get_info_all_cours("","","","",""):
        Cours.append(str(c.idc) + " " + c.nomc)
    for po in get_info_all_poney("","",""):
        Poneys.append(str(po.idpo)+ " " + po.nomp )
    return render_template("gerer_reservations.html",Personnes = Personne, cours = Cours, poneys = Poneys)

@app.route('/api/dataclients',methods=["POST"])
def data_client():
    data = {"data":[]}
    
    id = request.form["id"]
    naissance = request.form["naissance"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    prenom = request.form["prenom"]
    telephone = request.form["telephone"]
    a_paye = request.form["a_paye"]
    clients = get_info_all_clients(id,nom,prenom,naissance,telephone,adresseEmail,a_paye)
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

@app.route('/api/dataponeys',methods = ["POST"])
def data_poneys():
    data = {"data":[]}
    id = request.form["id"]
    nom = request.form["nom"]
    poids  = request.form["poids"]
    lignes = get_info_all_poney(id,nom,poids)

    for ligne in lignes:
        data["data"].append({
            "idpo": ligne.idpo,
            "nomp":ligne.nomp,
            "poidssup":ligne.poidssup
        })
    return data


@app.route('/api/datacours',methods=["POST"])
def data_cours():
    data = {"data":[]}
    print(request.form)
    idc = request.form["idc"]
    nomc = request.form["nomc"]
    type = request.form["typec"]
    prix = request.form["prix"]
    nomMoniteur = request.form["nomMoniteur"]
    
    lignes = get_info_all_cours(idc,nomc,type,prix,nomMoniteur)

    for ligne in lignes:
        data["data"].append({
            "idc": ligne.idc,
            "nomc":ligne.nomc,
            "descc":ligne.descc,
            "typec": ligne.typec,
            "prix": ligne.prix,
            "id" : ligne.moniteur.personne.nomp
        })
    return data

@app.route('/api/datamoniteurs',methods=["POST"])
def data_moniteurs():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    id = request.form["id"]
    naissance = request.form["naissance"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    prenom = request.form["prenom"]
    telephone = request.form["telephone"]
    lignes = get_info_all_moniteur(id,nom,prenom,naissance,telephone,adresseEmail)
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

    
@app.route('/api/datareservation',methods=["POST"])
def data_reservations():
    data = {"data":[]}
    jmahms = request.form["jmahms"]
    id = request.form["id"]
    idpo = request.form["idpo"]
    idc = request.form["idc"]
    duree = request.form["duree"]
    a_paye = request.form["a_paye"]


    lignes = get_info_all_reservations(jmahms,id,idc,idpo,duree,a_paye)
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

@app.route('/api/datapersonnes',methods=["POST"])
def data_personne():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = {"data":[]}
    id = request.form["id"]
    naissance = request.form["naissance"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    prenom = request.form["prenom"]
    telephone = request.form["telephone"]
    personnes = get_info_all_personnes(id,nom,prenom,naissance,adresseEmail,telephone)
    roleFiltre = request.form["role"]
    
    for personne in personnes:
        if get_moniteur(personne.id) is not None and  get_client(personne.id) is not None: 
            role = "Moniteur Client" 
        elif get_moniteur(personne.id) is not None:
            role = "Moniteur" 
        elif get_client(personne.id) is not None:
            role = "Client"
        else :
            role = ""
        if(roleFiltre == "" or roleFiltre in role):
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

@app.route('/api/datapersonnescombobox')
def data_personneCombo():
    """
    Il prend une liste de tuples et renvoie un dictionnaire avec une liste de dictionnaires
    :return: Un dictionnaire avec une clé "data" et une valeur d'une liste de dictionnaires.
    """
    data = []
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
        data.append(str(personne.id) + " " + personne.nomp + " " + personne.prenomp)
        
    return data

@login_required
@app.route('/Personne/<id>',methods=['POST',"GET"])
def PersonneDetail(id):
    return render_template("personneDetail.html",Personne = get_personne(id))

@login_required
@app.route('/Poney/<id>',methods=['POST',"GET"])
def PoneyDetail(id):
    return render_template("poneyDetails.html",id=id)

@login_required
@app.route("/Cours/<id>",methods=["POST","GET"])
def CoursDetails(id):
    Moniteurs = []
    if(request.method == "POST"):
        idm = request.form["id"]
    else:
        idm = get_cours(id).moniteur.id
        
    for moniteur in get_info_all_moniteur("","","","","",""):
        Moniteurs.append(str(moniteur.id) + " " + moniteur.personne.nomp + " " + moniteur.personne.prenomp)
    print(get_moniteur(idm))
    return render_template("CoursDetails.html",Cours = get_cours(id),Moniteurs = Moniteurs,Moniteur = get_moniteur(idm))

@login_required
@app.route('/Reservation/<jmahms><id><idpo>',methods=['POST',"GET"])
def ReservationDetail(jmahms,id,idpo):
    return render_template("index.html",id=id)#TODO



@login_required
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


@app.route("/Cours/Update",methods=["POST"])
def UpdateCours():
    descc = request.form["descc"]
    idmoniteur = request.form["idmoniteur"]
    nomc = request.form["nomc"]
    idc = request.form["idc"]
    type = request.form["type"]
    prix = request.form["prix"]
    c = Cours(idc,nomc,descc,type,prix,idmoniteur)
    save = modifier_cours(c)
    return "true" if save else "false"

@app.route('/Personne/Update',methods=['POST'])
def UpdatePersonne():
    id = request.form["id"]
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    email = request.form["email"]
    ddn = request.form["ddn"]
    poids = int(request.form["poids"])
    adresse = request.form["adresse"]
    code_postal = int(request.form["code_postal"])
    ville = request.form["ville"]
    tel = request.form["tel"]
    password = request.form["password"]
    p = Personne(id,nom,prenom,ddn,poids,email,adresse,code_postal,ville,tel,password)
    save = modifier_Personne(p)
    return "true" if save else "false"

@app.route('/Client/Update',methods=['POST'])
def UpdateClient():
    id = request.form["id"]
    cotisation = request.form["cotisation"]
    save = update_client(id,cotisation)
    return "true" if save else "false"

@app.route("/Reservation/Update",methods=["POST"])
def UpdateReservation():
    id = request.form["id"]
    jmahms = request.form["jmahms"]
    idpo = request.form["idpo"]
    est_paye = request.form["est_paye"]
    save = update_reservation(jmahms,id,idpo,est_paye)
    return "true" if save else "false"


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