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
                bd.connecter("DBdoudeau", "doudeau", "doudeau");
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
                        case 2:
                            
                            Executable.insererReservations(bd,myObj);
                            


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
