import sqlite3

# Conexión con la base de datos -si no existe, la crea-
conn = sqlite3.connect("db/my-database.sqlite")
db = conn.cursor()

# Borrado de la tabla si existe
db.execute("""
    DROP TABLE IF EXISTS counts;
""")

# Creación de la tabla
db.execute("""
    CREATE TABLE counts (
        count INTEGER,
        email TEXT
    );
""")

# Pidiendo archivo de correos.
fname = input("Ingresa el nombre del archivo: ")
if len(fname) < 1 : fname = "mbox-email.txt"

# Lectura de documento .txt con correos recibidos.
with open(f"files/{fname}") as text:
    for line in text:       # Por cada línea del archivo
        # Comprobación de si cuenta con un e-mail.
        # Va a la siguiente línea si no.
        if not line.startswith("From: "): continue

        # Se extrae el email
        pieces = line.split()
        email = pieces[1]

        # Buscando coincidencias en la DB
        db.execute("SELECT count from counts WHERE email = ?", (email,))
        row = db.fetchone()
        if row is None:     # Si no está guardado ese mail aún.
            query = "INSERT INTO counts (count, email) VALUES (1, ?)"
        else:               # Añadir a la cuenta del email.
            query = "UPDATE counts SET count = count + 1 WHERE email = ?"

        # Ejecución de query y escritura en DB.
        db.execute(query, (email,))
        conn.commit()

# Cantidad de coincidencias por email en orden descendente.
query = "SELECT email, count FROM counts ORDER BY count DESC LIMIT 10"
for row in db.execute(query):
    # Impresión 'email' : 'count'
    print(f"{row[0]}: {row[1]}")

# Se cierra la conexión con la base de datos
db.close()
