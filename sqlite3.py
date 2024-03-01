import sqlite3
import hashlib

# Connexion à la base de données
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Création de la table users si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, password TEXT)''')

# Insertion de l'utilisateur admin
admin_password = hashlib.sha256("password123".encode()).hexdigest()
cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
               ("Admin", "User", "admin@example.com", "123456789", "ADMIN", "admin", admin_password))

# Validation des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données mise à jour avec succès.")
