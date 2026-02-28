import sqlite3
import csv

conn = sqlite3.connect("db/my-database.sqlite")
cur = conn.cursor()

def main():
    build_database()
    
    csv_file = input("CSV File Name: ")
    
    write_database(f"files/{csv_file}")
    

def build_database():
    cur.executescript("""
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;
                      
CREATE TABLE Artist (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER,
    title   TEXT UNIQUE,
    FOREIGN KEY (artist_id) REFERENCES Artist(id) ON DELETE SET NULL
);

CREATE TABLE Track (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER,
    rating INTEGER,
    count INTEGER,
    FOREIGN KEY (album_id) REFERENCES Album(id) ON DELETE SET NULL,
    FOREIGN KEY (genre_id) REFERENCES Genre(id) ON DELETE SET NULL
);
""")
    conn.commit()
    

def write_database(relative_loc: str):
    csv_file = open(relative_loc, "r")

    with csv_file as tracks:
        tracks_list = csv.reader(tracks)
        
        for track in tracks_list:
            print(*track)
            if len(track) < 6: continue
            
            query = """
                INSERT OR IGNORE INTO Artist (name)
                values (?);
            """
            cur.execute(query, (track[1],))
            
            query = """
                SELECT id FROM Artist WHERE name = ?;
            """
            cur.execute(query, (track[1],))
            artist_id = cur.fetchone()[0]
            
            query = """
                INSERT OR IGNORE INTO Genre (name)
                values (?);
            """
            cur.execute(query, (track[6],))
            
            query = """
                SELECT id FROM Genre WHERE name = ?;
            """
            cur.execute(query, (track[6],))
            genre_id = cur.fetchone()[0]
            
            query = """
                INSERT OR IGNORE INTO Album (title, artist_id)
                values (?, ?);
            """
            params = (track[2], artist_id)
            cur.execute(query, params)
            
            query = """
                SELECT id FROM Album WHERE title = ?;
            """
            cur.execute(query, (track[2],))
            album_id = cur.fetchone()[0]
            
            query = """
                INSERT OR IGNORE INTO Track
                (title, album_id, len, rating, count, genre_id)
                values (?, ?, ?, ?, ?, ?)
            """
            params = (track[0], album_id, track[5], track[4], track[3], genre_id)
            cur.execute(query, params)
            
            conn.commit()
        
if __name__ == "__main__":
    main()
