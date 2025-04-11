from app import create_app
from app.models import Challenge, db

app = create_app()

# Funzione per popolare il database con le challenge
def populate_database():
    with app.app_context():
        # Verifica se ci sono già challenge nel database
        if Challenge.query.count() == 0:
            # Definisci le challenge
            challenges = [
                {
                    "name": "Challenge 1 ",
                    "description": "Visualizza file arbitrari leggendo oltre la directory consentita.",
                    "difficulty": "Facile",
                    "docker_image": "challenge1_image",  # Nome dell'immagine Docker
                    "ports": "{}"
                },
                {
                    "name": "Challenge 2 ",
                    "description": "Cookie Monster !!.",
                    "difficulty": "Intermedio",
                    "docker_image": "challenge2_image",  # Nome dell'immagine Docker
                    "ports": "{}"  
                }
            ]

            # Aggiungi le challenge al database
            for challenge_data in challenges:
                challenge = Challenge(
                    name=challenge_data["name"],
                    description=challenge_data["description"],
                    difficulty=challenge_data["difficulty"],
                    docker_image=challenge_data["docker_image"],
                    ports=challenge_data["ports"]
                )
                db.session.add(challenge)
            db.session.commit()
            print("Challenge aggiunte con successo!")
        else:
            print("Il database contiene già delle challenge.")

# Popola il database all'avvio
populate_database()

# Esegui l'applicazione
if __name__ == '__main__':
    app.run(debug=True, port=5000)