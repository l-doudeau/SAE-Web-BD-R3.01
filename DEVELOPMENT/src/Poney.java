public class Poney {
    

    private int id;
    private String nom;
    private float poidsSupporte;
    
    public Poney(int id, String nom, float poidsSupporte){
        this.id = id;
        this.nom = nom;
        this.poidsSupporte = poidsSupporte;
    }
    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNom() {
        return this.nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public float getPoidsSupporte() {
        return this.poidsSupporte;
    }

    public void setPoidsSupporte(float poidsSupporte) {
        this.poidsSupporte = poidsSupporte;
    }
    @Override
    public String toString(){
        return this.nom + " peut supporter un poids de " + this.poidsSupporte;
    }
    @Override
    public boolean equals(Object obj){
        if(obj ==null ){ return false;}
        if(obj == this){ return true;}
        if(obj instanceof Poney){
            Poney poney2 = (Poney) obj;
            return poney2.id == this.id;
        }
        return false;
    }
}
