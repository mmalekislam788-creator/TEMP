import requests
import time

BASE = "https://api.mail.tm"

HEADERS = {
    "Content-Type": "application/json"
}

def get_domain():
    r = requests.get(f"{BASE}/domains")
    return r.json()["hydra:member"][0]["domain"]

def create_account():
    domain = get_domain()
    email = f"user{int(time.time())}@{domain}"
    password = "Pass1234!"

    r = requests.post(
        f"{BASE}/accounts",
        json={"address": email, "password": password},
        headers=HEADERS
    )

    return email, password

def get_token(email, password):
    r = requests.post(
        f"{BASE}/token",
        json={"address": email, "password": password},
        headers=HEADERS
    )
    return r.json()["token"]

def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/messages", headers=headers)
    return r.json()["hydra:member"]

def read_message(token, msg_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/messages/{msg_id}", headers=headers)
    return r.json()

def main():
    print("Creating temp mail...\n")

    email, password = create_account()
    token = get_token(email, password)

    print("Temp Email:", email)
    print("Waiting for inbox...\n")

    while True:
        msgs = get_messages(token)
        if msgs:
            print(f"📩 {len(msgs)} Mail Found\n")
            for m in msgs:
                msg = read_message(token, m["id"])
                print("From   :", msg["from"]["address"])
                print("Subject:", msg["subject"])
                print("Body:\n", msg["text"])
                print("-" * 40)
            break
        time.sleep(5)

if __name__ == "__main__":
    main()
