import java.util.Date;

public class Client extends Personne {
    private boolean cotisation;
        
    public Client(int id, String nom, String prenom, Date dateDeNaissance, float poids, String adresseEmail,
            String adresse, int codePostal, String ville, int numTel, String motDePasse, boolean cotisation) {
        super(id, nom, prenom, dateDeNaissance, poids, adresseEmail, adresse, codePostal, ville, numTel, motDePasse);
        this.cotisation = cotisation;
    }
    
}
