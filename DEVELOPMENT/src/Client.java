import java.util.Calendar;

public class Client extends Personne {
    private boolean cotisation;
        
    public Client(int id, String nom, String prenom, Calendar dateDeNaissance, float poids, String adresseEmail,
            String adresse, int codePostal, String ville, String numTel, String motDePasse, boolean cotisation) {
        super(id, nom, prenom, dateDeNaissance, poids, adresseEmail, adresse, codePostal, ville, numTel, motDePasse);
        this.cotisation = cotisation;
        }

	public boolean getCotisation() {
		return this.cotisation;
	}

	public void setCotisation(boolean cotisation) {
		this.cotisation = cotisation;
	}


    
    @Override
    public String toString(){
        return this.cotisation?super.toString()+" il a cotisé": super.toString()+ "il n'a pas cosité";

    }
}
