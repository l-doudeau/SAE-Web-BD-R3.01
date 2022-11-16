import java.sql.Time;
import java.util.Calendar;
public class Reservation {
    
    private Calendar date;
    private int idPersonne;
    private int idCours;
    private int idPoney;
    private Time duree;
    private boolean aPaye;
    

    public Reservation(Calendar date, int idPersonne, int idCours, int idPoney, Time duree, boolean aPaye){
        this.date = date;
        this.idPersonne = idPersonne;
        this.idCours = idCours;
        this.idPoney = idPoney;
        this.duree = duree;
        this.aPaye = aPaye;
    }
    public Calendar getDate() {
        return this.date;
    }

    public void setDate(Calendar date) {
        this.date = date;
    }

    public int getIdPersonne() {
        return this.idPersonne;
    }

    public void setIdPersonne(int idPersonne) {
        this.idPersonne = idPersonne;
    }

    public int getIdCours() {
        return this.idCours;
    }

    public void setIdCours(int idCours) {
        this.idCours = idCours;
    }

    public int getIdPoney() {
        return this.idPoney;
    }

    public void setIdPoney(int idPoney) {
        this.idPoney = idPoney;
    }

    public Time getDuree() {
        return this.duree;
    }

    public void setDuree(Time duree) {
        this.duree = duree;
    }

    public boolean isAPaye() {
        return this.aPaye;
    }

    public boolean getAPaye() {
        return this.aPaye;
    }

    public void setAPaye(boolean aPaye) {
        this.aPaye = aPaye;
    }

    @Override
    public boolean equals(Object obj){
        if(obj ==null ){ return false;}
        if(obj == this){ return true;}
        if(obj instanceof Reservation){
            Reservation reservation2 = (Reservation) obj;
            return reservation2.idCours == this.idCours && reservation2.idPersonne == this.idPersonne && reservation2.idPoney == this.idPoney && reservation2.date == this.date;
        }
        return false;
    }
}
