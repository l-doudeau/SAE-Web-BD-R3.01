import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class Requete {
    

    public static Integer maxIDPersonne(ConnectionDB bd){
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(idp) from PERSONNE");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
    }

    public static Integer maxIDCours(ConnectionDB bd){
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(idc) from COURS");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
    }

    public static Integer maxIDPoney(ConnectionDB bd){
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(idpo) from PONEYS");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            e1.printStackTrace();
        }
        return null;
    }


    public static void afficheReservation(ConnectionDB bd){
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
                System.out.println("\nReservation du " + date + " " + heure +" " + a_paye + " par " + Executable.clients.get(res.getInt(2)).getNom() + " avec le poney " + Executable.poneys.get(res.getInt(4)).getNom() + " au cours " + Executable.cours.get(res.getInt(3)).getNomCours() + " qui dure " + temps +"h");
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
        

    }


    public static void afficheUneReservation(ConnectionDB bd,Integer idClient, Integer idPoney, Calendar dateR){
        Statement s;
        try {
            s = bd.getConnection().createStatement();

            ResultSet res = s.executeQuery("select * from RESERVER where YEAR(jmahms) = " + dateR.get(Calendar.YEAR) + " and  MONTH(jmahms) =" + dateR.get(Calendar.MONTH)+1 +" and DAY(jmahms) =" + dateR.get(Calendar.DAY_OF_MONTH) + " and  hour(jmahms) = " + dateR.get(Calendar.HOUR) + " and minute(jmahms) = " + dateR.get(Calendar.MINUTE) + " and second(jmahms) = " + dateR.get(Calendar.SECOND)+  " and idp = " + idClient + " and idpo = " + idPoney + ";");
            res.next();
            Time heure = res.getTime(1);
            Time temps = res.getTime(5);
            String a_paye;
            if(res.getBoolean(5)){
                a_paye = "payé";
            }
            else{
                a_paye = "n'est pas payé";
            }
            System.out.println("\nReservation du " + dateR.getTime() + " " + heure +" " + a_paye + " par " + Executable.clients.get(res.getInt(2)).getNom() + " avec le poney " + Executable.poneys.get(res.getInt(4)).getNom() + " au cours " + Executable.cours.get(res.getInt(3)).getNomCours() + " qui dure " + temps +"h");
    
        } catch (SQLException e) {
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
                Calendar calendrier = Calendar.getInstance();
                calendrier.setTime(clients.getDate(5));
                Client c = new Client(clients.getInt(1),  clients.getString(3), clients.getString(4), calendrier, clients.getInt(6), clients.getString(7), clients.getString(8), clients.getInt(9),  clients.getString(10),  clients.getString(11), clients.getString(12), clients.getBoolean(2));
                res.put(clients.getInt(1),c);
            }

            return res;
        } catch (SQLException e1) {
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
            Calendar calendrier = Calendar.getInstance();
            calendrier.setTime(moniteurs.getDate(4));
            Moniteur moniteur = new Moniteur(moniteurs.getInt(1), moniteurs.getString(2), moniteurs.getString(3), calendrier,moniteurs.getInt(5), moniteurs.getString(6), moniteurs.getString(7), moniteurs.getInt(8), moniteurs.getString(9), moniteurs.getString(10), moniteurs.getString(11));
            res.put(moniteurs.getInt(1),moniteur);
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

    public static boolean insererReservations(ConnectionDB bd, Reservation uneReservation){
        PreparedStatement ps;
        try {
            ps = bd.getConnection().prepareStatement("insert into RESERVER values (?, ?, ?, ?, ?, ?);");
            java.util.Date utilDate = uneReservation.getDate().getTime();
            java.sql.Date sqlDate = new java.sql.Date(utilDate.getTime());
            ps.setDate(1, sqlDate);
            ps.setInt(2, uneReservation.getIdPersonne());
            ps.setInt(3, uneReservation.getIdCours());
            ps.setInt(4, uneReservation.getIdPoney());
            ps.setTime(5, uneReservation.getDuree());
            ps.setBoolean(6, uneReservation.getAPaye());

            ps.executeUpdate();
            return true;
        }catch (SQLException e) {

            e.printStackTrace();
            return false;
        }
    }
    
    public static boolean insererClient(ConnectionDB bd, Client unClient){
        PreparedStatement psClient;
        PreparedStatement psPersonne;
        try {

            psPersonne = bd.getConnection().prepareStatement("INSERT INTO PERSONNE values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);");
            psClient = bd.getConnection().prepareStatement("insert into CLIENT values(?,?);");
            
            
            psPersonne.setInt(1, unClient.getId());
            psPersonne.setString(2, unClient.getNom());
            psPersonne.setString(3, unClient.getPrenom());
            Date date = unClient.getDateDeNaissance().getTime();
            java.sql.Date sqlDate = new java.sql.Date(date.getTime());

            psPersonne.setDate(4, sqlDate);
            psPersonne.setFloat(5, unClient.getPoids());
            psPersonne.setString(6, unClient.getAdresseEmail());
            psPersonne.setString(7, unClient.getAdresse());
            psPersonne.setInt(8, unClient.getCodePostal());
            psPersonne.setString(9, unClient.getVille());
            psPersonne.setString(10, unClient.getNumTel());
            psPersonne.setString(11, unClient.getMotdepasse());
            psPersonne.executeUpdate();

            psClient.setInt(1, unClient.getId());
            psClient.setBoolean(2, unClient.getCotisation());
            psClient.executeUpdate();

            
            return true;
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
    
    public static boolean insererMoniteur(ConnectionDB bd, Moniteur unMoniteur){
        PreparedStatement psPersonne;
        PreparedStatement psMoniteur;
        try {
            psPersonne = bd.getConnection().prepareStatement("insert into PERSONNE values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);");
            psMoniteur = bd.getConnection().prepareStatement("INSERT INTO MONITEUR values(?);");


            psPersonne.setInt(1,unMoniteur.getId());
            psPersonne.setString(2, unMoniteur.getNom());
            psPersonne.setString(3, unMoniteur.getPrenom());

            java.util.Date utilDate = unMoniteur.getDateDeNaissance().getTime();
            java.sql.Date sqlDate = new java.sql.Date(utilDate.getTime());

            psPersonne.setDate(4, sqlDate);
            psPersonne.setFloat(5, unMoniteur.getPoids());
            psPersonne.setString(6, unMoniteur.getAdresseEmail());
            psPersonne.setString(7, unMoniteur.getAdresse());
            psPersonne.setInt(8, unMoniteur.getCodePostal());
            psPersonne.setString(9, unMoniteur.getVille());
            psPersonne.setString(10, unMoniteur.getNumTel());
            psPersonne.setString(11, unMoniteur.getMotdepasse());
            
            psPersonne.executeUpdate();

            psMoniteur.setInt(1, unMoniteur.getId());
            psMoniteur.executeUpdate();
            return true;
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public static boolean insererCours(ConnectionDB bd, Cours unCours){
        PreparedStatement ps;
        try {
            ps = bd.getConnection().prepareStatement("insert into COURS values(?, ?, ?, ?, ?);");

            ps.setInt(1, unCours.getId());
            ps.setString(2, unCours.getNomCours());
            ps.setString(3, unCours.getDescription());
            ps.setString(4, unCours.getTypeCours());
            ps.setFloat(5, unCours.getPrix());

            ps.executeUpdate();
            return true;
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public static boolean insererPoney(ConnectionDB bd, Poney poney){
        PreparedStatement ps;
        try{
            ps = bd.getConnection().prepareStatement("insert into PONEYS values(?, ?, ?);");

            ps.setInt(1, poney.getId());
            ps.setString(2, poney.getNom());
            ps.setFloat(3, poney.getPoidsSupporte());

            ps.executeUpdate();
            return true;
        }
        
        catch(SQLException e){
            e.printStackTrace();
            return false;
        }
    }
}