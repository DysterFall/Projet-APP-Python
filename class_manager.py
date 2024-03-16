import hashlib
import random
import string
import sqlite3

class User:
    def __init__(self, first_name, last_name, email, phone, project_code, role, region, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.project_code = project_code
        self.role = role
        self.region = region
        self.password = password

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, new_first_name):
        self.first_name = new_first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, new_last_name):
        self.last_name = new_last_name

    def get_email(self):
        return self.email

    def set_email(self, new_email):
        self.email = new_email

    def get_phone(self):
        return self.phone

    def set_phone(self, new_phone):
        self.phone = new_phone

    def get_project_code(self):
        return self.project_code

    def set_project_code(self, new_project_code):
        self.project_code = new_project_code

    def get_role(self):
        return self.role

    def set_role(self, new_role):
        self.role = new_role

    def get_region(self):
        return self.region

    def set_region(self, new_region):
        self.region = new_region

    def get_password(self):
        return self.password

    def set_password(self, new_password):
        self.password = new_password

class UserManager:
    ROLES = ['chercheur', 'medecin', 'commercial', 'assistant']

    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def actions_chercheur(self, email_utilisateur):
        print("Fonctionnalités pour les chercheurs :")
        print("- Accès aux documents de recherche en lecture et écriture.")
        print("- Possibilité de travailler dans plusieurs unités.")

    def actions_medecin(self, email_utilisateur):
        print("Fonctionnalités pour les médecins :")
        print("- Accès aux résultats des tests de laboratoire.")

    def actions_commercial(self, email_utilisateur):
        print("Fonctionnalités pour les commerciaux :")
        print("- Accès aux caractéristiques et aux avantages des médicaments en lecture seule.")

    def actions_assistant(self, email_utilisateur):
        print("Fonctionnalités pour les assistants :")
        print("- Fonctionnalités à définir pour les assistants.")

    def actions_specifiques_utilisateur(self, role_utilisateur, email_utilisateur):
        if role_utilisateur == 'chercheur':
            self.actions_chercheur(email_utilisateur)
        elif role_utilisateur == 'medecin':
            self.actions_medecin(email_utilisateur)
        elif role_utilisateur == 'commercial':
            self.actions_commercial(email_utilisateur)
        elif role_utilisateur == 'assistant':
            self.actions_assistant(email_utilisateur)
        else:
            print("Rôle non reconnu.")

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, password TEXT, region TEXT)''')
        conn.commit()
        conn.close()

    def create_user(self, first_name, last_name, email, phone, project_code, role, region, password):
        if role.lower() not in self.ROLES:
            print("Erreur : Le rôle spécifié n'est pas valide.")
            return None

        hashed_password = self.hash_password(password)
        new_user = User(first_name, last_name, email, phone, project_code, role, region, hashed_password)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (new_user.get_first_name(), new_user.get_last_name(), new_user.get_email(), new_user.get_phone(), new_user.get_project_code(), new_user.get_role(), new_user.get_region(), new_user.get_password()))
        conn.commit()
        conn.close()
        return new_user

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def modify_user(self, email, **kwargs):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            update_query = f"UPDATE users SET {', '.join([f'{key}=?' for key in kwargs.keys()])} WHERE email=?"

            cursor.execute(update_query, tuple(kwargs.values()) + (email,))
            conn.commit()
            print("Utilisateur modifié avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la modification de l'utilisateur :", e)
        finally:
            conn.close()

    def delete_user(self, email):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE email=?", (email,))
            conn.commit()
            print("Utilisateur supprimé avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la suppression de l'utilisateur :", e)
        finally:
            conn.close()

    def display_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Nom: {row[0]}, Nom de famille: {row[1]}, Email: {row[2]}, Téléphone: {row[3]}, Code de projet: {row[4]}, Rôle: {row[5]}, Region: {row[6]}")
        conn.close()

    def afficher_menu_admin(self):
        print("\nMenu :")
        print("1. Créer un utilisateur")
        print("2. Modifier un utilisateur")
        print("3. Supprimer un utilisateur")
        print("4. Consulter les utilisateurs")
        print("5. Quitter l'application")

        choix = input("Choix : ")
        return choix

    def login(self, username, password):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT role, password FROM users WHERE email=?", (username,))
            row = cursor.fetchone()

            if row:
                role, hashed_password = row
                attempt = 0
                while attempt < 3:
                    if hashed_password == self.hash_password(password):
                        print("Connexion réussie.")
                        return role 
                    else:
                        attempt += 1
                        print("Mot de passe incorrect. Tentative", attempt, "sur 3.")
                        password = input("Veuillez réessayer le mot de passe : ")
                print("Trop de tentatives infructueuses. Veuillez réessayer plus tard.")
                return None
            else:
                print("Utilisateur non trouvé.")
                return None
        except sqlite3.Error as e:
            print("Erreur lors de la connexion :", e) 
            return None
        finally:
            conn.close()
