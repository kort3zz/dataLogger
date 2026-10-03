import sqlite3
import json


DB_NAME = "data/data.db"
CONFIG_NAME = "config.json"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            data_type TEXT NOT NULL,
            is_trend INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            object_id INTEGER NOT NULL,
            value TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def load_objects():
    with open(CONFIG_NAME, "r", encoding="utf-8") as file:
        config = json.load(file)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for obj in config["objects"]:
        cursor.execute("""
            INSERT OR REPLACE INTO objects
            (id, name, data_type, is_trend)
            VALUES (?, ?, ?, ?)
        """, (
            obj["id"],
            obj["name"],
            obj["type"],
            int(obj["trend"])
        ))

    connection.commit()
    connection.close()

def save_value(data):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO data_values
        (source_id, object_id, value, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        data["source_id"],
        data["object_id"],
        str(data["value"]),
        data["timestamp"]
    ))

    connection.commit()
    connection.close()

def show_values():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            source_id,
            object_id,
            value,
            timestamp
        FROM data_values
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    for row in rows:
        print(row)

if __name__ == "__main__":
    create_database()
    load_objects()

    print("Database created successfully.")
    print("Objects loaded from config.json.")

