import hashlib
import sqlite3
from class_manager import UserManager  # Import de la classe UserManager depuis un autre fichier

# Demande à l'utilisateur de saisir son nom d'utilisateur et son mot de passe
username = input("Nom d'utilisateur : ")
password = input("Mot de passe : ")

# Création d'une instance de UserManager en utilisant la base de données 'user.db'
user_manager = UserManager('user.db')

# Utilisation de la méthode login pour vérifier les informations d'identification
user_role = user_manager.login(username, password)

# Si l'utilisateur est un administrateur
if user_role == 'ADMIN':
    while True:
        # Affichage du menu administrateur
        choix = user_manager.afficher_menu_admin()

        # Créer un nouvel utilisateur
        if choix == '1':
            # Saisie des informations de l'utilisateur
            first_name = input("Entrez le prénom de l'utilisateur : ")
            last_name = input("Entrez le nom de famille de l'utilisateur : ")
            email = input("Entrez l'email de l'utilisateur : ")
            phone = input("Entrez le numéro de téléphone de l'utilisateur : ")
            project_code = input("Entrez le code du projet de l'utilisateur : ")
            role = input("Entrez le rôle de l'utilisateur : ")
            region = input("Entrez la région de l'utilisateur : ")
            new_password = input("Entrez le mot de passe de l'utilisateur : ")

            # Création d'un nouvel utilisateur avec les informations saisies
            nouvel_utilisateur = user_manager.create_user(first_name, last_name, email, phone, project_code, role, region, new_password)
            if nouvel_utilisateur:
                print("Utilisateur créé avec succès.")
            else:
                print("L'utilisateur n'a pas été créé en raison d'un rôle non valide.")

        # Modifier un utilisateur existant
        elif choix == '2':
            email = input("Entrez l'email de l'utilisateur à modifier : ")

            # Demande des attributs à modifier
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
            
            # Modifier les attributs sélectionnés
            modifications = {}
            if 1 in attributs_a_modifier:
                new_first_name = input("Nouveau prénom : ")
                user_manager.modify_user(email, first_name=new_first_name)
                print("Prénom modifié avec succès.")
            # Répétez pour les autres attributs...

        # Supprimer un utilisateur
        elif choix == '3':
            email = input("Entrez l'email de l'utilisateur à supprimer : ")
            confirmation = input("Êtes-vous sûr de vouloir supprimer cet utilisateur ? (oui/non) : ")
            if confirmation.lower() == "oui":
                user_manager.delete_user(email)
                print("Utilisateur supprimé avec succès.")
            else:
                print("Suppression annulée.")

        # Afficher tous les utilisateurs
        elif choix == '4':
            user_manager.display_users()

        # Quitter l'application
        elif choix == '5':
            print("Quitting...")
            break

# Si l'utilisateur a un rôle spécifique, affiche un message de bienvenue correspondant à ce rôle
elif user_role in ['user', 'chercheur', 'medecin', 'commercial', 'assistant']:
    print(f"Bienvenue {user_role.lower()}.")

# Si l'identification a échoué, affiche un message d'échec
else:
    print("Échec de la connexion.")
