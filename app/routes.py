from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User, Challenge, UserProgress, db
from .docker_manager import DockerManager
import json

main = Blueprint('main', __name__)
docker_manager = DockerManager()

# Registrazione utente
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Username e password richiesti'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username già esistente'}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return jsonify({'success': True, 'redirect': '/dashboard'})

# Pagina iniziale
@main.route('/')
def index():
    challenges = Challenge.query.all()
    return render_template('index.html', challenges=challenges)

#  Login utente
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e password richiesti'}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'success': True, 'redirect': '/dashboard'})

    return jsonify({'error': 'Credenziali non valide'}), 401

#  Dashboard utente
@main.route('/dashboard')
@login_required
def dashboard():
    challenges = Challenge.query.all()
    total_score = db.session.query(db.func.sum(UserProgress.score)).filter_by(user_id=current_user.id).scalar() or 0
    return render_template('dashboard.html', challenges=challenges, total_score=total_score)

#  Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Avvia un container Docker
@main.route('/start_container/<int:challenge_id>', methods=['POST'])
@login_required
def start_container(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404

    ports = json.loads(challenge.ports) if challenge.ports else {}
    port = ports.get("port", 5000 + challenge_id)

    container_info = docker_manager.launch_challenge(challenge.docker_image, current_user.id, challenge_id)

    if container_info:
        return jsonify({'success': True, 'url': f"http://localhost:{port}"})

    return jsonify({'error': 'Failed to start container'}), 500

#  Ferma un container Docker
@main.route('/stop_container/<int:challenge_id>', methods=['POST'])
@login_required
def stop_container(challenge_id):
    success = docker_manager.stop_challenge(current_user.id, challenge_id)

    if challenge_id == 1:
        return redirect(url_for('main.dashboard'))

    return jsonify({'success': success}) if success else jsonify({'error': 'Impossibile fermare il container'}), 500

# Route per inserimento flag
@main.route('/submit_flag/<int:challenge_id>', methods=['POST'])
@login_required
def submit_flag(challenge_id):
    submitted_flag = request.form.get('flag', '').strip()
    challenge = Challenge.query.get_or_404(challenge_id)

    progress = UserProgress.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    if progress and progress.completed:
        return jsonify(success=False, error="Hai già completato questa challenge!")

    if submitted_flag == challenge.flag:
        if not progress:
            progress = UserProgress(user_id=current_user.id, challenge_id=challenge_id)

        progress.completed = True
        progress.score = challenge.points
        db.session.add(progress)
        db.session.commit()
        return jsonify(success=True, message=f" Flag corretta! Hai guadagnato {challenge.points} punti.")
    else:
        return jsonify(success=False, error=" Flag errata. Riprova.")

#  Pagina "Inserisci Flag"
@main.route('/submit')
@login_required
def submit():
    challenges = Challenge.query.all()
    return render_template('submit_flag.html', challenges=challenges)

#  Ottieni punteggio totale
@main.route('/get_score', methods=['GET'])
@login_required
def get_score():
    total_score = db.session.query(db.func.sum(UserProgress.score)).filter_by(user_id=current_user.id).scalar() or 0
    return jsonify({'score': total_score})

#  Aggiorna punteggio (usando punti reali della challenge)
@main.route("/complete_challenge", methods=["POST"])
@login_required
def complete_challenge():
    data = request.get_json()
    challenge_id = data.get("challenge_id")

    if not challenge_id:
        return jsonify({"error": "ID della challenge mancante"}), 400

    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge non trovata"}), 404

    progress = UserProgress.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()

    if not progress:
        progress = UserProgress(user_id=current_user.id, challenge_id=challenge_id, completed=True, score=challenge.points)
        db.session.add(progress)
    elif not progress.completed:
        progress.completed = True
        progress.score = challenge.points

    db.session.commit()
    return jsonify({"success": True, "message": f"Punteggio aggiornato: +{challenge.points} punti!"})

@main.route('/leaderboard')
@login_required
def leaderboard():
    leaderboard_data = (
        db.session.query(User.username, db.func.sum(UserProgress.score).label("total_score"))
        .join(UserProgress, User.id == UserProgress.user_id)
        .group_by(User.id)
        .order_by(db.func.sum(UserProgress.score).desc())
        .all()
    )
    return render_template('leaderboard.html', leaderboard=leaderboard_data)
