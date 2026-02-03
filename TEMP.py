import requests
import time

# ===================== LOGO =====================
LOGO = r"""
______    ___  ___ ___  ____  
|      |  /  _]|   |   ||    \ 
|      | /  [_ | _   _ ||  o  )
|_|  |_||    _]|  \_/  ||   _/ 
  |  |  |   [_ |   |   ||  |   
  |  |  |     ||   |   ||  |   
  |__|  |_____||___|___||__|  
"""
# =================================================

BASE_URL = "https://api.mail.tm"
HEADERS = {"Content-Type": "application/json"}


def get_domain():
    response = requests.get(f"{BASE_URL}/domains")
    response.raise_for_status()
    return response.json()["hydra:member"][0]["domain"]


def create_account():
    domain = get_domain()
    email = f"user{int(time.time())}@{domain}"
    password = "Pass1234!"

    requests.post(
        f"{BASE_URL}/accounts",
        json={"address": email, "password": password},
        headers=HEADERS
    )

    return email, password


def get_token(email, password):
    response = requests.post(
        f"{BASE_URL}/token",
        json={"address": email, "password": password},
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["token"]


def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    response.raise_for_status()
    return response.json()["hydra:member"]


def read_message(token, message_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/messages/{message_id}",
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def main():
    print(LOGO)
    print("Creating temp mail...\n")

    email, password = create_account()
    token = get_token(email, password)

    print(f"Temp Email : {email}")
    print("Waiting for inbox...\n")

    while True:
        messages = get_messages(token)

        if messages:
            print(f"📩 {len(messages)} Mail Found\n")

            for msg in messages:
                full_msg = read_message(token, msg["id"])
                print("From   :", full_msg["from"]["address"])
                print("Subject:", full_msg["subject"])
                print("Body:\n", full_msg.get("text", "[No Text Body]"))
                print("-" * 40)

            break

        time.sleep(5)


if __name__ == "__main__":
    main()
