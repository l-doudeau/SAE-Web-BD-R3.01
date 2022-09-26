import java.net.ConnectException;
import java.sql.SQLException;
import java.util.Map;
import java.util.Scanner;

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
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        } catch (ClassNotFoundException e1) {
        
        }

        String[] options = {"1- Afficher les réservations",
        "2- Créer une réservation",
        "3- Ajouter un client",
        "4- Exit",
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
                        

                    } catch (SQLException e) {
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
                            Requete.afficheReservation(bd, clients, poneys, cours);
                            System.out.println("\nAppuyer sur entrée pour continuer");
                            myObj.nextLine();
                            break;
                    }    
                }

            }


        }
    }

    public static void printMenu(String[] options){

        for(String option : options){
            System.out.println(option);
        }
        System.out.print("Choisi ton option : ");
    
    }
}
