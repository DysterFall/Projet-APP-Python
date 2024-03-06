import sqlite3
import hashlib

# Connexion à la base de données
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Création de la table users si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, phone TEXT, project_code TEXT, role TEXT, region TEXT, password TEXT)''')

# Création de la table regions si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS regions
             (id INTEGER PRIMARY KEY, name TEXT)''')

# Création de la table units si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS units
             (id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER,
             FOREIGN KEY(region_id) REFERENCES regions(id))''')

# Création de la table projects si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS projects
             (code TEXT PRIMARY KEY, name TEXT, unit_id INTEGER,
             FOREIGN KEY(unit_id) REFERENCES units(id))''')

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

# Validation des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données mise à jour avec succès.")
