import java.util.Calendar;

public class Moniteur extends Personne {

    public Moniteur(int id, String nom, String prenom, Calendar dateDeNaissance, float poids, String adresseEmail, String adresse, int codePostal, String ville, String numTel, String motDePasse){
        super(id, nom, prenom, dateDeNaissance, poids, adresseEmail, adresse, codePostal, ville, numTel, motDePasse);
    }
    @Override
    public String toString(){
        return super.toString();
    }
}
