import requests
import sqlite3
import json
import time
import ssl
import sys

"""Constantes"""
# Api de localizaciones
URL = "https://py4e-data.dr-chuck.net/opengeo"
# Base de datos
conn = sqlite3.connect("geodata/opengeo.sqlite")
cur = conn.cursor()
# Evitar problemas con certificaciones SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

"""Creacion de DB"""
cur.execute("CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)")


"""Lectura de datos"""
with open("geodata/where.data") as data:
    count, notfount = 0, 0

    for line in data:
        if count > 100:
            print("Máximo de 100 datos por ejecución.")
            break
        
        address = line.strip()
        print("") # Línea en blanco

        # Buscando si ya está guardada la ubicacion en la db.
        cur.execute("SELECT geodata FROM Locations WHERE address = ?",
                    (memoryview(address.encode()), ))
        
        try:
            data = cur.fetchone()[0]
            print(f"Encontrado en la DB: {address}")
            continue
        except:
            pass

        # Llamado a API según la ubicación dada
        params = dict()
        params["q"] = address

        print(f"Obteniendo dirección URL: {URL}")
        request = requests.get(url=URL, params=params)
        response = request.content.decode()
        print(f"Obtenido: {len(response)} caracteres. {response[:20].replace("\n", " ")}")
        count += 1

        # Guardando datos en estructura de datos: diccionario
        try:
            js = json.loads(response)
        except:
            print(response) # En caso tal ocurra un error en la conversión.
            continue

        if not js or "features" not in js:
            print("=== Download Error ===")
            print(response)
            break

        if len(js["features"]) == 0:
            print("=== Ubicación no encontrada ===")
            notfount += 1

        # Guardando los datos obtenidos en la base de datos.
        cur.execute("INSERT INTO Locations (address, geodata) VALUES (?, ?)", 
                    (memoryview(address.encode()), memoryview(response.encode())))

        conn.commit()

        if count % 10 == 0:
            print("Haciendo pequeña pausa...")
            # time.sleep(5)

    if notfount > 0: print(f"{notfount} objetos cuyas ubicaciones no pudieron encontrarse.")


    print("\nHora de ejecutar geodump.py para visualizar en el mapa los datos obtenidos.\n")
