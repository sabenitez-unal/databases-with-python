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

