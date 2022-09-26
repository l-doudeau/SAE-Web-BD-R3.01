import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Requete {
    

    public static void afficheReservation(ConnectionDB bd){
        Statement s;
        try {
            s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select * from RESERVER");
            while(res.next()){
                Date date = res.getDate(0);

            }









        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        

    }

    public static Map<Integer,Client> chargerClient(ConnectionDB bd){
        Map<Integer,Client> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet clients = s.executeQuery("select * from CLIENT natural join PERSONNE");
        while(clients.next()){
            res.put(clients.getInt(0),new Client(clients.getInt(0), clients.getString(2), clients.getString(3), clients.getDate(4),clients.getInt(5), adresseEmail, adresse, codePostal, ville, numTel, motDePasse, clients.getBoolean(1))
            }

        return res;
    }


    public static Map<Integer, Poney> chargerPoney(ConnectionDB bd){
        try{
        Map<Integer,Poney> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet poneys = s.executeQuery("select * from PONEY");
        while(poneys.next()){
            res.put(poneys.getInt(0), new Poney(poneys.getInt(1), poneys.getString(2), poneys.getDouble(3)));
        }
        System.out.println(res);
        return res;
    } catch(SQLException e1){
        e1.printStackTrace();
    }
    return null;
    }

    public static Map<Integer,Moniteur> chargerMoniteur(ConnectionDB bd){
        try{
        Map<Integer, Moniteur> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet moniteurs = s.executeQuery("select * from MONITEUR natural join PERSONNE");
        while(moniteurs.next()){
            res.put(moniteurs.getInt(1),new Moniteur(moniteurs.getInt(1), moniteurs.getString(2), moniteurs.getString(3), moniteurs.getDate(4),moniteurs.getInt(5), moniteurs.getString(6), moniteurs.getString(7), moniteurs.getInt(8), moniteurs.getString(9), moniteurs.getInt(10), moniteurs.getString(11));
            }

            System.out.println(res);
            return res;
        } catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
        }
    

        
    public static Map<Integer,Cours> chargerCours(ConnectionDB bd){
        try{
        Map<Integer, Cours> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet Courss = s.executeQuery("select * from COURS");
        while(Courss.next()){
            res.put(Courss.getInt(0),new Cours(Courss.getInt(1), Courss.getString(2), Courss.getString(3), Courss.getString(4), Courss.getDouble(5));
            }

            System.out.println(res);
            return res;
        } catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
        }


}
