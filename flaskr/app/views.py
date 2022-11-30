from .app import app,login_manager
from .models import * 
from .ConnexionMySQL import *
from flask import render_template
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask import Flask,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


@login_manager.user_loader
def load_user(user_id):
    return get_personne(session,user_id)

@app.route("/")
@login_required
def index():
    if(get_moniteur(session,current_user.id)):
        return render_template("index.html",role="Moniteur")
    elif(get_client(session,current_user.id)):
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

@app.route('/api/dataclients')
def data_client():
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
    nom = request.form["nom"]
    poids = int(request.form["poids"])
    ajout_poney(session,nom,poids)
    return ""
@app.route('/AddReservation',methods=['POST'])
def AddReservation():
    jmahms = request.form["jmahms"]
    id = request.form["id"]
    idpo = request.form["idpo"]
    idc = request.form["idc"]
    duree = request.form["duree"]
    a_paye = request.form["a_paye"]
    ajout_reservation(session,jmahms,id,idpo,idc,duree,a_paye)
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
