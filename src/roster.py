import sqlite3
import json

conn = sqlite3.connect('db/rosterdb.sqlite')
cur = conn.cursor()

def make_db():
    cur.executescript(
        """
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

"""
    )

def main():
    make_db()

    file_name = input("Enter the file name: ")
    if len(file_name) < 1: file_name = "roster_data.json"

    with open(f"files/{file_name}") as file:
        data = json.load(file)

        for entry in data:
            name = entry[0]
            title = entry[1]
            role = entry[2]

            print((name, title))

            cur.execute("INSERT OR IGNORE INTO User (name) VALUES (?)", (name,))
            cur.execute("SELECT id FROM User WHERE name = ?", (name,))
            user_id = cur.fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)", (title,))
            cur.execute("SELECT id FROM Course WHERE title = ?", (title,))
            course_id = cur.fetchone()[0]

            cur.execute("INSERT OR IGNORE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)", (user_id, course_id, role))
            
            conn.commit()

if __name__ == "__main__":
    main()
