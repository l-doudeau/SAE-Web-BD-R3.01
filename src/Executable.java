import java.net.ConnectException;
import java.sql.SQLException;
import java.sql.Time;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Map;
import java.util.Scanner;
import java.util.spi.CalendarDataProvider;


public class Executable {
    

    public static void main(String[] args) {
        boolean arret = false;
        Map<Integer,Client> clients = null;
        Map<Integer,Cours> cours = null;
        Map<Integer,Moniteur> moniteurs = null;
        Map<Integer,Poney> poneys = null;
        ConnectionDB bd = null;
        try {
            bd = new ConnectionDB();
            try {
                bd.connecter("DBfaucher", "faucher", "Thierry45.");
                clients = Requete.chargerClient(bd);
                poneys = Requete.chargerPoney(bd);
                cours = Requete.chargerCours(bd);
                moniteurs = Requete.chargerMoniteur(bd);
            } 
            catch (SQLException e) {
                e.printStackTrace();
            }

        } catch (ClassNotFoundException e1) {
            System.out.println("Erreur lors de la connexion MYSQL\nVerifier l'ajout de mariaDB dans les Referenced Libraries");
        }

        String[] options = {"1- Afficher les résultats",
        "2- Insérer des données",
        "3- Exit",
        };

        String[] sousMenuAffichage =
        {"1- Affichier les Clients",
        "2- Afficher les Moniteurs",
        "3- Afficher les Poneys",
        "4- Afficher les Cours",
        "5- Afficher les réservations",    
        "6- Exit"
        };
        String[] sousMenuInsertion =
            {"1- Inserér un Clients",
            "2- Inserér un Moniteur",
            "3- Inserér un Poney",
            "4- Inserér un Cours",
            "5- Inserér une Réservation",    
            "6- Exit"
        };
    

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
                    } 
                    catch (SQLException e) {
                        System.out.println("\nIl y a une erreur dans les informations saisies !  \nAppuyez sur entrée pour recommencer");
                        myObj.nextLine();
                        clients = Requete.chargerClient(bd);
                        poneys = Requete.chargerPoney(bd);
                        cours = Requete.chargerCours(bd);
                        moniteurs = Requete.chargerMoniteur(bd);
                    }
                }else{
                    Executable.printMenu(options);
                    String choix = myObj.nextLine();
                    Integer numchoix = Integer.parseInt(choix);
                    switch (numchoix){
                        case 1:
                            Executable.menuAffichage(sousMenuAffichage,bd,clients,poneys,cours);
                            break;
                        case 2:
                            Executable.menuInsertion(sousMenuInsertion, bd, clients, poneys, cours);
                            break;

                    }    
                }

            }   
            myObj.close();

        }
    }

    private static void menuAffichage(String[] sousMenuAffichage,ConnectionDB bd,
    Map<Integer,Client> clients, Map<Integer,Poney> poneys, Map<Integer,Cours> cours) {
        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            Executable.printMenu(sousMenuAffichage);
            String choix = myObj.nextLine();
            Integer numchoix = Integer.parseInt(choix);
            switch(numchoix){
                case 1:
                    //TODO AFFICHER CLIENTS
                    break;
                case 2:
                    //TODO  AFFICHER MONITEURS
                    break;
                case 3:
                    //TODO AFFICHER COURS
                    break;
                case 4:
                    //TODO AFFICHER PONEY
                    break;
                case 5:
                    Requete.afficheReservation(bd, clients, poneys, cours);
                    System.out.println("\nAppuyer sur entrée pour continuer");
                    myObj.nextLine();
                    break;
                case 6:
                    fini = true;
                    break;
            }
            
        }
        myObj.close();
    }

    private static void menuInsertion(String[] sousMenuInsertion,ConnectionDB bd,
    Map<Integer,Client> clients, Map<Integer,Poney> poneys, Map<Integer,Cours> cours) {
        Scanner myObj = new Scanner(System.in);
        boolean fini = false;
        while(!fini){
            Executable.printMenu(sousMenuInsertion);
            String choix = myObj.nextLine();
            Integer numchoix = Integer.parseInt(choix);
            switch(numchoix){
                case 1:
                    //TODO INSERER CLIENTS
                    break;
                case 2:
                    //TODO  INSERER MONITEURS
                    break;
                case 3:
                    //TODO INSERER COURS
                    break;
                case 4:
                    //TODO INSERER PONEY
                    break;
                case 5:
                    Executable.insererReservations(bd, myObj);
                    break;
                case 6:
                    fini = true;
                }
            }
            myObj.close();
        }



    public static void printMenu(String[] options){
        System.out.println("=================================");
        for(String option : options){
            
            System.out.println(option);
            
        }
        System.out.println("=================================\n");
        System.out.print("Choisi ton option : ");
    
    }
    public static void insererReservations(ConnectionDB bd , Scanner scanner){
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
                e.printStackTrace();
                System.out.println(date_brute + " a " + temps_brute +" est une date invalide");
            }
        }
 
        
        System.out.println("Veuillez entrer l'id de la personne qui réserve le cours");
        String idP_brute = scanner.nextLine();
        
        Integer idP = Integer.parseInt(idP_brute);

        System.out.println("Veuillez entrer l'id du cours qui est réservé le cours");
        String idC_brute = scanner.nextLine();
        Integer idC = Integer.parseInt(idC_brute);

        System.out.println("Veuillez entrer l'id du poney qui est réservé pour le cours");
        String idPo_brute = scanner.nextLine();
        Integer idPo = Integer.parseInt(idPo_brute);


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
        if(Requete.insererReservations(bd, calendrier ,3, 1, 1, duree, a_paye)){
            System.out.println("L'inserstion s'est bien déroulé");
        }
        else{
            System.out.println("Erreur dans l'insertion ! ");
        }

    }
}
