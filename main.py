import hashlib
import sqlite3
from class_manager import UserManager

username = input("Nom d'utilisateur : ")
password = input("Mot de passe : ")

user_manager = UserManager('user.db')  # Création de l'instance UserManager

user_role = user_manager.login(username, password)  # Utilisation de la méthode login

if user_role == 'ADMIN':
    while True:
        choix = user_manager.afficher_menu_admin()  # Utilisation de la méthode afficher_menu_admin()


        if choix == '1':
            first_name = input("Entrez le prénom de l'utilisateur : ")
            last_name = input("Entrez le nom de famille de l'utilisateur : ")
            email = input("Entrez l'email de l'utilisateur : ")
            phone = input("Entrez le numéro de téléphone de l'utilisateur : ")
            project_code = input("Entrez le code du projet de l'utilisateur : ")
            role = input("Entrez le rôle de l'utilisateur : ")
            region = input("Entrez la région de l'utilisateur : ")
            new_password = input("Entrez le mot de passe de l'utilisateur : ")

            nouvel_utilisateur = user_manager.create_user(first_name, last_name, email, phone, project_code, role, region, new_password)
            if nouvel_utilisateur:
                print("Utilisateur créé avec succès.")
            else:
                print("L'utilisateur n'a pas été créé en raison d'un rôle non valide.")

        elif choix == '2':
            email = input("Entrez l'email de l'utilisateur à modifier : ")

            # Demander quels attributs modifier
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
                new_first_name = input("Nouveau prénom : ")
                user_manager.modify_user(email, first_name=new_first_name)
                print("Prénom modifié avec succès.")
            if 2 in attributs_a_modifier:
                new_last_name = input("Nouveau nom de famille : ")
                user_manager.modify_user(email, last_name=new_last_name)
                print("Nom de famille modifié avec succès.")
            if 3 in attributs_a_modifier:
                new_email = input("Nouvel email : ")
                user_manager.modify_user(email, email=new_email)
                print("Email modifié avec succès.")
            if 4 in attributs_a_modifier:
                new_phone = input("Nouveau numéro de téléphone : ")
                user_manager.modify_user(email, phone=new_phone)
                print("Numéro de téléphone modifié avec succès.")
            if 5 in attributs_a_modifier:
                new_project_code = input("Nouveau code de projet : ")
                user_manager.modify_user(email, project_code=new_project_code)
                print("Code de projet modifié avec succès.")
            if 6 in attributs_a_modifier:
                new_role = input("Nouveau rôle : ")
                user_manager.modify_user(email, role=new_role)
                print("Rôle modifié avec succès.")
            if 7 in attributs_a_modifier:
                new_region = input("Nouvelle région : ")
                user_manager.modify_user(email, region=new_region)
                print("Région modifiée avec succès.")

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
            print("Quitting...")
            break

elif user_role == 'user':
    print("Bienvenue utilisateur normal.")

elif user_role == 'chercheur':
    print("Bienvenue chercheur.")

elif user_role == 'medecin':
    print("Bienvenue medecin.")

elif user_role == 'commercial':
    print("Bienvenue commercial.")

elif user_role == 'assistant':
    print("Bienvenue assistant.")

else:
    print("Échec de la connexion.")
