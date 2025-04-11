# Vulnerable_Web_App
Vulnerable Web App è una piattaforma CTF, progettata per simulare attacchi informatici in un ambiente controllato e didattico. Gli utenti possono registrarsi, accedere e interagire con una serie di challenge di sicurezza offensive, ognuna ospitata in un container Docker isolato.
Ogni challenge rappresenta un diverso scenario di vulnerabilità (es. SQL Injection, XSS, Path Traversal), con l’obiettivo di ottenere una flag dimostrando di aver sfruttato correttamente la falla. 
In particolare :
- Challenge 1 : Una vulnerabilità di Path Traversal permette di accedere a file riservati nel server. L'obiettivo è leggere il file contenente la flag.
- Chellenge 2 : Una challenge basata sulla manipolazione dei cookie. Modificando i cookie di sessione, è possibile ottenere privilegi elevati e accedere alla flag.
- Challenge 3 : L’app permette agli utenti di modificare il proprio profilo, ma la query SQL che aggiorna la password è vulnerabile a SQL Injection.
- Challenge 4 : Il server utilizza token JWT con una chiave debole. L’obiettivo è forzare la firma di un token come admin e ottenere la flag.
- Challenge 5 : Un blog vulnerabile a XSS Worms. Iniettando uno script persistente, è possibile rubare i cookie dell’admin e ottenere la flag automaticamente.
- Challenge 6 : L’app web mostra una pagina con un form che ti chiede un IP da pingare. Il valore di ip viene inserito direttamente senza sanitizzazione questo apre la porta alla Command Injection.
 
Per creare e attivare l’ambiente virtuale :
python3 -m venv venv
source venv/bin/activate
 
pip install -r requirements.txt
 
Poi bisogna spostarsi in ongi cartella presente in docker_files (cd docker_files/challenge*) e buildare l'immagine della relativa challenge con il comando :
docker build -t challenge1_image.
Il procedimento va ripetuto per tutte le altre challenge, cambiando directory e l'immagine che sarà sempre ChallengeX_image. (X = numero della challenge)
 
Poi bisogna ritornare alla directory contenente il progetto e  avviare l'app con :
python3 run.py
