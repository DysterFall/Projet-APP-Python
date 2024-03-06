import hashlib
import random
import string
import sqlite3

class User:
    def __init__(self, first_name, last_name, email, phone, project_code, role, region):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.project_code = project_code
        self.role = role
        self.region = region

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_project_code(self):
        return self.project_code

    def get_role(self):
        return self.role

    def get_region(self):
        return self.region

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
        elif role_utilisateur == 'médecin':
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

    def create_user(self, first_name, last_name, email, phone, project_code, role, region):
        if role.lower() not in self.ROLES:
            print("Erreur : Le rôle spécifié n'est pas valide.")
            return None

        password = self.generate_password()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(first_name, last_name, email, phone, project_code, role, region)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (new_user.get_first_name(), new_user.get_last_name(), new_user.get_email(), new_user.get_phone(), new_user.get_project_code(), new_user.get_role(), new_user.get_region(), hashed_password))
        conn.commit()
        conn.close()
        return new_user

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        return password

    def modify_user(self, email, region=None, **kwargs):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            update_query = f"UPDATE users SET {', '.join([f'{key}=?' for key in kwargs.keys()])}"
            if region:
                update_query += ", region=?"
                cursor.execute(update_query, tuple(kwargs.values()) + (region, email))
            else:
                update_query += " WHERE email=?"
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
    
    def create_region(self, region_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO regions (region_name) VALUES (?)", (region_name,))
            conn.commit()
            print("Région créée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la création de la région :", e)
        finally:
            conn.close()


    def modify_region(self, old_region_name, new_region_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE regions SET region_name=? WHERE region_name=?", (new_region_name, old_region_name))
            conn.commit()
            print("Région modifiée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la modification de la région :", e)
        finally:
            conn.close()


    def delete_region(self, region_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM regions WHERE region_name=?", (region_name,))
            conn.commit()
            print("Région supprimée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la suppression de la région :", e)
        finally:
            conn.close()


    def create_unit(self, unit_name, region_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO units (unit_name, region_name) VALUES (?, ?)", (unit_name, region_name))
            conn.commit()
            print("Unité créée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la création de l'unité :", e)
        finally:
            conn.close()


    def modify_unit(self, old_unit_name, new_unit_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE units SET unit_name=? WHERE unit_name=?", (new_unit_name, old_unit_name))
            conn.commit()
            print("Unité modifiée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la modification de l'unité :", e)
        finally:
            conn.close()


    def delete_unit(self, unit_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM units WHERE unit_name=?", (unit_name,))
            conn.commit()
            print("Unité supprimée avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de la suppression de l'unité :", e)
        finally:
            conn.close()


    def assign_project_to_unit(self, project_code, unit_name):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET project_code=? WHERE unit_name=?", (project_code, unit_name))
            conn.commit()
            print("Projet affecté à l'unité avec succès.")
        except sqlite3.Error as e:
            print("Erreur lors de l'affectation du projet à l'unité :", e)
        finally:
            conn.close()


def afficher_menu_admin(user_manager):
    print("\nMenu :")
    print("1. Créer un utilisateur")
    print("2. Modifier un utilisateur")
    print("3. Supprimer un utilisateur")
    print("4. Consulter les utilisateurs")
    print("5. Créer une région")
    print("6. Modifier une région")
    print("7. Supprimer une région")
    print("8. Créer une unité")
    print("9. Modifier une unité")
    print("10. Supprimer une unité")
    print("11. Affecter un projet à une unité")
    print("12. Quitter l'application")

    choix = input("Choix : ")
    return choix

def login(username, password):
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT role, password FROM users WHERE email=?", (username,))
        row = cursor.fetchone()

        if row:
            role, hashed_password = row
            print("Rôle récupéré :", role)
            print("Mot de passe haché récupéré :", hashed_password)
            attempt = 0
            while attempt < 3:
                if hashed_password == hashlib.sha256(password.encode()).hexdigest():
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

username = input("Nom d'utilisateur : ")
password = input("Mot de passe : ")

user_role = login(username, password)
print("Rôle récupéré :", user_role)

if user_role == 'ADMIN':
    user_manager = UserManager('user.db')

elif user_role == 'user':
    print("Bienvenue utilisateur normal.")

else:
    print("Échec de la connexion.")

if user_role == 'ADMIN':
    user_manager = UserManager('user.db')

    while True:
        choix = choix = afficher_menu_admin(user_manager)

        if choix == '1':
            first_name = input("Entrez le prénom de l'utilisateur : ")
            last_name = input("Entrez le nom de famille de l'utilisateur : ")
            email = input("Entrez l'email de l'utilisateur : ")
            phone = input("Entrez le numéro de téléphone de l'utilisateur : ")
            project_code = input("Entrez le code du projet de l'utilisateur : ")
            role = input("Entrez le rôle de l'utilisateur : ")
            region = input("Entrez la région de l'utilisateur : ")

            nouvel_utilisateur = user_manager.create_user(first_name, last_name, email, phone, project_code, role, region)
            if nouvel_utilisateur:
                print("Utilisateur créé avec succès.")
            else:
                print("L'utilisateur n'a pas été créé en raison d'un rôle non valide.")

        elif choix == '2':
            email = input("Entrez l'email de l'utilisateur à modifier : ")
            print("Quels attributs souhaitez-vous modifier ?")
            print("1. Prénom")
            print("2. Nom de famille")
            print("3. Email")
            print("4. Numéro de téléphone")
            print("5. Code de projet")
            print("6. Rôle")
            print("7. Région")
            
            attributs_a_modifier = input("Entrez les numéros des attributs séparés par des virgules (ex: 1, 3, 5) : ")
            attributs_a_modifier = [int(x.strip()) for x in attributs_a_modifier.split(',')]
            
            modifications = {}
            
            if 1 in attributs_a_modifier:
                modifications['first_name'] = input("Nouveau prénom : ")
            if 2 in attributs_a_modifier:
                modifications['last_name'] = input("Nouveau nom de famille : ")
            if 3 in attributs_a_modifier:
                modifications['email'] = input("Nouvel email : ")
            if 4 in attributs_a_modifier:
                modifications['phone'] = input("Nouveau numéro de téléphone : ")
            if 5 in attributs_a_modifier:
                modifications['project_code'] = input("Nouveau code de projet : ")
            if 6 in attributs_a_modifier:
                new_role = input("Nouveau rôle : ")
                if new_role.lower() not in user_manager.ROLES:
                    print("Erreur : Le rôle spécifié n'est pas valide.")
                modifications['role'] = new_role
            if 7 in attributs_a_modifier:
                modifications['region'] = input("Nouvelle région : ")
            
            confirmation = input("Êtes-vous sûr de vouloir modifier cet utilisateur ? (oui/non) : ")
            if confirmation.lower() == "oui":
                user_manager.modify_user(email, **modifications)
                print("Utilisateur modifié avec succès.")
            else:
                print("Modification annulée.")


        elif choix == '3':
            email = input("Entrez l'email de l'utilisateur à supprimer : ")
            confirmation = input("Êtes-vous sûr de vouloir supprimer cet utilisateur ? (oui/non) : ")
            if confirmation.lower() == "oui":
                user_manager.delete_user(email)
                print("Utilisateur supprimé avec succès.")
            else:
                print("Suppression annulée.")

        elif choix == '4':
            user_manager.display_users()

        elif choix == '5':
            # Création d'une région
            region_name = input("Nom de la région : ")
            user_manager.create_region(region_name)

        elif choix == '6':
            # Modification d'une région
            old_region_name = input("Ancien nom de la région : ")
            new_region_name = input("Nouveau nom de la région : ")
            user_manager.modify_region(old_region_name, new_region_name)

        elif choix == '7':
            # Suppression d'une région
            region_name = input("Nom de la région à supprimer : ")
            user_manager.delete_region(region_name)

        elif choix == '8':
            # Création d'une unité
            unit_name = input("Nom de l'unité : ")
            region_name = input("Nom de la région de l'unité : ")
            user_manager.create_unit(unit_name, region_name)

        elif choix == '9':
            # Modification d'une unité
            old_unit_name = input("Ancien nom de l'unité : ")
            new_unit_name = input("Nouveau nom de l'unité : ")
            user_manager.modify_unit(old_unit_name, new_unit_name)

        elif choix == '10':
            # Suppression d'une unité
            unit_name = input("Nom de l'unité à supprimer : ")
            user_manager.delete_unit(unit_name)

        elif choix == '11':
            # Affecter un projet à une unité
            project_code = input("Code du projet : ")
            unit_name = input("Nom de l'unité : ")
            user_manager.assign_project_to_unit(project_code, unit_name)

        elif choix == '12':
            print("Quitting...")
            break