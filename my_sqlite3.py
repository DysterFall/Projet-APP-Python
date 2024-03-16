import sqlite3
import hashlib

# Connexion à la base de données
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Création de la table users si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, region TEXT, password TEXT)''')

# Vérification si l'utilisateur lambda existe déjà
cursor.execute("SELECT * FROM users WHERE email=?", ("lambda@example.com",))
existing_lambda = cursor.fetchone()

# Si l'utilisateur lambda existe déjà, le supprimer
if existing_lambda:
    cursor.execute("DELETE FROM users WHERE email=?", ("lambda@example.com",))

# Hashage du mot de passe pour l'utilisateur lambda
lambda_password = hashlib.sha256("lambda123".encode()).hexdigest()

# Vérifier si l'utilisateur admin existe déjà
cursor.execute("SELECT * FROM users WHERE email=?", ("admin@example.com",))
existing_admin = cursor.fetchone()

# Si l'utilisateur admin existe déjà, le supprimer
if existing_admin:
    cursor.execute("DELETE FROM users WHERE email=?", ("admin@example.com",))

# Insertion de l'utilisateur admin
admin_password = hashlib.sha256("password123".encode()).hexdigest()
cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("Admin", "User", "admin@example.com", "123456789", "999", "ADMIN", "France", admin_password))
cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               ("Lambda", "User", "lambda@example.com", "987654321", "888", "chercheur", "Canada", lambda_password))


# Validation des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données mise à jour avec succès.")
