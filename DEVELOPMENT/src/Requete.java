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
        /**
         * Il renvoie l'identifiant maximum de la table PERSONNE
         * 
         * @param bd la connexion à la base de données
         * @return L'identifiant maximum de la personne dans la base de données.
         */
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(id) from PERSONNE");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            return 0;
        }

    }

    
    public static Integer maxIDCours(ConnectionDB bd){
        /**
         * Il renvoie l'identifiant maximum des cours dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @return La valeur idc maximale dans la table COURS.
         */
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(idc) from COURS");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            return 0;
        }

    }
    
    public static Integer maxIDPoney(ConnectionDB bd){
        /**
         * Il renvoie l'ID maximum d'un poney dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @return L'ID maximum de la table Poney.
         */
        try{
            Statement s = bd.getConnection().createStatement();
            ResultSet res = s.executeQuery("select max(idpo) from PONEYS");
            res.next();
            return res.getInt(1);
        }
        catch(SQLException e1){
            return 0;
        }

    }


    
    public static void afficheReservation(ConnectionDB bd){
        /**
         * Il affiche toutes les réservations dans la base de données
         * 
         * @param bd la connexion à la base de données
         */
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
                System.out.println("\nReservation du " + date + " " + heure +" " + a_paye + " par " + ExePonney.clients.get(res.getInt(2)).getNom() + " avec le poney " + ExePonney.poneys.get(res.getInt(4)).getNom() + " au cours " + ExePonney.cours.get(res.getInt(3)).getNomCours() + " qui dure " + temps +"h");
            }

        } catch (SQLException e) {
            System.out.println("Aucune connexion");
        }
        

    }



    public static void afficheUneReservation(ConnectionDB bd,Integer idClient, Integer idPoney, Calendar dateR){
        /**
         * Il affiche une réservation compte tenu de l'identifiant du client, de l'identifiant du poney et
         * de la date de la réservation
         * 
         * @param bd la connexion à la base de données
         * @param idClient l'identifiant du client
         * @param idPoney l'id du poney
         * @param dateR la date de la réservation
         */
        PreparedStatement s;
        try {
            s = bd.getConnection().prepareStatement("select * from RESERVER where jmahms= ? and idpo = ? and id = ?");
            java.sql.Timestamp timestamp = new java.sql.Timestamp(dateR.getTimeInMillis());
            s.setTimestamp(1, timestamp);
            s.setInt(2, idPoney);
            s.setInt(3, idClient);
        
            ResultSet res = s.executeQuery();
            res.next();
            java.sql.Date heure = res.getDate(1);
            java.sql.Time temps = res.getTime(5);
            String a_paye;
            if(res.getBoolean(5)){
                a_paye = "payé";
            }
            else{
                a_paye = "n'est pas payé";
            }
            System.out.println("\nReservation du " + dateR.getTime() + " " + heure +" " + a_paye + " par " + ExePonney.clients.get(res.getInt(2)).getNom() + " avec le poney " + ExePonney.poneys.get(res.getInt(4)).getNom() + " au cours " + ExePonney.cours.get(res.getInt(3)).getNomCours() + " qui dure " + temps +"h");
    
        } catch (SQLException e) {
            
            System.out.println("Il n'y a aucune ligne correspondante aux données données");
        }
        

    }   


    public static Map<Integer, Personne> chargerPersonne(ConnectionDB bd){
        /**
         * Elle prend un objet ConnectionDB en paramètre et retourne un objet Map<Integer, Personne>
         * 
         * @param bd la connexion à la base de données
         * @return Une carte des objets Personne
         */
        try{
        Map<Integer,Personne> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet personnes = s.executeQuery("select * from PERSONNE");
        while(personnes.next()){
            Calendar c = Calendar.getInstance();
            
            c.setTime(personnes.getDate(4));

            res.put(personnes.getInt(1), new Personne(personnes.getInt(1), personnes.getString(2), personnes.getString(3), c, personnes.getInt(5), personnes.getString(6), personnes.getString(7), personnes.getInt(8), personnes.getString(9), personnes.getString(10),personnes.getString(11)));
        
        }

        return res;
    } catch(SQLException e1){
        System.out.println("Aucune connexion");
    }
    return null;
    }


    public static Map<Integer,Client> chargerClient(ConnectionDB bd){
        /**
         * Il prend une connexion à une base de données et renvoie une carte de tous les clients de la base
         * de données
         * 
         * @param bd la connexion à la base de données
         * @return Une carte des clients
         */
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
            System.out.println("Aucune connexion");
        }
        
        return null;
    }



    public static Map<Integer, Poney> chargerPoney(ConnectionDB bd){
        /**
         * Il prend une connexion à une base de données et renvoie une carte de tous les poneys de la base de
         * données
         * 
         * @param bd la connexion à la base de données
         * @return Une carte des poneys
         */
        try{
        Map<Integer,Poney> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet poneys = s.executeQuery("select * from PONEYS");
        while(poneys.next()){
            res.put(poneys.getInt(1), new Poney(poneys.getInt(1), poneys.getString(2),(float) poneys.getDouble(3)));
        }

        return res;
    } catch(SQLException e1){
        System.out.println("Aucune connexion");
    }
    return null;
    }


    public static Map<Integer,Moniteur> chargerMoniteur(ConnectionDB bd){
        /**
         * Elle prend un objet ConnectionDB en paramètre et retourne un objet Map<Integer, Moniteur>
         * 
         * @param bd la connexion à la base de données
         * @return Une carte des objets Moniteur
         */
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
            System.out.println("Aucune connexion");
        }
        return null;
    }
      
    public static Map<Integer,Cours> chargerCours(ConnectionDB bd){
        /**
         * Il prend un objet ConnectionDB en paramètre et renvoie un objet Map<Integer, Cours>
         * 
         * @param bd la connexion à la base de données
         * @return Une carte des objets Cours
         */
        try{
        Map<Integer, Cours> res = new HashMap<>();
        Statement s = bd.getConnection().createStatement();
        ResultSet Courss = s.executeQuery("select * from COURS");
        while(Courss.next()){
            res.put(Courss.getInt(1),new Cours(Courss.getInt(1), Courss.getString(2), Courss.getString(3), Courss.getString(4), (float) Courss.getDouble(5),Courss.getInt(6)));
            }


            return res;
        } catch(SQLException e1){
            System.out.println("Aucune connexion");
        }
        return null;
    }

    public static boolean insererReservations(ConnectionDB bd, Reservation uneReservation){
        /**
         * Il insère une réservation dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @param uneReservation l'objet de réservation
         * @return Un booléen
         */
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

            System.err.println("Il existe déjà une reservation avec cette date / ce client et ce poney");
            return false;
        }
    }
    

    public static boolean insererClient(ConnectionDB bd, Client unClient){
        /**
         * Il insère un client dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @param unClient l'objet client que nous voulons insérer dans la base de données
         * @return Une valeur booléenne.
         */
        PreparedStatement psClient;
        try {
            psClient = bd.getConnection().prepareStatement("insert into CLIENT values(?,?);");
            psClient.setInt(1, unClient.getId());
            psClient.setBoolean(2, unClient.getCotisation());
            psClient.executeUpdate();            
            return true;
        }
        catch (SQLException e) {
            System.out.println("L'id de la personne est déjà cliente");
            return false;
        }
    }
    
    public static boolean insererMoniteur(ConnectionDB bd, Moniteur unMoniteur){
        /**
         * Il insère une nouvelle ligne dans la table MONITEUR avec l'id de l'objet Moniteur passé en paramètre
         * 
         * @param bd la connexion à la base de données
         * @param unMoniteur l'objet Moniteur que l'on souhaite insérer dans la base de données
         * @return Une valeur booléenne.
         */
        PreparedStatement psMoniteur;
        try {
            psMoniteur = bd.getConnection().prepareStatement("INSERT INTO MONITEUR values(?);");
            psMoniteur.setInt(1, unMoniteur.getId());
            psMoniteur.executeUpdate();
            return true;
        }
        catch (SQLException e) {
            System.out.println("L'id de cette personne est déjà dans la table Moniteur");
            return false;
        }
    }


    public static boolean insererCours(ConnectionDB bd, Cours unCours){
        /**
         * Il insère un cours dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @param unCours L'objet de cours que nous voulons insérer dans la base de données.
         * @return Une valeur booléenne.
         */
        PreparedStatement ps;
        try {
            ps = bd.getConnection().prepareStatement("insert into COURS values(?, ?, ?, ?, ?,?);");

            ps.setInt(1, unCours.getId());
            ps.setString(2, unCours.getNomCours());
            ps.setString(3, unCours.getDescription());
            ps.setString(4, unCours.getTypeCours());
            ps.setFloat(5, unCours.getPrix());
            ps.setFloat(6,unCours.getIdMoniteur());

            ps.executeUpdate();
            return true;
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public static boolean insererPoney(ConnectionDB bd, Poney poney){
        /**
         * Il insère un poney dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @param poney le poney à insérer
         * @return Une valeur booléenne.
         */
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


    public static boolean insererPersonne(ConnectionDB bd, Personne personne) {
        /**
         * Il insère une personne dans la base de données
         * 
         * @param bd la connexion à la base de données
         * @param personne l'objet personne à insérer dans la base de données
         * @return Une valeur booléenne.
         */
        PreparedStatement psPersonne;
        try {
            psPersonne = bd.getConnection().prepareStatement("insert into PERSONNE values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);");


            psPersonne.setInt(1,personne.getId());
            psPersonne.setString(2, personne.getNom());
            psPersonne.setString(3, personne.getPrenom());

            java.util.Date utilDate = personne.getDateDeNaissance().getTime();
            java.sql.Date sqlDate = new java.sql.Date(utilDate.getTime());

            psPersonne.setDate(4, sqlDate);
            psPersonne.setFloat(5, personne.getPoids());
            psPersonne.setString(6, personne.getAdresseEmail());
            psPersonne.setString(7, personne.getAdresse());
            psPersonne.setInt(8, personne.getCodePostal());
            psPersonne.setString(9, personne.getVille());
            psPersonne.setString(10, personne.getNumTel());
            psPersonne.setString(11, personne.getMotdepasse());
            
            psPersonne.executeUpdate();
            return true;
        }
        catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }


    public static boolean supprimerReservations(ConnectionDB bd, Calendar calendrier, Integer idPersonne,
            Integer idCours){
        /**
         * Il supprime une réservation de la base de données
         * 
         * @param bd la connexion à la base de données
         * @param calendrier la date de la réservation
         * @param idPersonne l'identifiant de la personne qui a effectué la réservation
         * @param idCours l'identifiant du cours
         * @return Une valeur booléenne.
         */
        
        PreparedStatement psReserver;
        try {
            psReserver = bd.getConnection().prepareStatement("DELETE from RESERVER where jmahms=? and id =? and idpo=?");
            java.sql.Timestamp timestamp = new java.sql.Timestamp(calendrier.getTimeInMillis());
            psReserver.setTimestamp(1, timestamp);
            psReserver.setInt(2, idPersonne);
            psReserver.setInt(3, idCours);
            psReserver.executeUpdate();
            return true;
        }

        catch(SQLException e){
            e.printStackTrace();
            return false;
        }
    }


    public static boolean supprimerUnCours(ConnectionDB bd, int id) {
        /**
         * Il supprime un cours de la base de données
         * 
         * @param bd la connexion à la base de données
         * @param id l'id du cours à supprimer
         * @return Une valeur booléenne.
         */
        PreparedStatement psCours;
        try {
            if(bd.getConnection().createStatement().executeQuery("select * from RESERVER where idc = " + id).next()){
                bd.getConnection().createStatement().executeUpdate("DELETE from RESERVER where idc = " + id);
            }

            
            psCours = bd.getConnection().prepareStatement("DELETE from COURS where idc=?");
            psCours.setInt(1, id);
            psCours.executeUpdate();
            return true;
        }

        catch(SQLException e){
            e.printStackTrace();
            return false;
        }
    }


    public static boolean supprimerUnPoney(ConnectionDB bd, int id) {
        /**
         * Il supprime un poney de la base de données
         * 
         * @param bd la connexion à la base de données
         * @param id l'id du poney à supprimer
         * @return Un booléen
         */
        PreparedStatement psPoney;
        try {
            if(bd.getConnection().createStatement().executeQuery("select * from RESERVER where idpo = " + id).next()){
                bd.getConnection().createStatement().executeUpdate("DELETE from RESERVER where idpo = " + id);
            }
            psPoney = bd.getConnection().prepareStatement("DELETE from PONEYS where idpo=?");
            psPoney.setInt(1, id);
            psPoney.executeUpdate();
            return true;
        }

        catch(SQLException e){
            e.printStackTrace();
            return false;
        }
    }


    public static boolean supprimerUnePersonne(ConnectionDB bd, int id) {
        /**
         * Il supprime une personne de la base de données
         * 
         * @param bd Objet ConnectionDBConnectionDB object
         * @param id l'id de la personne à supprimer
         * @return Un booléen
         */
        PreparedStatement psPersonne;
        try {
            if(bd.getConnection().createStatement().executeQuery("select * from RESERVER where id = " + id).next()){
                bd.getConnection().createStatement().executeUpdate("DELETE from RESERVER where id= " + id);
            }
            if(bd.getConnection().createStatement().executeQuery("select * from MONITEUR where id = " + id).next()){
                if(bd.getConnection().createStatement().executeQuery("select * from COURS where id = " + id).next()){
                    ResultSet coursss = bd.getConnection().createStatement().executeQuery("select * from COURS where id = " + id);
                    while(coursss.next())
                        if(bd.getConnection().createStatement().executeQuery("select * from RESERVER where idc = "+coursss.getInt(1)).next()){
                            bd.getConnection().createStatement().executeUpdate("DELETE from RESERVER where idc = " + coursss.getInt(1));
                        }
                    bd.getConnection().createStatement().executeUpdate("DELETE from COURS where id = " + id);
                }
                bd.getConnection().createStatement().executeUpdate("DELETE from MONITEUR where id= " + id);
            }
            if(bd.getConnection().createStatement().executeQuery("select * from CLIENT where id = " + id).next()){
                bd.getConnection().createStatement().executeUpdate("DELETE from CLIENT where id= " + id);
            }
            psPersonne = bd.getConnection().prepareStatement("DELETE from PERSONNE where id=?");
            psPersonne.setInt(1, id);
            psPersonne.executeUpdate();
            return true;
        }

        catch(SQLException e){
            e.printStackTrace();
            return false;
        }
    }

}
