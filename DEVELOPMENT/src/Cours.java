public class Cours {
    
    private int id;
    private String nomCours;
    private String description;
    private String typeCours;
    private float prix;
    private int idp;


    public Cours(int id, String nomCours, String description, String typeCours, float prix, int idp){
        this.id = id;
        this.nomCours = nomCours;
        this.description = description;
        this.typeCours = typeCours;
        this.prix = prix;
        this.idp = idp;
    }

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNomCours() {
        return this.nomCours;
    }

    public void setNomCours(String nomCours) {
        this.nomCours = nomCours;
    }

    public String getDescription() {
        return this.description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getTypeCours() {
        return this.typeCours;
    }

    public void setTypeCours(String typeCours) {
        this.typeCours = typeCours;
    }

    public float getPrix() {
        return this.prix;
    }

    public void setPrix(float prix) {
        this.prix = prix;
    }

    public float getIdMoniteur() {
        return this.idp;
    }

    public void setIdMoniteur(int idp) {
        this.idp = idp;
    }

    @Override
    public String toString(){
        return "\n"+this.id + " " +this.nomCours + " : \n" + this.description + "\n" + "Il coûte " + this.prix + " et est de type " + this.typeCours+"\nL'id du moniteur est :" +this.idp ;
    }

    @Override
    public boolean equals(Object obj){
        if(obj ==null ){ return false;}
        if(obj == this){ return true;}
        if(obj instanceof Cours){
            Cours cours2 = (Cours) obj;
            return cours2.id == this.id;
        }
        return false;
    }
}
