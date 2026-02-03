import requests
import time
import os

# ===================== COLORS =====================
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[96m"
W = "\033[97m"
RESET = "\033[0m"
# =================================================

os.system("clear")

# ===================== LOGO =====================
LOGO = f"""
{C}______    ___  ___ ___  ____  
|      |  /  _]|   |   ||    \\ 
|      | /  [_ | _   _ ||  o  )
|_|  |_||    _]|  \\_/  ||   _/ 
  |  |  |   [_ |   |   ||  |   
  |  |  |     ||   |   ||  |   
  |__|  |_____||___|___||__|   
{RESET}
"""
# ===============================================

# ===================== INFO BOX =================
INFO_BOX = f"""
{B}╔══════════════════════════════════════╗
║ {G}{W} {C}SALAMU ALAIKUM{B}              ║
║ {G}{W} {Y}MR MELAK{B}                    ║
║ {G}{W} {R}CYBER STRIKER TEAM{B}          ║
╚══════════════════════════════════════╝{RESET}
"""
# ===============================================

BASE_URL = "https://api.mail.tm"
HEADERS = {"Content-Type": "application/json"}


def get_domain():
    r = requests.get(f"{BASE_URL}/domains")
    r.raise_for_status()
    return r.json()["hydra:member"][0]["domain"]


def create_account():
    domain = get_domain()
    email = f"user{int(time.time())}@{domain}"
    password = "Pass1234!"

    r = requests.post(
        f"{BASE_URL}/accounts",
        json={"address": email, "password": password},
        headers=HEADERS
    )

    if r.status_code not in (200, 201):
        raise Exception("Account create failed")

    return email, password


def get_token(email, password):
    r = requests.post(
        f"{BASE_URL}/token",
        json={"address": email, "password": password},
        headers=HEADERS
    )
    r.raise_for_status()
    return r.json()["token"]


def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/messages", headers=headers)

    if r.status_code == 401:
        return "UNAUTHORIZED"

    r.raise_for_status()
    return r.json()["hydra:member"]


def read_message(token, msg_id):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=headers)
    r.raise_for_status()
    return r.json()


def main():
    print(LOGO)
    print(INFO_BOX)

    print(f"{Y}[*]{W} Creating temp mail...\n")

    email, password = create_account()
    token = get_token(email, password)

    print(f"{G}[✓]{W} Temp Email : {C}{email}{RESET}")
    print(f"{Y}[*]{W} Waiting for inbox...\n")

    while True:
        messages = get_messages(token)

        if messages == "UNAUTHORIZED":
            print(f"{R}[!]{W} Token expired! Re-authenticating...\n")
            token = get_token(email, password)
            time.sleep(2)
            continue

        if messages:
            print(f"{G}[📩]{W} {len(messages)} Mail Found\n")

            for msg in messages:
                full = read_message(token, msg["id"])

                print(f"{B}════════════════════════════════════{RESET}")
                print(f"{C}From   :{W} {full['from']['address']}")
                print(f"{C}Subject:{Y} {full['subject']}")
                print(f"{C}Body:{W}\n{full.get('text', '[No Text Body]')}")
                print(f"{B}════════════════════════════════════{RESET}")

            break

        time.sleep(5)


if __name__ == "__main__":
    main()
