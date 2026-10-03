import sqlite3
import random
from datetime import datetime

DB_NAME = "data/data.db"

def get_objects():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, data_type
        FROM objects
    """)

    objects = cursor.fetchall()

    connection.close()

    return objects

def generate_value(data_type):
    if data_type == "int":
        return random.randint(0, 1000)

    elif data_type == "byte":
        return random.randint(0, 255)

    elif data_type == "float":
        return round(random.uniform(0, 100), 2)

    elif data_type == "bool":
        return random.choice([True, False])

    elif data_type == "string":
        return random.choice([
            "Sensor-A",
            "Sensor-B",
            "Sensor-C",
            "Unknown"
        ])

    else:
        raise ValueError(f"Unknown data type: {data_type}")

def generate_data(source_id, obj):
    object_id, object_name, data_type = obj

    return {
        "source_id": source_id,
        "object_id": object_id,
        "object_name": object_name,
        "type": data_type,
        "value": generate_value(data_type),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    objects = get_objects()

    print("Generated values:")

    for obj in objects:
        data = generate_data(1, obj)
        print(data)