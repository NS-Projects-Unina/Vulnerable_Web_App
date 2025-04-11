import docker
import os
import time

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            print("✅ Connessione a Docker riuscita!")
        except Exception as e:
            print(f" Errore nella connessione a Docker: {e}")

    def launch_challenge(self, image_name, user_id, challenge_id):
        container_name = f"challenge_{user_id}_{challenge_id}"

       
        challenge_ports = {
            2: 5002,
            3: 5003,
            4: 5004,
            5: 5005,
            6: 5006
        }
        selected_port = challenge_ports.get(challenge_id, 5001)

        try:
            print(f"Controllo se il container {container_name} esiste...")
            existing_containers = self.client.containers.list(all=True, filters={"name": container_name})

            if existing_containers:
                container = existing_containers[0]
                print(f"Container trovato! Stato attuale: {container.status}")

                if container.status == "running":
                    print(f"Il container {container_name} è già in esecuzione.")
                    return {"id": container.id, "port": selected_port}

                elif container.status == "exited":
                    print(f"Il container {container_name} è fermo. Riavvio in corso...")
                    container.start()
                    time.sleep(3)
                    container.reload()
                    print(f"Container {container_name} riavviato correttamente su http://localhost:{selected_port}")
                    return {"id": container.id, "port": selected_port}

            # Percorso assoluto della cartella della challenge
            host_path = os.path.abspath(f"./docker_files/challenge{challenge_id}")
            print(f"Montando volume da {host_path}")



            # Se il container non esiste viene creato
            if challenge_id == 5:
                # Percorsi per app e admin bot
                app_path = os.path.abspath("./docker_files/challenge5/app")
                bot_path = os.path.abspath("./docker_files/challenge5/admin_bot")

                # Avvia container dell'app
                print(f"Avvio container app per Challenge 5: {container_name}_app")
                app_container = self.client.containers.run(
                    image="challenge5_image",
                    name=f"{container_name}_app",
                    detach=True,
                    tty=True,
                    ports={5000: selected_port},
                    volumes={app_path: {'bind': '/app', 'mode': 'rw'}},
                    working_dir="/app",
                    environment={"FLASK_ENV": "development"},
                    command=["python", "app.py"]
                )

                time.sleep(3)
                app_container.reload()
                print(f"App Challenge 5 avviata su http://localhost:{selected_port}")

                #Avvio admin bot
                print(f" Avvio admin bot per Challenge 5: {container_name}_adminbot")
                adminbot_container = self.client.containers.run(
                    image="adminbot5_image",
                    name=f"{container_name}_adminbot",
                    detach=True,
                    tty=True,
                    volumes={bot_path: {'bind': '/bot', 'mode': 'rw'}},
                    working_dir="/bot",
                    network_mode="bridge",
                    links={f"{container_name}_app": "wormblog"},
                    command=["python3", "admin_bot.py"]
                )

                print("Admin bot Challenge 5 avviato correttamente.")
                return {"id": app_container.id, "port": selected_port}

            print(f"Creazione del container {container_name} per challenge {challenge_id}...")
            container = self.client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                tty=True,
                ports={5000: selected_port},
                volumes={host_path: {'bind': f"/challenge{challenge_id}", 'mode': 'rw'}},
                working_dir=f"/challenge{challenge_id}",
                environment={"FLASK_ENV": "development"},
                command=["python", "app.py"]
            )

            time.sleep(3)
            container.reload()

            print(f"Container {container_name} avviato su http://localhost:{selected_port}")
            return {"id": container.id, "port": selected_port}

        except Exception as e:
            print(f" ERRORE Docker: {e}")
            return None
