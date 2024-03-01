import hashlib
import random
import string
import sqlite3

class User:
    def __init__(self, first_name, last_name, email, phone, project_code, role):
        self.__first_name = first_name
        self.__last_name = last_name
        self.email = email
        self.phone = phone
        self.project_code = project_code
        self.role = role
        self.password = self.generate_password()
        self.login = self.generate_login()

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_login(self):
        return self.__first_name[0].lower() + self.__last_name.lower()

    def get_last_name(self):
        return self.__last_name
    
    def get_name(self):
        return self.__first_name

    def get_login(self):
        return self.login

class UserManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, password TEXT)''')
        conn.commit()
        conn.close()

    def create_user(self, first_name, last_name, email, phone, project_code, role):
        user = User(first_name, last_name, email, phone, project_code, role)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user.get_name(), user.get_last_name(), user.email, user.phone, user.project_code, user.role, user.password))
        conn.commit()
        conn.close()
        return user

    def modify_user(self, email, **kwargs):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f"UPDATE users SET {key}=? WHERE email=?", (value, email))
        conn.commit()
        conn.close()

    def delete_user(self, email):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        conn.close()

    def display_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Nom: {row[0]}, Nom de famille: {row[1]}, Email: {row[2]}, Téléphone: {row[3]}, Code de projet: {row[4]}, Rôle: {row[5]}, Mot de passe: {row[6]}")
        conn.close()

# Fonction pour afficher le menu et traiter les choix de l'utilisateur
def afficher_menu(user_manager):
    print("\nMenu :")
    print("1. Créer un utilisateur")
    print("2. Modifier un utilisateur")
    print("3. Supprimer un utilisateur")
    print("4. Consulter les utilisateurs")
    print("5. Quitter l'application")

    choix = input("Choix : ")
    return choix

# Vérifier les identifiants de l'utilisateur avant de lui permettre d'accéder au menu
def login():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT role, password FROM users WHERE email=?", (username,))
        row = cursor.fetchone()

        if row:
            role, hashed_password = row
            if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                print("Connexion réussie.")
                return role  # Retourner le rôle de l'utilisateur
            else:
                print("Mot de passe incorrect.")
                return None
        else:
            print("Utilisateur non trouvé.")
            return None
    except sqlite3.Error as e:
        print("Erreur lors de la connexion :", e)
        return None
    finally:
        conn.close()

# Utilisation de la fonction pour se connecter
user_role = login()

if user_role == 'admin':
    user_manager = UserManager('user.db')
    # Reste du code pour l'interface utilisateur administrateur
elif user_role == 'user':
    print("Bienvenue utilisateur normal.")
    # Code pour l'interface utilisateur normal
else:
    print("Accès refusé.")

# Utilisation de la fonction pour se connecter en tant qu'administrateur
# Utilisation de la fonction pour se connecter en tant qu'administrateur
if user_role == 'admin':
    user_manager = UserManager('user.db')

    while True:
        choix = afficher_menu(user_manager)

        # Sous le bloc while True dans le menu administrateur
        if choix == '1':
            first_name = input("Entrez le prénom de l'utilisateur : ")
            last_name = input("Entrez le nom de famille de l'utilisateur : ")
            email = input("Entrez l'email de l'utilisateur : ")
            phone = input("Entrez le numéro de téléphone de l'utilisateur : ")
            project_code = input("Entrez le code du projet de l'utilisateur : ")
            role = input("Entrez le rôle de l'utilisateur : ")

            nouvel_utilisateur = user_manager.create_user(first_name, last_name, email, phone, project_code, role)
            print("Utilisateur créé avec succès.")

        elif choix == '2':
            email = input("Entrez l'email de l'utilisateur à modifier : ")
            # Vous pouvez ajouter d'autres inputs pour les autres attributs à modifier
            user_manager.modify_user(email)  # Mettez les autres attributs à modifier comme arguments ici
            print("Utilisateur modifié avec succès.")

        elif choix == '3':
            email = input("Entrez l'email de l'utilisateur à supprimer : ")
            user_manager.delete_user(email)
            print("Utilisateur supprimé avec succès.")

        elif choix == '4':
            user_manager.display_users()

        elif choix == '5':
            print("Quitting...")
            break  # Sortir de la boucle while et terminer le programme


