import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Requete {
    

    public static void afficheReservation(ConnectionDB bd,Map<Integer,Client> clients, Map<Integer,Poney> poneys, Map<Integer,Cours> cours){
        Statement s;
        try {
            s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select * from RESERVER");
            while(res.next()){
                Date date = res.getDate(1);
                Time heure = res.getTime(1);
                Time temps = res.getTime(5);
                String a_paye;
                if(res.getBoolean(5)){
                    a_paye = "payé";
                }
                else{
                    a_paye = "n'est pas payé";
                }
                System.out.println("\nReservation du " + date + " " + heure +" " + a_paye + " par " + clients.get(res.getInt(2)).getNom() + " avec le poney " + poneys.get(res.getInt(4)).getNom() + " au cours " + cours.get(res.getInt(3)).getNomCours() + " qui dure " + temps +"h");
            }

        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        

    }

    public static Map<Integer,Client> chargerClient(ConnectionDB bd){
        try {
            Map<Integer,Client> res = new HashMap<>();
            Statement s = bd.getConnection().createStatement();
            ResultSet clients;
            clients = s.executeQuery("select * from CLIENT natural join PERSONNE");
            while(clients.next()){
                res.put(clients.getInt(1),new Client(clients.getInt(1), clients.getString(3), clients.getString(4), clients.getDate(5),clients.getInt(6), clients.getString(7), clients.getString(8), clients.getInt(9), clients.getString(10), clients.getInt(11),clients.getString(12), clients.getBoolean(2)));
            }

            return res;
        } catch (SQLException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        
        return null;
    }


    public static Map<Integer, Poney> chargerPoney(ConnectionDB bd){
        try{
        Map<Integer,Poney> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet poneys = s.executeQuery("select * from PONEYS");
        while(poneys.next()){
            res.put(poneys.getInt(1), new Poney(poneys.getInt(1), poneys.getString(2),(float) poneys.getDouble(3)));
        }

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
            res.put(moniteurs.getInt(1),new Moniteur(moniteurs.getInt(1), moniteurs.getString(2), moniteurs.getString(3), moniteurs.getDate(4),moniteurs.getInt(5), moniteurs.getString(6), moniteurs.getString(7), moniteurs.getInt(8), moniteurs.getString(9), moniteurs.getInt(10), moniteurs.getString(11)));
            }

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
            res.put(Courss.getInt(1),new Cours(Courss.getInt(1), Courss.getString(2), Courss.getString(3), Courss.getString(4), (float) Courss.getDouble(5)));
            }


            return res;
        } catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
        }

    public static boolean insererReservations(ConnectionDB bd, Calendar calendrier, int idP, int idC, int idPo, Time duree, boolean a_paye){
        PreparedStatement ps;
        try {
            ps = bd.getConnection().prepareStatement("insert into RESERVER values (?, ?, ?, ?, ?, ?);");
        String mois = ""+calendrier.get(Calendar.MONTH);
        String jours = ""+calendrier.get(Calendar.DATE);
        if(mois.length() == 1){
            mois = "0" + mois;

        }

        if(jours.length() == 1){
            jours = "0" + jours;
        }
        java.util.Date utilDate = calendrier.getTime();
        java.sql.Date sqlDate = new java.sql.Date(utilDate.getTime());
        ps.setDate(1, sqlDate);
        ps.setInt(2, idP);
        ps.setInt(3, idC);
        ps.setInt(4, idPo);
        ps.setTime(5, duree);
        ps.setBoolean(6, a_paye);

        ps.executeUpdate();
        return true;
    } catch (SQLException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
        return false;
    }
    }


}
