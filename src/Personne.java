import java.util.Calendar;

public class Personne {
    
    private int id;
    private String nom;
    private String prenom;
    private Calendar dateDeNaissance;
    private float poids;
    private String adresseEmail;
    private String adresse;
    private int codePostal;
    private String ville;
    private String numTel;
    private String motdepasse;


    public Personne(int id, String nom, String prenom, Calendar dateDeNaissance, float poids, String adresseEmail, String adresse, int codePostal, String ville, String numTel, String motDePasse){
        this.id = id;
        this.nom = nom;
        this.prenom = prenom;
        this.dateDeNaissance = dateDeNaissance;
        this.poids = poids;
        this.adresseEmail = adresseEmail;
        this.adresse = adresse;
        this.codePostal = codePostal;
        this.ville = ville;
        this.numTel = numTel; 
        this.motdepasse = motDePasse;
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

    public String getPrenom() {
        return this.prenom;
    }

    public void setPrenom(String prenom) {
        this.prenom = prenom;
    }

    public Calendar getDateDeNaissance() {
        return this.dateDeNaissance;
    }

    public void setDateDeNaissance(Calendar dateDeNaissance) {
        this.dateDeNaissance = dateDeNaissance;
    }

    public float getPoids() {
        return this.poids;
    }

    public void setPoids(float poids) {
        this.poids = poids;
    }

    public String getAdresseEmail() {
        return this.adresseEmail;
    }

    public void setAdresseEmail(String adresseEmail) {
        this.adresseEmail = adresseEmail;
    }

    public String getAdresse() {
        return this.adresse;
    }

    public void setAdresse(String adresse) {
        this.adresse = adresse;
    }

    public int getCodePostal() {
        return this.codePostal;
    }

    public void setCodePostal(int codePostal) {
        this.codePostal = codePostal;
    }

    public String getVille() {
        return this.ville;
    }

    public void setVille(String ville) {
        this.ville = ville;
    }

    public String getNumTel() {
        return this.numTel;
    }

    public void setNumTel(String numTel) {
        this.numTel = numTel;
    }

    public String getMotdepasse() {
        return this.motdepasse;
    }

    public void setMotdepasse(String motdepasse) {
        this.motdepasse = motdepasse;
    }


    @Override
    public String toString(){
        return "Le client d'ID = " + this.id + ", s'appelle " + this.nom + " " + this.prenom + ", habite à : " + this.ville + " au " + this.adresse + " " + this.codePostal + ". Il est joignable au " + this.numTel + " ou par mail au " + this.adresseEmail + "\n"; 
    }
    @Override
    public boolean equals(Object obj){
        if(obj ==null ){ return false;}
        if(obj == this){ return true;}
        if(obj instanceof Personne){
            Personne personne2 = (Personne) obj;
            return this.id == personne2.id;
        }
        return false;
    }
}
