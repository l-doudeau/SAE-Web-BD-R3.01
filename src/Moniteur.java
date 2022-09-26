import java.util.Date;

public class Moniteur extends Personne {

    public Moniteur(int id, String nom, String prenom, Date dateDeNaissance, float poids, String adresseEmail, String adresse, int codePostal, String ville, int numTel, String motDePasse){
        super(id, nom, prenom, dateDeNaissance, poids, adresseEmail, adresse, codePostal, ville, numTel, motDePasse);
    }
}
