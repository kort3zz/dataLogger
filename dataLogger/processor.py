import json
from database import save_value

CONFIG_NAME = "config.json"
LOG_NAME = "logs/rejected.log"

def load_filters():
    with open(CONFIG_NAME, "r", encoding="utf-8") as file:
        config = json.load(file)

    return {
        obj["id"]: obj
        for obj in config["objects"]
    }

def check_condition(value, rule):
    condition = rule["condition"]

    if condition == "between":
        return rule["min"] <= value <= rule["max"]

    elif condition == "greater":
        return value > rule["min"]

    elif condition == "less":
        return value < rule["max"]

    elif condition == "equal":
        return value == rule["value"]

    else:
        raise ValueError(
            f"Unknown condition: {condition}"
        )


def save_rejected(data):
    with open(LOG_NAME, "a", encoding="utf-8") as file:
        file.write(
            f"{data['timestamp']} | "
            f"source={data['source_id']} | "
            f"object={data['object_name']} | "
            f"value={data['value']}\n"
        )

def process_data(data, filters):
    object_id = data["object_id"]

    if object_id not in filters:
        save_rejected(data)
        return False

    rule = filters[object_id]

    if check_condition(data["value"], rule):
        save_value(data)
        return True

    save_rejected(data)
    return False