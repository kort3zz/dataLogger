import random
import time

from generator import get_objects, generate_data

def run_source(source_id, values_per_second, data_queue):
    objects = get_objects()

    delay = 1 / values_per_second

    while True:
        obj = random.choice(objects)

        data = generate_data(source_id, obj)

        data_queue.put(data)

        time.sleep(delay)