import sqlite3, json, codecs

# Conexion con la db.
conn = sqlite3.connect("geodata/opengeo.sqlite")
cur = conn.cursor()

# Obteniendo todos los datos
cur.execute("SELECT * FROM Locations")

# Abriendo JS Que guardará y procesará las ubicaciones a visualizar.
with open("geodata/where.js", "w") as fhand:
    fhand.write("myData = [\n")
    count = 0

    # Iterando por cada fila de la tabla de la db
    for row in cur:
        data = str(row[1].decode())
        try: js = json.loads(data)
        except: continue

        if len(js["features"]) == 0: continue

        try:
            lat = js["features"][0]["geometry"]["coordinates"][1]
            lng = js["features"][0]["geometry"]["coordinates"][0]
            where = js["features"][0]["properties"]["display_name"]
            where = where.replace("'", "")
        except:
            print("Formato no válido.")
            print(js)
            continue

        try: 
            print(where, lat, lng)

            count += 1
            if count > 1 : fhand.write(",\n")
            output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
            fhand.write(output)
