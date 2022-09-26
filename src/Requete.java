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

}
