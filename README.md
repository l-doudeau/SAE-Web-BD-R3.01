# SAE-Web-BD-R3.01
## DE NARDI Lenny 23A
## DOUDEAU Luis 23A
## FAUCHER Thomas 23A

Pré-requis pour faire fonctionner ce projet :

Ce qu'il est requis pour commencer le projet :

    Installation de java
    Installation de MySQL Server/Client
    
    
Installation des différent composites necessaire au fonctionnement de l'application :

    1/ Ouvrez un terminale sur votre machine et entrer la commande suivante : 'sudo apt install default-jdk'
    2/ sudo apt install mysql-server
    3/ sudo systemctl start mysql.service
    4/ pip install flask
    5/ pip3 install mysql-connector-python
    6/ pip install flask_login
    7/ pip install flask_sqlalchemy
    8/ pip install pymysql
    
Lancer le projet :

    1/ Placer vous dans le repertoire 'scripts' qui se trouve dans le dossier DEVELOPMENT à la racine du projet : 
    chemin : /DEVELOPMENT/scripts
    2/ Entrer la commande suivante : 'sudo mysql -u votre_nom_user -p' ou 'mysql -h servinfo-mariadb -u votre_user -p'
    3/ Entre le mot de passe de votre machine ou 'root'
    4/ Une fois connecter sur MySQL, entrer les commandes suivante : 
      4A/ D'abord : 'source creaPon.sql'
      4B/ Enfin :   'source insPon.sql'
    6/ Ouvrez le fichier ExePonney.java qui se trouve dans le repertoire /DEVELOPMENT/src
    7/ Modifier à la ligne 119, les informations selon votre compte MySQL, à savoir votre_user et votre_mot_de_passe
    8/ Ouvrir un terminale dans le dossier DEVELOPMENT qui se trouve à la racine du projet
    9/ Entrer la commande suivante : 'javac -d bin src/*.java'
    10/ Puis, entrer la commande suivante : 'java -cp bin ExePonney'


Programmes/logiciels/ressources utilisé pour développer ce projet

    Java (langage de programmation)
    JDBC (interface de programmation permettant aux applications Java d'accéder à des sources de données).
    VsCode (éditeur de code)
    MySQL (Système de gestion de bases de données relationnelles)
    SQL (Langage informatique normalisé servant à exploiter des bases de données relationnelles)


Auteur : 

   Luis DOUDEAU
   Thomas FAUCHER
   Lenny DE NARDI
