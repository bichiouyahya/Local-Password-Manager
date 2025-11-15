import json
import os
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

VAULT_FILE = "vault.json"
SALT_FILE = "salt.bin"


def load_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()

    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt


def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)


def main():
    salt = load_salt()

    master_password = getpass.getpass("Enter master password: ")
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    # Test correct password by verifying decryption of any entry
    if os.path.exists(VAULT_FILE) and os.path.getsize(VAULT_FILE) > 0:
        try:
            test_data = load_vault()
            if test_data:
                first_site = list(test_data.keys())[0]
                # try decrypt something; if fails → wrong password
                fernet.decrypt(test_data[first_site]["email"].encode())
        except:
            print("❌ Wrong master password!")
            return

    vault = load_vault()

    while True:
        command = input("\nCommand (add/get/delete/list/exit): ").lower()

        if command == "add":
            site = input("Site: ")
            email = input("Email: ")
            password = getpass.getpass("Password: ")

            vault[site] = {
                "email": fernet.encrypt(email.encode()).decode(),
                "password": fernet.encrypt(password.encode()).decode()
            }
            save_vault(vault)
            print("✔ Saved")

        elif command == "get":
            site = input("Site: ")
            if site in vault:
                try:
                    print("Email:", fernet.decrypt(vault[site]["email"].encode()).decode())
                    print("Password:", fernet.decrypt(vault[site]["password"].encode()).decode())
                except:
                    print("❌ Wrong master password!")
            else:
                print("No such site.")

        elif command == "list":
            print("\nSaved sites:")
            for s in vault:
                print(" -", s)

        elif command == "exit":
            break

        elif command == "delete":
            site = input("Site to delete: ")
            if site in vault:
                confirm = input(f"Are you sure you want to delete '{site}'? (y/n): ").lower()
                if confirm == "y":
                    del vault[site]
                    save_vault(vault)
                    print("✔ Deleted")
                else:
                    print("Cancelled.")
            else:
                print("No such site.")

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
