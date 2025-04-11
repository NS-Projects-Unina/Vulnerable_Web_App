from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os
import json

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///challenges.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    
    from .models import User, Challenge, UserProgress

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    from .routes import main
    app.register_blueprint(main)

    
    with app.app_context():
        from flask_migrate import Migrate
        migrate = Migrate(app, db)
        db.create_all()

        if not Challenge.query.get(1):
            challenge1 = Challenge(
                id=1,
                name="Challenge 1- File Viewer 🔍",
                description="Sei stato incaricato di esplorare una web application che permette agli utenti di visualizzare file salvati sul server. Il tuo obiettivo è trovare un file nascosto utilizzando le informazioni fornite dalla web app. Usa la tua conoscenza delle vulnerabilità comuni per ottenere accesso a file altrimenti inaccessibili.",
                difficulty="Semplice",
                docker_image="challenge1_image",
                ports=json.dumps({"port": 5001}),
                flag="path_traversal_challenge_winner",
                points=50
            )
            db.session.add(challenge1)
            db.session.commit()
            print("✅ Challenge 1 inserita nel database.")

        if not Challenge.query.get(2):
            challenge2 = Challenge(
                id=2,
                name="Challenge 2 - COOKIES 🍪",
                description="Hai trovato un'app Flask in cui l'accesso alla flag è riservato all'utente admin. Sembra che l'autenticazione sia gestita tramite cookie non protetti. Riuscirai a sfruttare questa debolezza per diventare admin e rubare la flag?",
                difficulty="Semplice",
                docker_image="challenge2_image",
                ports=json.dumps({"port": 5002}),
                flag="cookie_monster",
                points=70
            )
            db.session.add(challenge2)
            db.session.commit()
            print("✅ Challenge 2 inserita nel database.")

        
        if not Challenge.query.get(3):
            challenge3 = Challenge(
                id=3,
                name="Challenge 3- Alice's Attack",
                description=" Una semplice applicazione Flask gestisce profili utenti con un database SQLite. C'è un utente chiamato Bob che ha qualcosa da nascondere... 👀 Riuscirai a bucare il login e accedere al suo profilo per scoprire la flag?",
                difficulty="Intermedia",
                docker_image="challenge3_image",
                ports=json.dumps({"port": 5003}),
                flag="flag_from_bob",
                points=100
            )
            db.session.add(challenge3)
            db.session.commit()
            print("✅ Challenge 3 inserita nel database.")

        if not Challenge.query.get(4):
            dos_challenge = Challenge(
                id=4,
                name="Challenge 4- Fake ADMIN 🧠",
                description="Hai davanti un'app Flask che usa JWT (JSON Web Tokens) per gestire l'autenticazione. Ogni utente riceve un token con un ruolo predefinito: user. Solo chi possiede un token con ruolo admin può leggere la flag! Ma... il segreto per firmare il token è troppo debole 😏",
                difficulty="Intermedia",
                docker_image="challenge4_image",
                ports=json.dumps({"port": 5004}),
                flag="jwt_secret_ch_fl",
                points=100
            )
            db.session.add(dos_challenge)
            db.session.commit()
            print("✅ Challenge 4 inserita nel database.")

        
        if not Challenge.query.get(5):
            wormblog_challenge = Challenge(
                id=5,
                name="Challenge 5 - WormBlog",
                description="Benvenuto su WormBlog, una semplice app di blogging in Flask. Chiunque può postare messaggi, ma solo l'admin ha accesso al cookie speciale che sblocca la flag. Peccato che i messaggi non vengano sanitizzati... 🪱 ",
                difficulty="Intermedia",
                docker_image="challenge5_image",  
                ports=json.dumps({"port": 5005}),
                flag="stored_xss_worm_executed",
                points=120
            )
            db.session.add(wormblog_challenge)
            db.session.commit()
            print("✅ Challenge 5 (WormBlog) inserita nel database.")

        
        if not Challenge.query.get(6):
            pingme_challenge = Challenge(
                id=6,
                name="Challenge 6 PingMe",
                description="PingMe è uno strumento diagnostico che permette agli utenti di controllare la connettività verso un indirizzo IP. Tuttavia, il backend esegue comandi di sistema usando direttamente l’input dell’utente... e senza sanitizzazione 😏",
                difficulty="Intermedia",
                docker_image="challenge6_image",  
                ports=json.dumps({"port": 5006}),
                flag="command_injection_achieved",
                points=80
            )
            db.session.add(pingme_challenge)
            db.session.commit()
            print("✅ Challenge 6 (PingMe) inserita nel database.")

    return app
