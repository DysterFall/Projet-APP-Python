import hashlib
import sqlite3
import random
import string
#testtest
# Classe représentant un utilisateur
class User:
    # Constructeur de la classe User
    def __init__(self, first_name, last_name, email, phone, project_code, role, region, password, login):
        # Initialisation des attributs de l'utilisateur
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone = phone
        self.__project_code = project_code
        self.__role = role
        self.__region = region
        self.__password = password
        self.__login = login 

    # Méthodes pour obtenir et définir le prénom de l'utilisateur
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, new_first_name):
        self.__first_name = new_first_name

    # Méthodes similaires pour les autres attributs de l'utilisateur...
    def get_last_name(self):
            return self.__last_name

    def set_last_name(self, new_last_name):
        self.__last_name = new_last_name

    def get_email(self):
        return self.__email

    def set_email(self, new_email):
        self.__email = new_email

    def get_phone(self):
        return self.__phone

    def set_phone(self, new_phone):
        self.__phone = new_phone

    def get_project_code(self):
        return self.__project_code

    def set_project_code(self, new_project_code):
        self.__project_code = new_project_code

    def get_role(self):
        return self.__role

    def set_role(self, new_role):
        self.__role = new_role

    def get_region(self):
        return self.__region

    def set_region(self, new_region):
        self.__region = new_region

    def get_password(self):
        return self.__password

    def set_password(self, new_password):
        self.__password = new_password

    def get_login(self):
        return self.__login

    def set_login(self, new_login):
        self.__login = new_login

# Classe gérant les utilisateurs
class UserManager:
    ROLES = ['chercheur', 'medecin', 'commercial', 'assistant']

    # Constructeur de la classe UserManager
    def __init__(self, db_file):
        # Initialise le nom du fichier de base de données et crée la table des utilisateurs si elle n'existe pas
        self.db_file = db_file
        self.create_table()

    # Méthodes pour les fonctionnalités spécifiques aux différents rôles d'utilisateurs
    def actions_chercheur(self, email_utilisateur):
        # Affiche les fonctionnalités pour les chercheurs
        print("Fonctionnalités pour les chercheurs :")
        print("- Accès aux documents de recherche en lecture et écriture.")
        print("- Possibilité de travailler dans plusieurs unités.")

    def actions_medecin(self, email_utilisateur):
        # Affiche les fonctionnalités pour les médecins
        print("Fonctionnalités pour les médecins :")
        print("- Accès aux résultats des tests de laboratoire.")

    def actions_commercial(self, email_utilisateur):
        # Affiche les fonctionnalités pour les commerciaux
        print("Fonctionnalités pour les commerciaux :")
        print("- Accès aux caractéristiques et aux avantages des médicaments en lecture seule.")

    def actions_assistant(self, email_utilisateur):
        # Affiche les fonctionnalités pour les assistants
        print("Fonctionnalités pour les assistants :")
        print("- Fonctionnalités à définir pour les assistants.")

    # Méthode pour appeler les actions spécifiques selon le rôle de l'utilisateur
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

    # Méthode pour créer la table des utilisateurs dans la base de données
    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, password TEXT, region TEXT, login TEXT)''')
        conn.commit()
        conn.close()

    # Méthode pour créer un nouvel utilisateur dans la base de données
    def create_user(self, first_name, last_name, email, phone, project_code, role, region, password, login):
        if role.lower() not in self.ROLES:
            print("Erreur : Le rôle spécifié n'est pas valide.")
            return None
    
        hashed_password = self.hash_password(password)
        new_user = User(first_name, last_name, email, phone, project_code, role, region, hashed_password, login)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (new_user.get_first_name(), new_user.get_last_name(), new_user.get_email(), new_user.get_phone(), new_user.get_project_code(), new_user.get_role(), new_user.get_region(), new_user.get_password(), new_user.get_login()))
        conn.commit()
        conn.close()
        return new_user

    # Méthode pour hacher le mot de passe avec SHA-256
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Méthode pour modifier les détails d'un utilisateur dans la base de données
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

    # Méthode pour supprimer un utilisateur de la base de données
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

    # Méthode pour afficher tous les utilisateurs présents dans la base de données
    def display_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Nom: {row[0]}, Nom de famille: {row[1]}, Email: {row[2]}, Téléphone: {row[3]}, Code de projet: {row[4]}, Rôle: {row[5]}, Region: {row[6]}")
        conn.close()

    # Méthode pour afficher le menu d'administration pour les utilisateurs autorisés
    def afficher_menu_admin(self):
        print("\nMenu :")
        print("1. Créer un utilisateur")
        print("2. Modifier un utilisateur")
        print("3. Supprimer un utilisateur")
        print("4. Consulter les utilisateurs")
        print("5. Quitter l'application")

        choix = input("Choix : ")
        return choix

    # Méthode pour vérifier les informations d'identification de l'utilisateur lors de la connexion
    def login(self, login, password):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT role, password FROM users WHERE login=?", (login,))
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
