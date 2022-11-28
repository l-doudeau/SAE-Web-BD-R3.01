import java.sql.*;

public class ConnectionDB{

    private Connection mysql;
    private boolean isConnected;

    public ConnectionDB() throws ClassNotFoundException{
        this.mysql = null;
        this.isConnected = false;
        // Class.forName("com.mysql.cj.jdbc.Driver");
        Class.forName("org.mariadb.jdbc.Driver");
    }
    public void connecter(String database, String username, String password) throws SQLException{
        this.mysql = null;
        this.isConnected = false;
        this.mysql = DriverManager.getConnection("jdbc:mysql://servinfo-mariadb/" + database, username , password); 
        this.isConnected = true;
    }

    public boolean isConnected(){
        return this.isConnected;
    }

    public Connection getConnection(){
        return this.mysql;
    }

    public void quit() throws SQLException{
        this.mysql.close();
        this.isConnected = false;

    }

    
}