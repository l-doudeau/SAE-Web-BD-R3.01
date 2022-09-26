import java.time.LocalTime;
import java.util.Date;

public class Reservation {
    
    private Date date;
    private int idPersonne;
    private int idCours;
    private int idPoney;
    private LocalTime duree;
    private boolean aPaye;
    

    public Reservation(Date date, int idPersonne, int idCours, int idPoney, LocalTime duree, boolean aPaye){
        this.date = date;
        this.idPersonne = idPersonne;
        this.idCours = idCours;
        this.idPoney = idPoney;
        this.duree = duree;
        this.aPaye = aPaye;
    }
    public Date getDate() {
        return this.date;
    }

    public void setDate(Date date) {
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

    public LocalTime getDuree() {
        return this.duree;
    }

    public void setDuree(LocalTime duree) {
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
