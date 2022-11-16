from flask import Flask, render_template, request,redirect,url_for
from .ConnexionMySQL import get_personne,session,get_moniteur,get_client,get_personne_email,get_info_all_clients,deleteclient,ajout_client
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from secrets import token_urlsafe

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
        except(KeyError):
            return render_template("login.html",error="Email ou mot de passe incorrect")
    return render_template("login.html")


@app.route('/Clients')
@login_required
def clients():
    print(login_manager.login_message + "\n")
    return render_template('gerer_client.html')


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


@app.route('/DeleteClient',methods=['POST'])
def DeleteClient():
    new_freq = request.get_data()
    id_brute = new_freq.decode("utf-8")
    print(new_freq)
    id = id_brute.split("=")[1]
    deleteclient(session,id)
    return ""

@app.route('/AddClient',methods=['POST'])
def AddClient():
    new_freq = request.get_data()
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    ddn = request.form["date"]
    print(ddn)
    poids = int(request.form["poids"])
    adresseemail = request.form["adresseemail"]
    adresse = request.form["adresse"]
    code_postal = int(request.form["codepostal"])
    ville = request.form["ville"]
    numerotel = request.form["tel"]
    cotise = request.form["cotise"]
    ajout_client(session,prenom,nom,ddn,poids,adresseemail,adresse,code_postal,ville,numerotel,cotise)
    return ""
