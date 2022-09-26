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

}
