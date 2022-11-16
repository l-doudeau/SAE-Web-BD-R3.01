from flask import Flask, render_template, request
from Client import  Client
from Personne import Personne
from ConnexionMySQL import ouvrir_connexion
from sqlalchemy.orm import sessionmaker

connexion ,engine = ouvrir_connexion("root","root","localhost", "GRAND_GALOP")
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'

@app.route('/')
def default():
    return render_template('gerer_client.html')
Session = sessionmaker(bind=engine)
DBSession = Session()


@app.route('/api/dataclients')
def data_client():
    data = {"data":[]}
    lignes =DBSession.query(Personne.idp,Personne.nomp,Personne.prenomp,Personne.ddn,Personne.adressemail,Personne.numerotel,Client.cotisationa).join(Client, Personne.idp == Client.idp)
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
    user = DBSession.query(Client).get(id)
    DBSession.delete(user)
    DBSession.commit()
    return ""
