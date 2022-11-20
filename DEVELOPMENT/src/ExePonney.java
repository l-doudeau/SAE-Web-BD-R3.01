/* ============================= VOICI LES INSTRUCTIONS AFIN DE LANCER L'APPLICATION !!!!!! ================================

 *  Tout d'abord vous devez lancer les fichiers '.sql' qui se trouve dans le repertoire DEVELOPMENT/scripts
 *  1) Placez-vous dans le repertoire : DEVELOPMENT/scripts
 *  2) Ouvrir une invite de commande et vous connecter à MySQL avec vos identifiants personnels (mysql -h servinfo-mariabd -u votre-login -p)
 *  3) Selectionner votre base de donnée (use DBvotre_login)
 *  4) entrer ces commandes :
 *  > source crePon.sql
 *  > source insPon.sql

 * Afin de lancer l'application vous avez plusieurs possibilités :

 *   1/ Lancer avec VSCode : --> PRÉFÉRABLE
 *      A) Vous devez changer à la ligne 119 de ce fichier les informations pour se connecter à la base de données (votre username et password)
 *      B) Vous devez ajouter dans les Referenced Libraries le fichier 'mysql-connector-java.jar' (module JDBC) si il n'est pas ajouté
 *      C) Lancer avec le bouton en haut à droite / le Run and Debug
 *      D) L'application se lancera dans le terminale en bas de l'écran sur VSCode, vous pouvez le mettre en plein écran
 *         afin d'avoir la meilleur experience possible de l'application.
 * 
 *   2/ Lancer en console : 
 *       A) Vous devez changer à la ligne 97 de ce fichier les informations pour se connecter à la base de données (votre username et password)
 *       B) Placer vous dans le dossier DEVELOPMENT qui se trouve à la racine du projet
 *       C) Ouvrez une invite de commande et entre les commande suivantes :
 *       > javac -d bin --module-path /usr/share/java --add-modules=mysql-connector-java-8.0.30.jar src/*.java | changer le chemin de votre 'mysql-connector-java' si besoin
 *       > java -cp /usr/share/java/mysql-connector-java-8.0.30.jar:bin/ExePonney | changer le chemin de votre 'mysql-connector-java' si besoin
*/


import java.sql.SQLException;
import java.sql.Time;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Calendar;
import java.util.Date;
import java.util.Map;
import java.util.Scanner;


public class ExePonney {
    static String[] options = {"1- Afficher les résultats",
        "2- Insérer des données",
        "3- Supprimer des données",
        "4- Exit",
        };

    static String[] sousMenuAffichage =
        {"1- Client",
        "2- Moniteurs",
        "3- Poneys",
        "4- Cours",
        "5- Réservations",    
        "6- Exit"
        };


    static String[] sousSousMenuAffichage =
        {"1- Afficher un(e)",
        "2- Afficher les",   
        "3- Exit"
        };
    static String[] sousMenuInsertion =
            {"1- Inserér une Personne",
            "2- Inserér un Clients",
            "3- Inserér un Moniteur",
            "4- Inserér un Poney",
            "5- Inserér un Cours",
            "6- Inserér une Réservation",    
            "7- Exit"
        };
     static String[] sousMenuSuppresion =
            {"1- Supprimer une Personne",
            "2- Supprimer un Poney",
            "3- Supprimer un Cours",
            "4- Supprimer une Réservation",    
            "5- Exit"
        };

        private static void printMenu(String[] options){

            System.out.println("=================================");
            for(String option : options){
                
                System.out.println(option);
                
            }
            System.out.println("=================================\n");
            System.out.println("Choisi ton option : ");
        
        }
    
        private static void printMenu(String[] options, String arg){
            System.out.println("=================================");
            for(String option : options){
                
                System.out.println(option + " " + arg);
                
            }
            System.out.println("=================================\n");
            System.out.print("Choisi ton option : ");
        
        }
    
        static Map<Integer,Personne> personnes;
        static Map<Integer,Client> clients ;
        static Map<Integer,Cours> cours;
        static Map<Integer,Moniteur> moniteurs;
        static Map<Integer,Poney> poneys;

        public static void main(String[] args) {
        boolean arret = false;
        
        ConnectionDB bd = null;
        try {
            bd = new ConnectionDB();
            try {
                bd.connecter("GRAND_GALOP", "login", "login");
                clients = Requete.chargerClient(bd);
                poneys = Requete.chargerPoney(bd);
                cours = Requete.chargerCours(bd);
                personnes = Requete.chargerPersonne(bd);
                moniteurs = Requete.chargerMoniteur(bd);
            } 
            catch (SQLException e) {
                e.printStackTrace();
            }

        } catch (ClassNotFoundException e1) {
            System.out.println("Erreur lors de la connexion MYSQL\nVerifier l'ajout de mariaDB dans les Referenced Libraries");
        }

        
    

        Scanner myObj = new Scanner(System.in);
        if(bd!=null){
            while(!arret){
                if(!bd.isConnected()){
                    System.out.println("Veuillez entrer le nom de la base de données : ");
                    String database = myObj.nextLine();
                    System.out.println("Veuillez entrer votre nom d'utilisateur : ");
                    String username = myObj.nextLine(); 
                    System.out.println("Veuillez entrer votre mot de passe : ");
                    String password = myObj.nextLine();
                    try {
                        bd.connecter(database, username, password);
                        clients = Requete.chargerClient(bd);
                        poneys = Requete.chargerPoney(bd);
                        cours = Requete.chargerCours(bd);
                        moniteurs = Requete.chargerMoniteur(bd); 
                    } 
                    catch (SQLException e) {
                        System.out.println("\nIl y a une erreur dans les informations saisies !  \nAppuyez sur entrée pour recommencer");
                        myObj.nextLine();
                        
                    }
                }else{

                    ExePonney.printMenu(options);
                    String choix = myObj.nextLine();
                    Integer numchoix = Integer.parseInt(choix);
                    switch (numchoix){
                        case 1:
                            ExePonney.menuAffichage(sousMenuAffichage,bd);
                            break;
                        case 2:
                            ExePonney.menuInsertion(sousMenuInsertion,bd);
                            break;
                        case 3:
                            ExePonney.menuSuppresion(sousMenuSuppresion,bd);
                            break;
                        case 4:
                            arret = true;
                            System.out.println("Merci d'avoir utilisé notre application");
                            break;
                    }    
                
                }

            }   
            myObj.close();

        }
    }

    private static void menuSuppresion(String[] sousMenuSuppresion2, ConnectionDB bd) {

        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            ExePonney.printMenu(sousMenuSuppresion2);
            String choix = myObj.nextLine();
            Integer numchoix = Integer.parseInt(choix);
            switch(numchoix){
                case 1: 
                    supprimerUnePersonne(bd,myObj);
                    break;
                case 2:
                    supprimerPoney(bd,myObj);
                    break;
                case 3:
                    supprimerCours(bd,myObj);
                    break;
                case 4:
                    supprimerReservations(bd, myObj);
                    break;
                case 5:
                    fini = true;
                    break;
                
                default:
                    System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                    break;
            }
        }
    }
   

    private static void supprimerReservations(ConnectionDB bd, Scanner myObj) {
        boolean ok = false;
        Integer idPoney = -1;
        Integer idPersonne = -1;
        Calendar calendrier = Calendar.getInstance();

        ok=false;
        while(!ok){            
            System.out.println("Veuillez entrer la date de la réservation XX/XX/XXXX HH:mm:ss ");
            String date_brute = myObj.nextLine();
            SimpleDateFormat formatDate = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
            formatDate.setLenient(false);
            try{
                String[] date_time = date_brute.split(" ");
                String[] date_brute_tableau = date_time[0].split("/");
                String[] time_brute_tableau = date_time[1].split(":");
                LocalDateTime localDateTime = LocalDateTime.of(Integer.parseInt(date_brute_tableau[2]), Integer.parseInt(date_brute_tableau[1]), Integer.parseInt(date_brute_tableau[0]), Integer.parseInt(time_brute_tableau[0]), Integer.parseInt(time_brute_tableau[1]), Integer.parseInt(time_brute_tableau[2]));
                Instant instant = localDateTime.atZone(ZoneId.systemDefault()).toInstant();
                Date date = Date.from(instant);
                calendrier.setTime(date);
                ok = true;
            }
            catch(Exception e){
                System.out.println("Saisie incorrecte !");
                ExePonney.pressEnter(myObj);
            }

        }

        while(!personnes.keySet().contains(idPersonne)){
            System.out.println("Veuillez entrer l'id de la personne qui a réservé le cours à supprimer");
            try{
                int id = Integer.parseInt(myObj.nextLine());
                if(!personnes.keySet().contains(id)){
                    System.out.println("ID introuvable \nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }else{
                    idPersonne = id;
                }

            }
            catch(NumberFormatException e){
                System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
                myObj.nextLine();
            }
        }
        while(!poneys.keySet().contains(idPoney)){
            System.out.println("Veuillez entrer l'id du poney réservé à supprimer");
            try{
                int id = Integer.parseInt(myObj.nextLine());
                if(!poneys.keySet().contains(id)){
                    System.out.println("ID introuvable \nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }else{
                    idPoney = id;
                }

            }
            catch(NumberFormatException e){
                System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
                myObj.nextLine();
            }
        }
        Requete.afficheUneReservation(bd, idPersonne,idPoney, calendrier);
        System.out.println("Etes-vous sur de vouloir supprimer cette reservation ? O/N");
            String choix = myObj.nextLine();
            if(choix.equalsIgnoreCase("O")){
                if(Requete.supprimerReservations(bd,calendrier,idPersonne,idPoney)){
                    System.out.println("Suppresion effectuée\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }else{
                    System.out.println("Erreur lors de la suppression !\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }
            }
            else if(choix.equalsIgnoreCase("N")){
                System.out.println("Suppresion annulée\nAppuyer sur entrée pour continuer");
                myObj.nextLine();
            }
        
    }

    private static void supprimerCours(ConnectionDB bd, Scanner myObj) {
        System.out.println("Veuillez entrer l'id du cours à supprimer");
        try{
            int id = Integer.parseInt(myObj.nextLine());
            if(!cours.keySet().contains(id)){
                System.out.println("ID introuvable \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
            }else{
                System.out.println(cours.get(id));
                System.out.println("Etes-vous sur de vouloir supprimer ce cours O/N");
                String choix = myObj.nextLine();
                if(choix.equalsIgnoreCase("O")){
                    if(Requete.supprimerUnCours(bd,id)){
                        System.out.println("Suppresion effectuée\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                        cours.remove(id);
                    }else{
                        System.out.println("Erreur lors de la suppression !\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                    }
                }
                else if(choix.equalsIgnoreCase("N")){
                    System.out.println("Suppresion annulée\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }

            }
        }
        catch(NumberFormatException e){
            System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
        }
    }
    

    private static void supprimerPoney(ConnectionDB bd, Scanner myObj) {
        System.out.println("Veuillez entrer l'id du poney à supprimer");
        try{
            int id = Integer.parseInt(myObj.nextLine());
            if(!poneys.keySet().contains(id)){
                System.out.println("ID introuvable \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
            }else{

                System.out.println(poneys.get(id));
                System.out.println("Etes-vous sur de vouloir supprimer ce poney O/N");
                String choix = myObj.nextLine();
                if(choix.equalsIgnoreCase("O")){
                    if(Requete.supprimerUnPoney(bd,id)){
                        System.out.println("Suppresion effectuée\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                        poneys.remove(id);
                    }
                    else{
                        System.out.println("Erreur lors de la suppression !\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                    }
                }
                else if(choix.equalsIgnoreCase("N")){
                    System.out.println("Suppresion annulée\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }

            }
        }
        catch(NumberFormatException e){
            System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
        }
    }
    

    private static void supprimerUnePersonne(ConnectionDB bd, Scanner myObj) {
        System.out.println("Veuillez entrer l'id de la personne à supprimer");
        try{
            int id = Integer.parseInt(myObj.nextLine());
            if(!personnes.keySet().contains(id)){
                System.out.println("ID introuvable \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
            }else{           
                System.out.println(personnes.get(id));
                System.out.println("Etes-vous sur de vouloir supprimer cette personne O/N");
                String choix = myObj.nextLine();
                if(choix.equalsIgnoreCase("O")){
                    if(Requete.supprimerUnePersonne(bd,id)){
                        System.out.println("Suppresion effectuée\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                        personnes.remove(id);
                    }
                    else{
                        System.out.println("Erreur lors de la suppression !\nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                    }
                }
                else if(choix.equalsIgnoreCase("N")){
                    System.out.println("Suppresion annulée\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                }
            }
        }
        catch(NumberFormatException e){
            System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
            myObj.nextLine();
        }
    }
            
    
    private static void menuAffichage(String[] sousMenuAffichage,ConnectionDB bd) {
        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            ExePonney.printMenu(sousMenuAffichage);
            String choix = myObj.nextLine();
            try{
                Integer numchoix = Integer.parseInt(choix);
                switch(numchoix){
                    case 1:
                        menuAffichageCarac(sousSousMenuAffichage, "Client(e)(s)", bd);
                        break;
                    case 2:
                        menuAffichageCarac(sousSousMenuAffichage, "Moniteur(s)/Monitrice(s)", bd);
                        break;
                    case 3:
                        menuAffichageCarac(sousSousMenuAffichage, "Poney(s)", bd);
                        break;
                    case 4:
                        menuAffichageCarac(sousSousMenuAffichage, "Cours", bd);
                        break;
                    case 5:
                        menuAffichageCarac(sousSousMenuAffichage, "Reservation(s)", bd);
                        break;
                    case 6:
                        fini = true;
                        break;
                    default:
                        System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                        break;
                }
                
            }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
            }
        }
    }

    private static void menuAffichageCarac(String[] sousMenuAffichage, String arg,ConnectionDB bd){

        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            ExePonney.printMenu(sousMenuAffichage,arg);
            String choix = myObj.nextLine();
            try{
                Integer numchoix = Integer.parseInt(choix);
                switch(numchoix){
                    case 1:
                        switch(arg){
                            case "Client(e)(s)":
                                afficheUnClient(bd,myObj);
                                pressEnter(myObj);
                                break;

                            case "Moniteur(s)/Monitrice(s)":
                                afficheUnMoniteur(bd,myObj);
                                pressEnter(myObj);
                                break;
                            
                            case "Poney(s)":
                                afficheUnPoney(bd,myObj);
                                pressEnter(myObj);
                                break;

                            case "Cours":
                                afficheUnCours(bd,myObj);
                                pressEnter(myObj);
                                break;
                            case "Reservation(s)":
                                afficheUneReservation(bd,myObj);
                                pressEnter(myObj);
                                break;
                        }

                        break;
                    case 2:
                        switch(arg){
                            case "Client(e)(s)":
                                afficherLesClients();
                                pressEnter(myObj);
                                break;

                            case "Moniteur(s)/Monitrice(s)":
                                afficherLesMoniteurs();
                                pressEnter(myObj);
                                break;
                            
                            case "Poney(s)":
                                afficherLesPoneys();
                                pressEnter(myObj);
                                break;

                            case "Cours":
                                afficherLesCours();
                                pressEnter(myObj);
                                break;
                            case "Reservation(s)":
                                Requete.afficheReservation(bd);
                                pressEnter(myObj);
                                break;
                        }

                        break;
                    case 3:
                        fini = true;
                        break;
                }
            
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte ! ");
        }
    }
        System.out.println("");
    }

    private static void menuInsertion(String[] sousMenuInsertion,ConnectionDB bd) {
        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            ExePonney.printMenu(sousMenuInsertion);
            String choix = myObj.nextLine();
            try{
                Integer numchoix = Integer.parseInt(choix);
                switch(numchoix){
                    case 1: 
                        insererUnePersonne(bd,myObj);
                        break;
                    case 2:
                        insererClient(bd, myObj);
                        break;
                    case 3:
                        insererMoniteur(bd, myObj);
                        break;
                    case 4:
                        insererPoney(bd,myObj);
                        break;
                    case 5:
                        insererCours(bd,myObj);
                        break;
                    case 6:
                        ExePonney.insererReservations(bd, myObj);
                        break;
                    case 7:
                        fini = true;
                        break;
                    
                    default:
                        System.out.println("Saisie incorect ! \nAppuyer sur entrée pour continuer");
                        myObj.nextLine();
                        break;
                }
            }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
            }
        }
    }
 

    private static void afficheUnClient(ConnectionDB bd,Scanner myObj) {
        System.out.println("Veuillez rentrer l'id de la personne recherchée");
        String id_brute = myObj.nextLine();
        Integer id = Integer.parseInt(id_brute);
        if(clients.get(id) == null)
            System.out.println("Cette id ne correspond pas à un client !");
        else
            System.out.println(clients.get(id));
    }

    private static void afficheUneReservation(ConnectionDB bd,Scanner myObj) {
        Integer idClient = null;
        Integer idPoney = null;
        Calendar calendrier = Calendar.getInstance();
        boolean ok = false;
        //Demander l'id du client
        while(!ok){
            afficherLesClients();
        System.out.println("Veuillez rentrer l'id du client de la réservation recherchée");
        idClient = Integer.parseInt(myObj.nextLine());
        if(clients.get(idClient) == null)
            System.out.println("Cette id ne correspond pas à un client !");
        else
            ok = true;
        
        }
        //Demander l'id du poney
        ok = false;
        while(!ok){
            afficherLesPoneys();
            System.out.println("Veuillez rentrer l'id du poney de la réservation recherchée");
            try{
                idPoney = Integer.parseInt(myObj.nextLine());
                if(poneys.get(idPoney) == null)
                    System.out.println("Cette id ne correspond à aucun poney !");
                else
                    ok = true;
            }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
            }
        }

        //Demander la date de la réservation
        ok=false;
        while(!ok){            
            System.out.println("Veuillez entrer la date de la réservation XX/XX/XXXX HH:mm:ss ");
            String date_brute = myObj.nextLine();
            SimpleDateFormat formatDate = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
            formatDate.setLenient(false);
            try{
                String[] date_time = date_brute.split(" ");
                String[] date_brute_tableau = date_time[0].split("/");
                String[] time_brute_tableau = date_time[1].split(":");
                LocalDateTime localDateTime = LocalDateTime.of(Integer.parseInt(date_brute_tableau[2]), Integer.parseInt(date_brute_tableau[1]), Integer.parseInt(date_brute_tableau[0]), Integer.parseInt(time_brute_tableau[0]), Integer.parseInt(time_brute_tableau[1]), Integer.parseInt(time_brute_tableau[2]));
                Instant instant = localDateTime.atZone(ZoneId.systemDefault()).toInstant();
                Date date = Date.from(instant);
                calendrier.setTime(date);
                ok = true;
            }
            catch(Exception e){
                System.out.println("Saisie incorrecte !");
                ExePonney.pressEnter(myObj);
            }

        }
        Requete.afficheUneReservation(bd, idClient, idPoney, calendrier);
        

    }
    
    private static void afficheUnCours(ConnectionDB bd,Scanner myObj) {
        System.out.println("Veuillez rentrer l'id du cours recherché");
        String id_brute = myObj.nextLine();
        try{
            Integer id = Integer.parseInt(id_brute);
            if(cours.get(id) == null)
                System.out.println("Cette id ne correspond à aucun cours !");
            else
                System.out.println(cours.get(id));
        
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte !");
        }
    }
        
    private static void afficheUnPoney(ConnectionDB bd,Scanner myObj) {
        System.out.println("Veuillez rentrer l'id du poney recherché");
        String id_brute = myObj.nextLine();
        try{
            Integer id = Integer.parseInt(id_brute);
            if(poneys.get(id) == null)
                System.out.println("Cette id ne correspond à aucun poney !");
            else
                System.out.println(poneys.get(id));
        }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
        }
    }

    private static void afficheUnMoniteur(ConnectionDB bd,Scanner myObj) {
        System.out.println("Veuillez rentrer l'id de la personne recherchée");
        try{
            String id_brute = myObj.nextLine();
            Integer id = Integer.parseInt(id_brute);
            if(moniteurs.get(id) == null)
                System.out.println("Cette id ne correspond pas à un moniteur !");
            else
                System.out.println(moniteurs.get(id));
            
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte !");
        }
    }
    private static void afficherLesClients() {

        for(Client c : clients.values()){
            System.out.println(c.toString());
        }

    }
    private static void afficherLesMoniteurs() {

        for(Moniteur moniteur : moniteurs.values()){
            System.out.println(moniteur.toString());
        }

    }
    private static void afficherLesCours() {

        for(Cours unCours : cours.values()){
            System.out.println(unCours.toString());
        }

    }
    private static void afficherLesPoneys() {

        for(Poney poney : poneys.values()){
            System.out.println(poney.toString());
        }

    }

    private static void insererReservations(ConnectionDB bd , Scanner scanner){
        boolean ok =false;
        Calendar calendrier = Calendar.getInstance();
        while (!ok){
            System.out.println("Veuillez entrer la date de la reservation sous la forme XX/XX/XXXX ");
            String date_brute = scanner.nextLine();
            System.out.println("Veuillez entrer l'heure reservation sous la forme XX:XX:XX ");
            String temps_brute = scanner.nextLine();
            SimpleDateFormat formatDate = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
            formatDate.setLenient(false);
            try
            {
                Date d = formatDate.parse(date_brute +" " +temps_brute);
                System.out.println(date_brute+" est une date valide");
                calendrier.setTime(d);
                ok = true;
            }
            // Date invalide
            catch (ParseException e)
            {
                System.out.println(date_brute + " a " + temps_brute +" est une date invalide");
            }
        }
 
            try{
            System.out.println("Veuillez entrer l'id de la personne qui réserve le cours");
            Integer idP = Integer.parseInt(scanner.nextLine());
        
            System.out.println("Veuillez entrer l'id du cours qui est réservé le cours");
            Integer idC = Integer.parseInt(scanner.nextLine());


            System.out.println("Veuillez entrer l'id du poney qui est réservé pour le cours");
            Integer idPo = Integer.parseInt(scanner.nextLine());


            System.out.println("Veuillez entrer le temps du cours sous la forme XX:XX:XX ");
            String time_brute = scanner.nextLine(); 
            Time duree = Time.valueOf(time_brute);


            System.out.println("Veuillez entrer si oui ou non, le client à payé : O/N ");
            String reponse = scanner.nextLine();
            boolean a_paye;
            if(reponse == "O"){
                a_paye = true;
            }
            else{
                a_paye = false;
            }
            Reservation reservation = new Reservation(calendrier, idP, idC, idPo, duree, a_paye);
            if(Requete.insererReservations(bd, reservation)){
                System.out.println("L'inserstion s'est bien déroulé");
            }
            else{
                System.out.println("Erreur dans l'insertion ! ");
            }
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte !");
        }

    }

    private static void insererUnePersonne(ConnectionDB bd, Scanner scanner) {
        boolean ok =false;
        Calendar calendrier = Calendar.getInstance();
        System.out.println("Veuillez entrer le 'NOM prenom' de la personne ");
        String nomPrenom_brute = scanner.nextLine();
        String [] nomPrenom = nomPrenom_brute.split(" ");
        while(!ok){

            
            System.out.println("Veuillez entrer la date de naissance de la personne sous la forme XX/XX/XXXX ");
            String date_brute = scanner.nextLine();
            SimpleDateFormat formatDate = new SimpleDateFormat("dd/MM/yyyy");
            formatDate.setLenient(false);
            try{
                Date d = formatDate.parse(date_brute);
                calendrier.setTime(d);
                ok = true;
            }
            // Date invalide
            catch (ParseException e)
            {
                System.out.println(date_brute +" est une date invalide");
            }
        }
            try{
            System.out.println("Veuillez entrer le poids de la personne ");
            Float poids = Float.parseFloat(scanner.nextLine());


            System.out.println("Veuillez entrer l'adresse email de la personne");
            String email = scanner.nextLine();

            System.out.println("Veuillez entrer la mot de passe de la personne");
            String password = scanner.nextLine();
            
            System.out.println("Veuillez entrer l'adresse de la personne");
            String adresse_postal = scanner.nextLine();
            
            System.out.println("Veuillez entrer le code postal de la personne");
            Integer code_postal = Integer.parseInt(scanner.nextLine());
            
            System.out.println("Veuillez entrer la ville de la personne");
            String ville = scanner.nextLine();

            System.out.println("Veuillez entrer le numéro de téléphone de la personne");
            String numTel = scanner.nextLine();

            Personne personne = new Personne(Requete.maxIDPersonne(bd)+1, nomPrenom[0], nomPrenom[1], calendrier, poids, email, adresse_postal, code_postal, ville, numTel, password);
            if(Requete.insererPersonne(bd, personne)){
                System.out.println("Insertion efféctuée ");
                pressEnter(scanner);
            
            }else{
                System.out.println("Insertion impossible");
            }
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte !");
        }

    }
    
    private static void insererClient(ConnectionDB bd, Scanner scanner){
        boolean ok = false;
        Boolean cotisation = null;
        Personne p  = null;
        while(!ok){
            System.out.println("Veuillez entrer l'id du client");
            try{
                Integer idC = Integer.parseInt(scanner.nextLine());
                if(personnes.get(idC) instanceof Personne){
                    ok = true;
                    p = personnes.get(idC);
                }
                else{
                    System.out.println("l'id du client est inconnu (Veuillez créer la personne)");
                    pressEnter(scanner);
                }
            }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
            }
        }
        ok = false;
        while(!ok){
            System.out.println("Veuillez entrer si le client à déjà cotisé O/N ");
            String reponse = scanner.nextLine();
            if(reponse.equalsIgnoreCase("O") || reponse.equalsIgnoreCase("N")){
                ok = true;
                if(reponse.equalsIgnoreCase("O")) cotisation = true;
                else cotisation = false;
            }
            else{
                System.out.println("Reponse invalide ! ");
                pressEnter(scanner);
            }
        }

        Client c = new Client(p.getId(), p.getNom(), p.getPrenom(), p.getDateDeNaissance(), p.getPoids(),p.getAdresseEmail(),p.getAdresse(),p.getCodePostal(), p.getVille(),p.getNumTel(), p.getMotdepasse(), cotisation);
        if(Requete.insererClient(bd, c)){
            System.out.println("Insertion efféctuée ");
            clients.put(p.getId(), c);
            pressEnter(scanner);
        }

    }

    private static void insererMoniteur(ConnectionDB bd, Scanner scanner){
        boolean ok = false;
        Personne p = null;
        while(!ok){
            System.out.println("Veuillez entrer l'id du client");
            Integer idM = Integer.parseInt(scanner.nextLine());
            if(personnes.get(idM) instanceof Personne){
                ok = true;
                p = personnes.get(idM);
            }
            else{
                System.out.println("l'id du moniteur est inconnu (Veuillez créer la personne)");
                pressEnter(scanner);
            }
        }
        Moniteur m = new Moniteur(p.getId(), p.getNom(), p.getPrenom(), p.getDateDeNaissance(), p.getPoids(),p.getAdresseEmail(),p.getAdresse(),p.getCodePostal(), p.getVille(),p.getNumTel(), p.getMotdepasse());
        if(Requete.insererMoniteur(bd, m)){
            System.out.println("Insertion efféctuée ");
            pressEnter(scanner);
        
        }

    }

    private static void insererPoney(ConnectionDB bd,Scanner scanner){

        System.out.println("Veuillez entrer le nom du poney ");
        String nomPo = scanner.nextLine();
        try{
            System.out.println("Veuillez entrer le poids max du poney");
            Integer poidsMax = Integer.parseInt(scanner.nextLine());
            
            Poney poney = new Poney(Requete.maxIDPoney(bd)+1, nomPo, poidsMax);
            if(Requete.insererPoney(bd,poney)){
                System.out.println("Insertion efféctuée");
                pressEnter(scanner);
            }
        }catch(NumberFormatException e){
                System.out.println("Saisie incorrecte !");
            }
        


    }
  
    private static void insererCours(ConnectionDB bd, Scanner myObj) {
        

        String nomCours = "";
        String description = "";
        String typeCours = "";
        Integer prix = null;
        Integer id = null;

        System.out.println("Veuillez entrer le nom du cours");
        nomCours = myObj.nextLine();

        System.out.println("Veuillez entrer la description du cours");
        description = myObj.nextLine();
        boolean ok = false;
        while(!ok){
 
            System.out.println("Veuillez entrer le type du cours (Collectif/Individuel)");
            typeCours = myObj.nextLine();
            if(typeCours.equalsIgnoreCase("Collectif") || typeCours.equalsIgnoreCase("Individuel")){
                ok = true;
            }
            else{
                System.out.println("Saisie incorrect veuillez recommancer !");
                pressEnter(myObj);
            }
        }
        try{
            System.out.println("Veuillez entrer le prix du cours");
            prix  = Integer.parseInt(myObj.nextLine());

            afficherLesMoniteurs();
            System.out.println("Veuillez entrer l'id du moniteur");
            id  = Integer.parseInt(myObj.nextLine());

            Cours cours = new Cours(Requete.maxIDCours(bd)+1, nomCours, description, typeCours, prix,id);
            if(Requete.insererCours(bd, cours)){
                System.out.println("Insertion efféctué ");
                pressEnter(myObj);
            }
        }catch(NumberFormatException e){
            System.out.println("Saisie incorrecte !");
        }
        
    }
  
  
  
    private static void pressEnter(Scanner myObj){
        System.out.println("\nAppuyer sur entrée pour continuer");
        myObj.nextLine();
    }
}